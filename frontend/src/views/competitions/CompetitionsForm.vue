<template>
  <div class="container" style="max-width: 600px;">
    <h1>{{ isEdit ? 'Muuda võistlust' : 'Lisa võistlus' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="name" class="form-label">Nimetus:</label>
        <input
          v-model="competition.name"
          type="text"
          id="name"
          class="form-control"
          placeholder="Sisesta võistluse nimetus"
        />

        <div class="form-check">
          <input
            v-model="competition.active"
            type="checkbox"
            id="active"
            class="form-check-input"
          />
          <label for="active" class="form-check-label">Aktiivne?</label>
        </div>

        <label for="comments" class="form-label">Kommentaarid:</label>
        <textarea
          v-model="competition.comments"
          id="comments"
          class="form-control"
          placeholder="Sisesta kommentaarid..."
        ></textarea>

        <label for="start_time" class="form-label">Algusaeg:</label>
        <input
          v-model="competition.startDate"
          type="datetime-local"
          id="start_time"
          class="form-control"
        />

        <label for="end_time" class="form-label">Lõppaeg:</label>
        <input
          v-model="competition.endDate"
          type="datetime-local"
          id="end_time"
          class="form-control"
        />
      </div>
      <button type="submit" class="btn btn-primary">
        {{ isEdit ? 'Muuda' : 'Lisa' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CompetitionService from '@/services/CompetitionService'
import type { ICompetition } from "@/types/ICompetition";

const competition = ref<ICompetition>({
});

const isEdit = ref(false)
const route = useRoute()
const router = useRouter()

const fetchCompetition = async () => {
  if (route.params.id) {

    isEdit.value = true
    const response = await CompetitionService.getCompetitionById(route.params.id)
   if (response.data) {
      competition.value = {
        ...response.data,
        startDate: response.data.startDate?.slice(0, 16),
        endDate: response.data.endDate?.slice(0, 16),
      };
    }
  }
}


const submitForm = async () => {
  try {
    if (isEdit.value) {
      await CompetitionService.updateCompetition(route.params.id, competition.value);
    } else {
      await CompetitionService.createCompetition(competition.value);
    }
    router.push('/competitions');
  } catch (err) {
    console.error('Error submitting competition:', err);
  }
};

onMounted(fetchCompetition)
</script>
