<template>
  <div class="p-4 w-full">
    <h2 class="text-xl font-bold mb-4">{{ competitionEventName }} - Järjestatud tulemused</h2>

    <AgGridVue
      class="ag-theme-alpine"
      style="width: 100%; height: 500px"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :defaultColDef="defaultColDef"
      @cellValueChanged="onCellValueChanged"
      :rowSelection="{ type: 'multiple', enableClickSelection: true }"
    />

      <AgGridVue
        v-if="hasRegrouped"
        class="ag-theme-alpine mt-4"
        style="width: 100%; height: 400px"
        :columnDefs="finalColumnDefs"
        :rowData="finalists"
        :defaultColDef="defaultColDef"
        @cellValueChanged="onCellValueChanged"
        :rowSelection="{ type: 'multiple', enableClickSelection: true }"
       />


    <div class="mt-4 flex justify-end gap-2">
      <div v-if="regrouping && !hasRegrouped">
        <button class="btn btn-primary" @click="regroupFinalists">Grupeeri</button>
      </div>
      <button class="btn btn-secondary" @click="$router.back()">Tagasi</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, onBeforeUnmount, onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {AgGridVue} from 'ag-grid-vue3';
import {AllCommunityModule, ModuleRegistry} from 'ag-grid-community';
import ResultsService from '@/services/ResultsService';
import TimetableService from '@/services/TimetableService';
import type {IResult} from '@/types/IResult';

const route = useRoute();
const competitionEventId = Number(route.params.competition_event_id);
const selectedRound = Number(route.query.round_id);

const competitionEventName = ref('');
const columnDefs = ref<any[]>([]);
const rowData = ref<any[]>([]);
const numberOfAttempts = ref(3);
const finalistsAttemptCount = ref(3);
const finalistAthletesCount = ref(8);
const windMeasurement = ref(false);
const regrouping = ref(false);
const regroupingDone = ref(false);
const hasRegrouped = ref(false);
const finalists = ref<any[]>([]);
let socket: WebSocket | null = null;


ModuleRegistry.registerModules([AllCommunityModule]);

const defaultColDef = {
  resizable: true,
  sortable: true,
  filter: true,
};

onMounted(async () => {
  // Trying to create websocket here
  socket = new WebSocket("ws://localhost:8000/ws/results/");

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.type === "result_update") {
      console.log("Incoming result update:", message.data);

    }
  };

  const response = await TimetableService.getTimetableEntryById(competitionEventId);

  if (response.data) {
    competitionEventName.value = `${response.data.event.name} (${response.data.age_class.name})`;
    numberOfAttempts.value = response.data.number_of_attempts ?? 3;
    windMeasurement.value = response.data.wind_measurement ?? false;
    regrouping.value = response.data.regrouping ?? false;
    finalistsAttemptCount.value = response.data.finalists_attempt_count ?? 3;
    regroupingDone.value = response.data.regrouping_done;


  const staticColumns = [
      {
        headerName: 'Jrk',
        field: 'lane_or_order_number',
        editable: false,
        width: 100,
      },
      {
        headerName: 'BIB',
        field: 'BIB_number',
        editable: false,
        width: 80,
      },
      {
        headerName: 'Võistleja',
        field: 'athleteName',
        editable: false,
        width: 200,
      },
    ];

    const dynamicColumns: any[] = [];

    for (let i = 0; i < numberOfAttempts.value; i++) {
      dynamicColumns.push({
        headerName: `Katse ${i + 1}`,
        field: `attempt_${i + 1}`,
        editable: true,
        cellStyle: { backgroundColor: '#f0f9ff' }, // light blue
        width: 100,
      });

      if (windMeasurement.value) {
        dynamicColumns.push({
          headerName: `Tuul ${i + 1}`,
          field: `wind_${i + 1}`,
          editable: true,
          cellStyle: { backgroundColor: '#fef9f1' }, // light orange
          width: 100,
        });
      }
    }

    columnDefs.value = [...staticColumns, ...dynamicColumns];
  }


  const resultsResponse = await ResultsService.getResultsByRound(selectedRound);
  rowData.value = buildRowDataFromResults(resultsResponse.data).sort(
    (a, b) => (a.lane_or_order_number ?? 999) - (b.lane_or_order_number ?? 999)
  );
  if (regrouping.value && regroupingDone.value) {
    regroupFinalists();
  }
});

function buildRowDataFromResults(results: IResult[]): any[] {

    const athleteMap: Record<number, any> = {};

  for (const result of results) {
    const athleteId = result.competition_event_competition_athlete_id!;
    if (!athleteMap[athleteId]) {
      athleteMap[athleteId] = {
        lane_or_order_number: result.lane_or_order_number,
        BIB_number: result.BIB_number,
        athleteName: `${result.athlete.first_name} ${result.athlete.last_name}`,
        competition_event_competition_athlete_id: athleteId, // ✅ Add this!
      };
    }
    if (result.attempt_nr) {
      if (result.result_as_number !== undefined) {
        athleteMap[athleteId][`attempt_${result.attempt_nr}`] = result.result_as_number.toFixed(2);
      }

      if (
        result.wind_as_number !== null
      ) {
        const wind = result.wind_as_number;
        athleteMap[athleteId][`wind_${result.attempt_nr}`] = (wind >= 0 ? '+' : '') + wind.toFixed(1);
      }
    }
  }

  return Object.values(athleteMap);

}

const onCellValueChanged = async (event: any) => {
  const field = event.colDef.field;
  const newValue = event.newValue;

  const isWind = field.startsWith("wind_");
  const attemptNr = parseInt(field.split("_")[1]);
  const athlete = event.data;

  const existingAttempt = athlete[`attempt_${attemptNr}`];
  const existingWind = athlete[`wind_${attemptNr}`];


  const payload: IResult = {
    competition_event_competition_athlete_id: event.data.competition_event_competition_athlete_id,
    round_id: selectedRound,
    attempt_nr: attemptNr,
    result_as_number: isWind ? existingAttempt ?? null : parseFloat(newValue),
    wind_as_number: isWind ? parseFloat(newValue) : existingWind ?? null,
  };

  const response = await ResultsService.saveResults([payload]);
  if (response.errors) {
    console.error("❌ Save failed:", response.errors);
  } else {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({
        type: "result_update",
        data: payload
      }));
    }
  }
};

const regroupFinalists = async () => {
  hasRegrouped.value = true;
  await TimetableService.markRegroupingDone(competitionEventId);

  // Sort by best result across attempts
  const sorted = [...rowData.value].sort((a, b) => {
    const bestA = getBestAttempt(a);
    const bestB = getBestAttempt(b);
    return (bestB ?? 0) - (bestA ?? 0);
  });

  // Get top N
  const count = finalistAthletesCount.value ?? 8;
  finalists.value = sorted.slice(0, count).map(athlete => ({
    ...athlete,
    ...generateEmptyAttempts(finalistsAttemptCount.value)
  }));
};

const getBestAttempt = (athlete: any) => {
  const attempts = Object.keys(athlete)
    .filter(key => key.startsWith('attempt_'))
    .map(k => parseFloat(athlete[k]))
    .filter(v => !isNaN(v));
  return attempts.length ? Math.max(...attempts) : null;
};

const generateEmptyAttempts = (count: number) => {
  const obj: any = {};
  for (let i = 1; i <= count; i++) {
    obj[`attempt_${i}`] = null;
    obj[`wind_${i}`] = null;
  }
  return obj;
};

const finalColumnDefs = computed(() => {
  const attemptCols = [];
  const offset = numberOfAttempts.value;

  for (let i = 1; i <= finalistsAttemptCount.value; i++) {
    attemptCols.push({
      headerName: `Katse ${offset + i}`,
      field: `attempt_${offset + i}`,
      editable: true,
      cellStyle: { backgroundColor: '#f0f9ff' }, // light blue
      width: 100,
    });
    if (windMeasurement.value) {
      attemptCols.push({
        headerName: `Tuul ${offset + i}`,
        field: `wind_${offset + i}`,
        editable: true,
        cellStyle: { backgroundColor: '#fef9f1' }, // light orange
        width: 100,
      });
    }
  }
  return [
    { headerName: 'Jrk', field: 'lane_or_order_number', editable: false, width: 80 },
    { headerName: 'BIB', field: 'BIB_number', editable: false, width: 80 },
    { headerName: 'Võistleja', field: 'athleteName', editable: false },
    ...attemptCols
  ];
});

onBeforeUnmount(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<style scoped>
.ag-theme-alpine {
  font-size: 14px;
}
</style>
