<template>
  <div>
    <h2>{{ competitionEventName }}</h2>


    <!-- WIND INPUT if enabled -->
    <div v-if="windMeasurement" class="mb-3">
      <label for="wind" class="form-label">Tuule mõõtmine (m/s):</label>
      <input
        id="wind"
        v-model="windValue"
        type="number"
        step="0.1"
        class="form-control"
        style="width: 150px"
        @change="saveWind"
      />
    </div>

    <!-- AG GRID -->
    <AgGridVue
      class="ag-theme-alpine"
      style="width: 100%; height: 400px"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :defaultColDef="defaultColDef"
      @cellValueChanged="onCellValueChanged"
    />

    <div class="mt-3">
      <button class="btn btn-secondary" @click="$router.back()">Tagasi</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { AgGridVue } from 'ag-grid-vue3';
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
import TimetableService from '@/services/TimetableService';
import ResultsService from '@/services/ResultsService';
import type { IResult } from '@/types/IResult';
import { formatSecondsToTimeStringThousandths, parseTimeStringToSeconds } from "@/utils/Helper";

ModuleRegistry.registerModules([AllCommunityModule]);

const route = useRoute();
const competitionEventId = Number(route.params.competition_event_id);
const selectedRoundId = Number(route.query.round_id);

const competitionEventName = ref('Jooksu tulemused');
const windMeasurement = ref(false);
const windValue = ref<number | null>(null);
const columnDefs = ref<any[]>([]);
const rowData = ref<any[]>([]);

const defaultColDef = {
  resizable: true,
  sortable: true,
  filter: true,
};

onMounted(async () => {
  const response = await TimetableService.getTimetableEntryById(competitionEventId);
  if (response.data) {
    competitionEventName.value = `${response.data.event.name} (${response.data.age_class.name})`;
    windMeasurement.value = response.data.wind_measurement ?? false;

  }

  columnDefs.value = [
    { headerName: 'Jrk', field: 'lane_or_order_number', editable: false, width: 80 },
    { headerName: 'BIB', field: 'BIB_number', editable: false, width: 80 },
    { headerName: 'Võistleja', field: 'athleteName', editable: false, width: 200 },
    {
      headerName: 'Tulemus',
      field: 'result_as_number',
      editable: true,
      width: 120,
      valueFormatter: (params: any) => {
        return params.value ? params.value : '';
      },
    },
  ];

  const resultsRes = await ResultsService.getResultsByRound(selectedRoundId);
  if (resultsRes.data){
      const windResult = resultsRes.data.find((r: IResult) => r.wind_as_number !== null);
    if (windResult) {
      windValue.value = windResult.wind_as_number!;
    }
  }
  rowData.value = buildRowDataFromResults(resultsRes.data);
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
        competition_event_competition_athlete_id: athleteId,
      };
    }
    if (result.result_as_number != null) {
      athleteMap[athleteId].result_as_number =  formatSecondsToTimeStringThousandths(result.result_as_number);
    }
  }

  return Object.values(athleteMap);
}

const saveWind = async () => {
  if (windValue.value == null) return;
  const payload = rowData.value.map((row: any) => ({
    competition_event_competition_athlete_id: row.competition_event_competition_athlete_id,
    round_id: selectedRoundId,
    wind_as_number: windValue.value,
  }));
  await ResultsService.saveResults(payload);
};

const onCellValueChanged = async (event: any) => {

  const parsed = parseTimeStringToSeconds(event.newValue);
  if (parsed === null) {
    console.warn("Invalid time input:", event.newValue);
    return;
  }

  const payload: IResult = {
    competition_event_competition_athlete_id: event.data.competition_event_competition_athlete_id,
    round_id: selectedRoundId,
    result_as_number: parsed,
  };

  const response = await ResultsService.saveResults([payload]);
  if (response.errors) {
    console.error('❌ Save failed:', response.errors);
  }
};
</script>
