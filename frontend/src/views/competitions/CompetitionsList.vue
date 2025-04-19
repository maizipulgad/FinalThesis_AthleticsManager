<template>
  <div class="container mx-auto max-w-5xl px-4">
    <h1>Võistlused</h1>
    <button @click="navigateToAddCompetition" class="btn btn-primary">Lisa võistlus</button>
    <table class="table mt-3">
      <thead>
        <tr>
          <th>#</th>
          <th>Nimetus</th>
          <th>Aktiivne?</th>
          <th>Kommentaarid</th>
          <th>Algusaeg</th>
          <th>Lõppaeg</th>
          <th>Muuda</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(competition, index) in competitions" :key="competition.id">
          <td>{{ index + 1 }}</td>
          <td>{{ competition.name }}</td>
          <td>
            <input
              type="checkbox"
              :checked="competition.active"
              disabled
              class="form-check-input"
            />
          </td>
          <td>{{ competition.comments }}</td>
          <td>{{ formatDate(competition.startDate) }}</td>
          <td>{{ formatDate(competition.endDate) }}</td>
          <td>
            <RouterLink className="nav-link text-dark" :to="`/competitions/edit/${competition.id}/`"
              >Muuda</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CompetitionService from '@/services/CompetitionService'
import { useRouter } from 'vue-router'
import type { ICompetition } from '@/types/ICompetition';
import { formatDate } from '@/utils/Helper';


const competitions = ref<ICompetition[]>([]);
const router = useRouter()
const errors = ref<string[]>([]);
const isLoading = ref(false);

const fetchCompetitions = async () => {
  isLoading.value = true;
  try {
    const res = await CompetitionService.getAllCompetitions();
    if (res.data) {
      competitions.value = res.data;
      errors.value = [];
    } else {
      errors.value = res.errors!;
    }
  } catch (error) {
    errors.value = ['An unexpected error occurred. Please try again.'];
  } finally {
    isLoading.value = false;
  }
};

const navigateToAddCompetition = () => {
  router.push('/competitions/add')
}


onMounted(fetchCompetitions)
</script>

