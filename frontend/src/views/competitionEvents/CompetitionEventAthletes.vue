<template>
  <div>
    <h2>{{ competitionEventName }}</h2>

      <!-- Buttons Container -->
      <div class="button-container">
        <router-link
          :to="`/competition-event/${competitionEventId}/manage-athletes`"
          class="btn btn-primary me-2"
        >
          Halda võistlejaid
        </router-link>

              <button @click="handleResultsClick" :disabled="selectedRound === null" class="btn btn-success">Sisesta tulemusi</button>
      </div>

        <!-- Jooks (Round) Buttons -->
      <div class="round-buttons">
        <!-- Kõik võistlejad Button (All Competitors) -->
        <button
          @click="selectedRound = null"
          class="btn"
          :class="{ 'btn-primary': selectedRound === null, 'btn-outline-primary': selectedRound !== null }"
        >
          Kõik võistlejad
        </button>

      <!--  Dynamically Generated "Jooks" Buttons -->
        <button
          v-for="round in rounds"
          :key="round.id"
          @click="selectedRound = round.id"
          class="btn btn-sm"
          :class="{ 'btn-primary': selectedRound === round.id, 'btn-outline-primary': selectedRound !== round.id }"
        >
          Jooks {{ round.roundNumber }}
        </button>
      </div>

      <!--  PRINT buttons -->
      <div class="mt-2">
        <button class="btn btn-outline-secondary btn-sm me-2" @click="generateStartPDF" :disabled="selectedRound === null">Stardiprotokoll</button>
        <button class="btn btn-outline-secondary btn-sm" @click="generateResultsPDF">Tulemuste protokoll</button>
      </div>

      <div class="container" style="max-width: 900px; margin-left: 0; margin-right: auto;">
        <div class="scroll-area">
        <table class="table">
          <thead>
            <tr>
              <th>BIB</th>
              <th>Jooks</th>
              <th>Rada</th>
              <th>Võistleja</th>
              <th>Sünniaeg</th>
              <th>Kollektiiv</th>
              <th v-for="i in maxAttempts" :key="i">Katse {{ i }}</th>
              <th>Parim</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="athlete in filteredAthletes" :key="athlete.competition_athlete_id">
              <td>{{ athlete.BIB_number }}</td>
              <td>{{ getResultForAthlete(athlete)?.round_number ?? '-' }}</td>
              <td>{{ getResultForAthlete(athlete)?.lane_or_order_number ?? '-' }}</td>
              <td>{{ athlete.athlete.first_name }} {{ athlete.athlete.last_name }}</td>
              <td>{{ formatDateDOB(athlete.athlete.date_of_birth) || '-' }}</td>
              <td>{{ athlete.collective?.name || '-' }}</td>
              <td v-for="i in maxAttempts" :key="`attempt_${i}`">
                <div>
                  <span>{{ getAttempt(athlete, i) ?? '-' }}</span>
                </div>
                <div class="text-muted small">
                  <span v-if="getWind(athlete, i) !== null">
                    {{ getWind(athlete, i) }}
                  </span>
                </div>
              </td>
                <td>
                  <strong>
                    {{ getBestResult(athlete) !== null ? formatSecondsToTimeStringHundredths(getBestResult(athlete)!) : '-' }}
                  </strong>
                </td>
            </tr>
          </tbody>
        </table>
      </div></div>

  </div>

  <ResultsModal
    v-if="showResultsModal"
    :showModal="showResultsModal"
    :selectedRound="selectedRound ?? undefined"
    :windMeasurementEnabled="windMeasurementEnabled"
    v-model:windValue="windValue"
    :filteredAthletes="filteredAthletes"
    @close="showResultsModal = false"
    @resultsSaved="handleResultsSaved"
/>
</template>

<script setup lang="ts">
import {ref, onMounted, watch, computed, onBeforeUnmount} from "vue";
import { useRoute, useRouter } from "vue-router";
import CompetitionAthletesService from "@/services/CompetitionAthletesService";
import type {ICompetitionAthlete} from "@/types/ICompetitionAthlete";
import { generateStartListPDF, generateResultsListPDF } from "@/utils/pdfHelpers";
import { formatSecondsToTimeStringHundredths } from "@/utils/Helper";


const route = useRoute();
const router = useRouter();

const assignedAthletes = ref<ICompetitionAthlete[]>([]);
const competitionEventName = ref("");
import { formatDateDOB } from '@/utils/Helper';
import TimetableService from "@/services/TimetableService";
import type {IRound} from "@/types/IRound";
import ResultsModal from "@/components/ResultsModal.vue";
import ResultsService from "@/services/ResultsService";
const competitionEventId = ref<number | null>(Number(route.params.competition_event_id)); // Use ref
const rounds = ref<IRound[]>([]);
const selectedRound = ref<number | null>(null);
const showResultsModal = ref(false);
const windMeasurementEnabled = ref(false);
const windValue = ref<number>(0);
const eventType  = ref<string>("");
const numberOfAttempts = ref<number>(1);

const handleResultsClick = () => {
  if (!selectedRound.value || !competitionEventId.value) return;

  if (["LONG_JUMP", "TRIPLE_JUMP" , "THROW"].includes(eventType.value)) {
    router.push({
      name: "JumpAndThrowResults",
      params: {
        competition_event_id: competitionEventId.value,
      },
      query: {
        round_id: selectedRound.value
      }
    });
  }
  else if (["HIGH_JUMP", "POLE_VAULT"].includes(eventType.value)) {
        router.push({
      name: "HighJumpAndPoleVaultResults",
      params: {
        competition_event_id: competitionEventId.value,
      },
      query: {
        round_id: selectedRound.value
      }
    });
  }
    if (["LONG_JUMP", "TRIPLE_JUMP" , "THROW"].includes(eventType.value)) {
    router.push({
      name: "JumpAndThrowResults",
      params: {
        competition_event_id: competitionEventId.value,
      },
      query: {
        round_id: selectedRound.value
      }
    });
  }
  else if (["RUNNING"].includes(eventType.value)) {
        router.push({
      name: "RunningResults",
      params: {
        competition_event_id: competitionEventId.value,
      },
      query: {
        round_id: selectedRound.value
      }
    });
  }
  else {
    showResultsModal.value = true;
  }
};


const handleResultsSaved = () => {
  showResultsModal.value = false;
  loadAthletes();
};


const loadAthletes = async () => {
  if (!competitionEventId.value) return;

    const [athRes, resRes, ttRes] = await Promise.all([
      CompetitionAthletesService.getAthletesByEvent(competitionEventId.value),
      ResultsService.getResultsByCompetitionEvent(competitionEventId.value),
      TimetableService.getTimetableEntryById(competitionEventId.value)
    ]);

    if (ttRes.data) {
      competitionEventName.value = `${ttRes.data.event.name} (${ttRes.data.age_class.name})`;
      windMeasurementEnabled.value = ttRes.data.wind_measurement ?? false;
      eventType.value = ttRes.data.event?.event_type.name;
      numberOfAttempts.value  = ttRes.data.number_of_attempts ?? 1;
      rounds.value = ttRes.data.rounds!.map((round) => ({
          id: round.round_id, // Use round_id for filtering
          roundNumber: round.round_number, // Display round number
          competitionEventId: round.competition_event_id,
          startTime: round.start_time,
        }));

    }

    if (athRes.data && resRes.data) {
      const allResults = resRes.data;
      assignedAthletes.value = athRes.data.map((athlete: any) => {
        athlete.results = allResults.filter((r: any) => r.competition_event_competition_athlete === athlete.competition_athlete_id);
        return athlete;
      });
    }

};


const maxAttempts = computed(() => {
  let max = 0;
  for (const athlete of assignedAthletes.value) {
    const event = athlete.assigned_events?.find(
      (e) => e.competition_event_id === competitionEventId.value
    );
    if (!event?.results) continue;

    for (const result of event.results) {
      if (result.attempt_nr && result.attempt_nr > max) {
        max = result.attempt_nr;
      }
    }
  }
  return max;
});

const getAttempt = (athlete: ICompetitionAthlete, attemptNr: number): string | null => {
  const event = athlete.assigned_events?.find(
    (e) => e.competition_event_id === competitionEventId.value
  );
  if (!event?.results) return null;

  const result = event.results.find(r => r.attempt_nr === attemptNr);
  if (!result || result.result_as_number === null) return null;

  const num = parseFloat(result.result_as_number!.toString());
  return isNaN(num) ? null : num.toFixed(2);
};


const getWind = (athlete: ICompetitionAthlete, attemptNr: number): string | null => {
  const event = athlete.assigned_events?.find(
    (e) => e.competition_event_id === competitionEventId.value
  );
  if (!event?.results) return null;

  const result = event.results.find(r => r.attempt_nr === attemptNr);
  if (!result || result.wind_as_number === null) return null;

  const wind = parseFloat(result.wind_as_number!.toString());
  if (isNaN(wind)) return null;

  return `${wind >= 0 ? "+" : ""}${wind.toFixed(1)}`;
};


function getBestResult(athlete: ICompetitionAthlete): number | null {
  const assignedEvent = athlete.assigned_events?.find(
    (event) => event.competition_event_id === competitionEventId.value
  );

  if (!assignedEvent?.results) return null;

  const filteredResults = selectedRound.value
    ? assignedEvent.results.filter(r => r.round === selectedRound.value)
    : assignedEvent.results;

  if (eventType.value === "HIGH_JUMP" || eventType.value === "POLE_VAULT") {
    // Special case: highest height cleared (entries ending with "O")
    let best = 0;
    for (const result of filteredResults) {
      if (result.result_as_char?.trim().endsWith("O") && result.result_as_number) {
        const height = parseFloat(result.result_as_number);
        if (height > best) best = height;
      }
    }
    return best > 0 ? best.toFixed(2) : "NH";
  }

  const best = Math.max(
    ...filteredResults
      .filter(r => r.result_as_number !== null && r.result_as_number !== undefined)
      .map(r => Number(r.result_as_number))
  );

  return isFinite(best) ? best : null;
}



const getResultForAthlete = (athlete: ICompetitionAthlete) => {
  const event = athlete.assigned_events?.find(
    (e) => e.competition_event_id === competitionEventId.value
  );

  if (!event?.results) return null;

  if (selectedRound.value) {
    return event.results.find((r) => r.round === selectedRound.value) ?? null;
  }
  return event.results[0] ?? null;
};



const filteredAthletes = computed(() => {
  if (!competitionEventId.value) return [];

  let athletes = assignedAthletes.value;

  if (selectedRound.value) {
    athletes = athletes.filter((athlete) =>
      athlete.assigned_events?.some(
        (event) =>
          event.competition_event_id === competitionEventId.value &&
          event.results?.some((result) => result.round === selectedRound.value)
      )
    );
  }

  const isTrackEvent = ["RUNNING", "SPRINT", "HURDLES"].includes(eventType.value ?? "");
  return [...athletes].sort((a, b) => {
    const resultA = getBestResult(a);
    const resultB = getBestResult(b);

    if (resultA === -Infinity && resultB === -Infinity) return 0;
    if (resultA === -Infinity) return 1;
    if (resultB === -Infinity) return -1;

    // Ascending for runs (less is better), descending for jumps/throws (more is better)
    return isTrackEvent ? resultA - resultB : resultB - resultA;
  });

});

const generateStartPDF = () => {
  const roundName = `Jooks ${rounds.value.find(r => r.id === selectedRound.value)?.roundNumber}`;
  generateStartListPDF(
    roundName,
    competitionEventName.value,
    filteredAthletes.value,
    numberOfAttempts.value,
    windMeasurementEnabled.value
  );
};

const generateResultsPDF = () => {
  generateResultsListPDF(
    filteredAthletes.value,
    competitionEventName.value,
    windMeasurementEnabled.value,
    maxAttempts.value,
      competitionEventId.value
  );
};


onMounted(() => {
  loadAthletes();
});

watch(() => route.params.competition_event_id, (newId) => {
  if (newId) {
    competitionEventId.value = Number(newId);
    loadAthletes();
  }
});

</script>


<style scoped>
.round-buttons {
  margin: 10px 0;
  display: flex;
  gap: 10px;
}

.round-buttons .btn {
  padding: 8px 15px;
  font-size: 14px;
}

.modal button {
  margin: 10px;
}
</style>