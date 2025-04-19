<template>

  <div class="container">
        <div class="card p-3 mb-4">
          <h2>Lisa võistlejaid sellele võistlusele</h2>

            <!-- Multiselect thingie  -->
            <multiselect
            v-model="selectedAthlete"
            :options="athletes"
            :multiple="false"
            :searchable="true"
            :close-on-select="true"
            :clear-on-select="true"
            :custom-label="formatAthleteLabel"
            :filter="customSearchFilter"
            track-by="id"
            placeholder="Otsi võistlejat..."
            open-direction="bottom"
          >

          <template #singleLabel="{ option }">
            {{ option.firstName }} {{ option.lastName }}
          </template>

          <!-- Show full name in the dropdown list -->
          <template #option="{ option }">
            {{ option.firstName }} {{ option.lastName }} (ID: {{ option.id }})
          </template>
          </multiselect>


          <!-- BIB  -->
          <label for="bibNumber" class="mt-2">BIB:</label>
          <input
            v-model="bibNumber"
            type="number"
            class="form-control"
            placeholder="Sisesta võistlejanumber"
          />

          <!-- Collective Selection Dropdown -->
          <label>Vali klubi:</label>
          <multiselect
            v-model="selectedCollective"
            label="name"
            track-by="id"
            placeholder="Otsi klubi..."
            open-direction="bottom"
            :options="collectives"
            :multiple="false"
            :searchable="true"
            :clear-on-select="true"
            :close-on-select="true"
          ></multiselect>


          <!-- Competition Events Selection -->
          <multiselect
              v-model="selectedEvents"
              label="displayLabel"
              track-by="competition_event_id"
              placeholder="Otsi võistlusala..."
              open-direction="bottom"
              :options="filteredEvents"
              :multiple="true"
              :searchable="true"
              @select="onEventSelected"
              :internal-search="false" :clear-on-select="false" :close-on-select="false" :options-limit="300"
                   :limit="6" :max-height="600" :show-no-results="false" :hide-selected="true"
                   @search-change="searchQuery = $event">


              <template #tag="{ option, remove }">
                <span class="multiselect__tag">
                  {{ option.age_class.name }} {{ option.event.name }}
                  <i class="multiselect__tag-icon" @click="remove(option)"></i>
                </span>
              </template>
            <template #noResult>
              <span>Oops! No elements found. Consider changing the search query.</span>
            </template>
            </multiselect>

          <br>

          <button @click="assignAthleteToEvents" class="btn btn-primary">Määra alad</button>
        </div>

    <!-- Display List of Existing Athletes -->
    <div class="card p-3">
        <h2>Selle võistluse võistlejad</h2>
        <div v-if="isLoading" class="loading-spinner">
    Loading athletes...
    </div>
      <table class="table table-striped mt-3">
        <thead>
          <tr>
            <th>BIB</th>
            <th>Võistleja</th>
            <th>Kollektiiv</th>
            <th>Võistlusalad</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="athlete in athletesWithEvents" :key="athlete.competition_athlete_id">
            <td>{{ athlete.BIB_number }}</td>
            <td>{{ athlete.athlete.first_name }} {{ athlete.athlete.last_name }}</td>
            <td>{{ athlete.collective?.name|| '-' }}</td>
            <td>
              <span v-if="athlete.assigned_events.length === 0">No events assigned</span>
              <template v-else>
                <span v-for="(event, index) in athlete.assigned_events" :key="event.competition_event_id">
                  {{ event.event_name }} ({{ event.age_class }}){{ index === athlete.assigned_events!.length - 1 ? '' : ', ' }}
                </span>
              </template>
            </td>
          </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>


<script setup lang="ts">
import {computed, onMounted, ref, watch} from "vue";
import {useHeaderStore} from "@/stores/header";
import CompetitionAthletesService from "@/services/CompetitionAthletesService";
import type {ICompetitionEventAthlete} from "@/types/ICompetitionEventAthlete";
import TimetableService from "@/services/TimetableService";
import type {ICompetitionEvent} from "@/types/ICompetitionEvent";
import AthleteService from "@/services/AthleteService";
import type {IAthlete} from "@/types/IAthlete";
import Multiselect from "vue-multiselect";
import type {ICompetitionAthlete} from "@/types/ICompetitionAthlete";
import { useToast } from "vue-toastification";
import type {ICollective} from "@/types/ICollective";
import CollectiveService from "@/services/CollectiveService";


const headerStore = useHeaderStore();
const athletes = ref<IAthlete[]>([]);
const events = ref<ICompetitionEvent[]>([]);
const selectedAthlete = ref<IAthlete | null>(null);
let selectedEvents = ref<ICompetitionEvent[]>([]);
const athletesWithEvents = ref<ICompetitionAthlete[]>([]);
const isLoading = ref(false);
const bibNumber = ref<number | null>(null); // Store BIB number
const selectedCollective = ref<ICollective | null>(null);
const collectives = ref<ICollective[]>([]);

const showAthleteList = ref(false); // Controls dropdown visibility
const athleteSearch = ref('');
const eventSearch = ref('');
const searchQuery = ref("");
const toast = useToast();


const customSearchFilter = (option: IAthlete, query: string) => {
  const fullName = `${option.firstName} ${option.lastName} (ID: ${option.id})`.toLowerCase();
  return fullName.includes(query.toLowerCase());
};


const filteredEvents = computed(() => {
  return events.value
    .filter(event =>
      event.event.name.toLowerCase().includes(eventSearch.value.toLowerCase())
    )
    .map(event => ({
      ...event,
      displayLabel: `${event.age_class?.name + " " + event.event.name}`
    }));
});


const onEventSelected = (event: any) => {
  if (event.competition_event_id) {
    selectedEventIds.value.push(event.competition_event_id); // Store only the ID
  }
};


const selectedEventIds = computed({
  get: () => selectedEvents.value.map(event => event.competition_event_id),
  set: (ids) => {
    // Prevent duplicates
    selectedEvents.value = events.value.filter(event => ids.includes(event.competition_event_id));
  }
});

const formatAthleteLabel = (athlete:  IAthlete) => {
  return `${athlete.firstName} ${athlete.lastName} (ID: ${athlete.id})`;
};

const fetchAthletes = async () => {
  if (!headerStore.selectedCompetitionId) return;
  const response = await AthleteService.getAllAthletes();
  if (response.data) {
    athletes.value = response.data;
  }
};

const fetchEvents = async () => {
  if (!headerStore.selectedCompetitionId) return;
  const response = await TimetableService.getTimetableByCompetition(headerStore.selectedCompetitionId);
  if (response.data) {
    events.value = response.data;
  }
};

const fetchCollectives = async () => {
  if (!headerStore.selectedCompetitionId) return;
  const response = await CollectiveService.getAllCollectives();
  if (response.data) {
    collectives.value = response.data;
  }
};

// Assign athlete to selected events
const assignAthleteToEvents = async () => {
  if (!selectedAthlete.value) {
    toast.error("Palun lisa võistlejale vähemalt üks võistleja.");
    return;
  }

    if (!bibNumber.value) {
    toast.error("Palun lisa võistlejanumber.");
    return;
  }

  const competitionId = headerStore.selectedCompetitionId; // Ensure competition is selected
  if (!competitionId) {
    toast.error("Ühtki võistlust ei ole valitud!");
    return;
  }

  // 1. Ensure the athlete exists in CompetitionAthlete
  const competitionAthlete = await CompetitionAthletesService.createOrGetCompetitionAthlete(
    competitionId,
    selectedAthlete.value.id,
    bibNumber!.value,
    selectedCollective.value?.id || null, //
  );

  if (!competitionAthlete) {
    toast.error("Failed to register athlete in competition.");
    return;
  }

  const competitionAthleteId = competitionAthlete.competition_athlete_id;

  const existing = athletesWithEvents.value.find(
    a => a.competition_athlete_id === competitionAthleteId
  );

  const existingEventIds = existing?.assigned_events.map(e => e.competition_event_id) || [];
  const selectedEventIdsSet = new Set(selectedEventIds.value);


  // 2. Remove deselected events
  for (const existingEventId of existingEventIds) {
    if (!selectedEventIdsSet.has(existingEventId)) {
      const entryToRemove = existing?.assigned_events.find(e => e.competition_event_id === existingEventId);
      if (entryToRemove) {
        const removed = await CompetitionAthletesService.removeAthleteFromEvent(entryToRemove.competition_event_competition_athlete_id);
        if (!removed) {
          toast.error(`Viga eemaldamisel: ${entryToRemove.event_name}`);
        }
      }
    }
  }

  const eventsToAssign = [...new Set(
    selectedEventIds.value.filter(
      id => !existingEventIds.includes(id)
    )
  )];


  for (const eventId of eventsToAssign) {
    const entry: ICompetitionEventAthlete = {
      competition_event_id: eventId,
      competition_athlete_id: competitionAthleteId,
    };

    const response = await CompetitionAthletesService.addAthleteToEvent(entry);
    if (!response) {
      toast.error(`Failed to assign athlete to event ${eventId}`);
    }
  }

  toast.success("Athlete successfully assigned to selected events!");

  // Re-set the values
  athleteSearch.value = "";
  selectedAthlete.value = null;
  selectedCollective.value = null;
  selectedEvents.value = [];
  bibNumber.value = null;
  showAthleteList.value = false;

  await fetchAthletesWithEvents();
};

const fetchAthletesWithEvents = async () => {
  if (!headerStore.selectedCompetitionId) return;
  isLoading.value = true;

  try {
    const response = await CompetitionAthletesService.getAthletesByCompetition(
      headerStore.selectedCompetitionId
    );

    if (response && response.data) {
      athletesWithEvents.value = response.data;
    } else {
      athletesWithEvents.value = [];
    }
  } catch (error) {
    console.error("Error fetching athletes:", error);
    toast.error("Failed to load athletes.");
  } finally {
    isLoading.value = false; // Hide loading indicator
  }
};

onMounted(() => {
  fetchAthletes();
  fetchEvents();
  fetchAthletesWithEvents();
  fetchCollectives();
});

watch(selectedAthlete, async (newAthlete) => {

  if (!newAthlete) {
    bibNumber.value = null;
    selectedCollective.value = null;
    selectedEvents.value = [];
    return;
  }

  if (!headerStore.selectedCompetitionId) return;

  const response = await CompetitionAthletesService.getAthletesByCompetition(
    headerStore.selectedCompetitionId
  );

  const competitionEntry = response.data?.find(
    entry => entry.athlete.athlete_id === newAthlete.id
  );

  if (competitionEntry) {
    bibNumber.value = competitionEntry.BIB_number;
    selectedCollective.value = collectives.value.find(c => c.id === competitionEntry.collective?.collective_id) || null;
    selectedEvents.value = events.value.filter(ev =>
      competitionEntry.assigned_events.some(assigned =>
        assigned.competition_event_id === ev.competition_event_id
      )
    );
  }
});

</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.css">

.container {
  max-width: 900px;
  margin: auto;
}

.card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.multiselect__tag {
  background-color: #4CAF50;
  color: white;
  padding: 4px 8px;
  border-radius: 20px;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
  margin-right: 5px;
}

.multiselect__tag-icon {
  cursor: pointer;
  font-weight: bold;
  margin-left: 1px;
  color: white;
  font-size: 16px;
  line-height: 1;
}

</style>
