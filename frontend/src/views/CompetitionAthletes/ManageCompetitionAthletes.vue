<template>
  <div class="container" style="max-width: 900px; margin-left: 0; margin-right: auto;">
    <h2>Halda võistlejaid</h2>
    <table class="table">
      <thead>
        <tr>
          <th>BIB</th>
          <th>Võistleja</th>
          <th>Kollektiiv</th>
          <th>Jooks (Grupp)</th>
          <th width="50px">Rada (Järjekord)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="athlete in assignedAthletes" :key="athlete.competition_athlete_id">
          <td>{{ athlete.BIB_number }}</td>
          <td>{{ athlete.athlete.first_name }} {{ athlete.athlete.last_name }}</td>
          <td>{{ athlete.collective?.name || "-" }}</td>

          <!-- Round ("Jooks"") Selection -->
          <td>
            <multiselect
              v-model="athlete.selectedRound"
              :options="rounds"
              placeholder="Vali Jooks"
              :multiple="false"
              track-by="id"
              label="name"
            />
          </td>

          <!-- Lane ("Rada") Input -->
          <td>
            <input v-model="athlete.selectedLane" type="number" min="1" class="form-control" />
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Save and Cancel Buttons -->
    <div class="button-container">
      <button class="btn btn-success" @click="saveAssignments">Salvesta / Uuenda</button>
      <router-link :to="`/competition-event/${competitionEventId}`" class="btn btn-secondary">
        Tagasi
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import CompetitionAthletesService from "@/services/CompetitionAthletesService";
import Multiselect from "vue-multiselect";
import { useToast } from "vue-toastification";
import type {ICompetitionAthlete} from "@/types/ICompetitionAthlete";
import TimetableService from "@/services/TimetableService";
import type {IRound} from "@/types/IRound";

const toast = useToast();
const route = useRoute();
const router = useRouter();

const competitionEventId = Number(route.params.competition_event_id);
const assignedAthletes = ref<ICompetitionAthlete[]>([]);

const rounds = ref<IRound[]>([]);

const fetchTimetableEntry = async () => {
  const response = await TimetableService.getTimetableEntryById(competitionEventId);
  if (response.data) {
    rounds.value = response!.data.rounds.map(round => ({
      id: round.round_id,
      name: `Jooks ${round.round_number}`,
      roundNumber: round.round_number,
      competitionEventId: round.competition_event_id,
      startTime: round.start_time,
    }));
  } else {
    console.error("Failed to fetch number_of_rounds:", response.errors);
  }
};


// Load athletes and their assigned rounds/lane
const fetchAthletes = async () => {
  const response = await CompetitionAthletesService.getAthletesByEvent(competitionEventId);
  if (response.data) {
    assignedAthletes.value = response.data.map((athlete) => {
      const assignedEvent = athlete!.assigned_events!.find(event => event.competition_event_id === competitionEventId);
      const result = assignedEvent?.results.length! > 0 ? assignedEvent!.results[0] : null;

      return {
        ...athlete,
        selectedRound: result?.round
          ? rounds.value.find(r => r.id === result.round) || null  // ✅ Ensures correct object
          : null, // Default to null if not assigned
        selectedLane: result?.lane_or_order_number || 1, // Load existing lane_number or default to 1
      };
    });
  }
};


const saveAssignments = async () => {
  try {
    const payload = assignedAthletes.value.map((athlete) => {
      const assignedEvent = athlete.assigned_events.find(event =>
        event.competition_event_id === competitionEventId
      );

      if (!assignedEvent) {
        console.warn(`⚠ No assigned event found for athlete ${athlete.athlete.first_name} ${athlete.athlete.last_name}`);
        return null;
      }

      return {
        competition_event_competition_athlete_id: assignedEvent.competition_event_competition_athlete_id,
        round_number: athlete.selectedRound?.id || null,
        lane_number: athlete.selectedLane,
      };
    });

    if (payload.length === 0) {
      toast.error("❌ No valid assignments found.");
      return;
    }

    const success = await CompetitionAthletesService.assignRoundsAndLanes(payload);
    if (success) {
      toast.success("Athlete assignments saved!");
      router.back();
    } else {
      toast.error("Failed to save assignments.");
    }
  } catch (error) {
    toast.error("Unexpected error.");
  }
};

onMounted(() => {
  fetchAthletes();
  fetchTimetableEntry();

});</script>

<style scoped>
.button-container {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>
