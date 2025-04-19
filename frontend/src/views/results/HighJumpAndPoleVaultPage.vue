<template>
  <div>
    <h2>{{ competitionEventName }}</h2>

    <div class="mb-3">
      <router-link
        :to="`/competition-event/${competitionEventId}/manage-athletes`"
        class="btn btn-primary me-2"
      >
        Halda võistlejaid
      </router-link>
      <button @click="showHeightModal = true" class="btn btn-outline-primary">
        Määra algkõrgused
      </button>
    </div>

    <HeightSetupModal
      v-if="showHeightModal"
      :roundId="selectedRoundId"
      @close="showHeightModal = false"
      @heightsSaved="loadJumpHeights"
    />

    <AgGridVue
      class="ag-theme-alpine"
      style="width: 100%; height: 500px"
      :columnDefs="columnDefs"
      :rowData="rowData"
      :defaultColDef="defaultColDef"
      @cellValueChanged="onCellValueChanged"
      :rowSelection="{ type: 'multiple', enableClickSelection: true }"

    />
      <div>
      <button class="btn btn-secondary" @click="$router.back()">Tagasi</button>
  </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import {AgGridVue} from 'ag-grid-vue3';
import {AllCommunityModule, ModuleRegistry} from 'ag-grid-community';
import HeightSetupModal from "@/components/HeightSetupModal.vue";
import JumpHeightService from "@/services/JumpHeightService";
import ResultsService from "@/services/ResultsService";
import TimetableService from "@/services/TimetableService";
import type {IResult} from "@/types/IResult";

const route = useRoute();
const competitionEventId = Number(route.params.competition_event_id);
const selectedRoundId = Number(route.query.round_id);
const competitionEventName = ref("Kõrgushüpe / Teivashüpe");
const columnDefs = ref<any[]>([]);


const showHeightModal = ref(false);
const jumpHeights = ref<number[]>([]);
const rowData = ref<any[]>([]);

ModuleRegistry.registerModules([AllCommunityModule]);

const defaultColDef = {
  resizable: true,
  sortable: true,
  filter: true,
};


onMounted(async () => {
  const response = await TimetableService.getTimetableEntryById(competitionEventId);

  if (response.data) {
    competitionEventName.value = `${response.data.event.name} (${response.data.age_class.name})`;

    const heightsResponse = await JumpHeightService.getHeightsByRound(selectedRoundId!);
    if (heightsResponse.data) {
      jumpHeights.value = heightsResponse.data.map(h => parseFloat(h.height.toString()));
    }

    const staticColumns = [
      {
        headerName: "Jrk",
        field: "lane_or_order_number",
        editable: false,
        width: 80,
      },
      {
        headerName: "BIB",
        field: "BIB_number",
        editable: false,
        width: 80,
      },
      {
        headerName: "Võistleja",
        field: "athleteName",
        editable: false,
        width: 200,
      },
      {
        headerName: "Algkõrgus",
        field: "startingHeight",
        editable: true,
        width: 130,
        cellEditor: "agSelectCellEditor",
        cellEditorParams: {
          values: jumpHeights.value.map(h => h.toFixed(2)), // drop-down
        },
      },
    ];

    const dynamicColumns = jumpHeights.value.map((height) => {
      const fieldKey = `height_${height.toFixed(2)}`;
      return {
        headerName: height.toFixed(2),
        field: `height_${height.toFixed(2)}`,
        editable: true,
        cellEditor: 'agTextCellEditor',

        valueSetter: (params: any) => {
          params.data[params.colDef.field] = params.newValue;
          return true;
        },
        valueGetter: (params: any) => {
        return params.data?.[fieldKey] || "";
        },
        width: 100,
        cellStyle: { backgroundColor: "#fef9f1" },
      };
    });

    columnDefs.value = [...staticColumns, ...dynamicColumns, {
      headerName: "Parim",
      field: "best",
      width: 120,
      editable: false,
    }];
  }

  const resultsResponse = await ResultsService.getResultsByRound(selectedRoundId!);
  rowData.value = buildRowDataFromResults(resultsResponse.data);
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
        startingHeight: result.starting_height ?? "",
        competition_event_competition_athlete_id: athleteId,
      };
    }

    if (result.result_as_char && result.result_as_number) {
      const fieldKey = `height_${result.result_as_number.toFixed(2)}`;
      athleteMap[athleteId][fieldKey] = result.result_as_char;

    }
  }

  //Optionally compute "best" from cleared heights (for sorting)
  Object.values(athleteMap).forEach((athlete: any) => {
    let best = 0;
    for (const key of Object.keys(athlete)) {
      if (
          key.startsWith("height_") &&
          typeof athlete[key] === "string" &&
          athlete[key].trim().endsWith("O")
      ) {
        const height = parseFloat(key.replace("height_", ""));
        if (height > best) best = height;
      }
    }
    athlete.best = best > 0 ? best.toFixed(2) : "NH";
  });
  return Object.values(athleteMap);
}

const onCellValueChanged = async (event: any) => {
  const field = event.colDef.field;
  const athlete = event.data;
  const newValue = event.data[field];

  if (field === "startingHeight") {
    const startingHeight = parseFloat(newValue);
    const athleteId = athlete.competition_event_competition_athlete_id;

    const resultsToSave: IResult[] = [];

    for (const h of jumpHeights.value) {
      const height = parseFloat(h.toFixed(2));

      if (height < startingHeight) {
        // Insert skipped mark "-"
        resultsToSave.push({
          competition_event_competition_athlete_id: athleteId,
          round_id: selectedRoundId!,
          starting_height: height,
          result_as_char: "-",
          result_as_number: height,
        });

        // Immediately show it in the frontend grid as well
        athlete[`height_${height.toFixed(2)}`] = "-";
      }
    }

    // Save "-" skips
    if (resultsToSave.length > 0) {
      const response = await ResultsService.saveResults(resultsToSave);
      if (response.errors) {
        console.error("❌ Saving skipped heights failed", response.errors);
      }
    }

  // Save the starting height (as before)
    const response = await ResultsService.saveResults([{
      competition_event_competition_athlete_id: athleteId,
      round_id: selectedRoundId!,
      starting_height: startingHeight,
    }]);

    if (response.errors) {
      console.error("❌ Save failed:", response.errors);
    }
  }

  if (field.startsWith("height_")) {
    const height = parseFloat(field.replace("height_", ""));
    const payload: IResult = {
      competition_event_competition_athlete_id: athlete.competition_event_competition_athlete_id,
      round_id: selectedRoundId!,
      result_as_number: height,
      starting_height: height,
      result_as_char: newValue,
    };
    const response = await ResultsService.saveResults([payload]);

    if (response.errors) {
      console.error("❌ Save failed:", response.errors);
    }
  }
  const resultsResponse = await ResultsService.getResultsByRound(selectedRoundId!);
  rowData.value = buildRowDataFromResults(resultsResponse.data);
};

async function loadJumpHeights() {
  const res = await JumpHeightService.getHeightsByRound(selectedRoundId);
  if (res.data) {
    jumpHeights.value = res.data.map((h) => parseFloat(h.height));
  }
}
</script>
