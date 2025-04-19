<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-dialog" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Sisesta tulemusi - Jooks {{ selectedRoundNumber }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitForm">
            <div class="mb-3">

            <!-- Wind Measurement Field (If Applicable) -->
            <div v-if="windMeasurementEnabled">
              <label for="wind">Tuule kiirus (m/s):</label>
              <input v-model="form.windValue" type="number" step="0.01" class="form-control" />
            </div>

            <!-- Athlete Results Input -->
            <table class="table">
              <thead>
                <tr>
                  <th>BIB</th>
                  <th>Athlete</th>
                  <th>Result (s)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="athlete in form.results" :key="athlete.competition_athlete_id">
                  <td>{{ athlete.BIB_number }}</td>
                  <td>{{ athlete.athleteName }}</td>
                  <td>
                    <input
                      v-model="athlete.resultInput"
                      type="number"
                      step="0.001"
                      class="form-control"
                      placeholder="Enter time"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button @click="saveResults" class="btn btn-primary">Salvesta tulemused</button>
            <button @click="closeModal" class="btn btn-secondary">Tühista</button>
          </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {defineProps, defineEmits, ref, onMounted} from "vue";
  import ResultsService from "@/services/ResultsService";
  const selectedRoundNumber = ref<number | null>(null);

    const props = defineProps({
      showModal: Boolean,
      selectedRound: Number,
      windMeasurementEnabled: Boolean,
  });
  const emit = defineEmits(['close', 'resultsSaved']);

  const form = ref({
    results: [] as {
      result_id: number | null;
      competition_event_competition_athlete_id: number;
      BIB_number: number;
      athleteName: string;
      resultInput: number | null;
    }[],
    windValue: 0,
  });
  const closeModal = () => {
    emit("close");
  };

  const fetchResults = async () => {
  if (!props.selectedRound) return;

  try {
    const response = await ResultsService.getResultsByRound(props.selectedRound);


    form.value.results = response!.data.map((r: any) => ({
      result_id: r.result_id,
      competition_event_competition_athlete_id: r.competition_event_competition_athlete_id,
      resultInput: r.result_as_number ?? null,
      BIB_number: r.BIB_number ?? '-',
      athleteName: `${r.athlete.first_name} ${r.athlete.last_name}`,
    }));

    // Set wind value from first result (or default to 0)
    form.value.windValue = response!.data[0]?.wind_as_number ?? 0;

    selectedRoundNumber.value = response.data[0].round_number ?? 0;

  } catch (error) {
    console.error("❌ Failed to load round results:", error);
  }
};

onMounted(() => {
  fetchResults();
});

const saveResults = async () => {
  try {
    const payload = form.value.results.map((athlete) => ({
      competition_event_competition_athlete_id: athlete.competition_event_competition_athlete_id,
      round_id: props.selectedRound,
      result_as_number: athlete.resultInput,
      wind_as_number: props.windMeasurementEnabled ? parseFloat(form.value.windValue.toFixed(2)) : null,
    }));


  const response = await ResultsService.saveResults(payload);

    if (response.data) {
      emit("resultsSaved", form.value);
      closeModal();
    } else {
      console.error("Failed to save results:", response.errors);
    }
  } catch (error) {
    console.error("Error saving results:", error);
  }
};
</script>

<style scoped>
.modal-overlay {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}
</style>
