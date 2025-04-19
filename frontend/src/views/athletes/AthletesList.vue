<template>
  <div class="container mx-auto max-w-5xl px-4">
    <h1>Võistlejad</h1>
    <button @click="navigateToAddAthlete" class="btn btn-primary">Lisa võistleja</button>

    <input
      type="text"
      data-testid="search-input"
      v-model="searchQuery"
      placeholder="Otsi ees- või perenime järgi"
      class="form-control my-3"
      style="max-width: 300px;"

    />

    <table class="table mt-3">
      <thead>
        <tr>
          <th>#</th>
          <th>Eesnimi</th>
          <th>Perenimi</th>
          <th>Sünniaeg</th>
          <th>Sugu</th>
          <th>Muuda</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(athlete, index) in filteredAthletes" :key="athlete.id">
          <td>{{ index + 1 }}</td> <!-- Display the index + 1 -->
          <td>{{ athlete.firstName }}</td>
          <td>{{ athlete.lastName }}</td>
          <td>{{ formatDateDOB(athlete.dateOfBirth!) }}</td>
          <td>{{ athlete.sex }}</td>
          <td>
            <RouterLink className="nav-link text-dark" :to="`/athletes/edit/${athlete.id}/`"
              >Muuda</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, computed} from 'vue'
import AthleteService from '@/services/AthleteService'
import { useRouter } from 'vue-router'
import type { IAthlete } from "@/types/IAthlete";
import { formatDateDOB } from '@/utils/Helper';


const athletes = ref<IAthlete[]>([]);
const router = useRouter()
const errors = ref<string[]>([]);
const isLoading = ref(false);
const searchQuery = ref("");

const fetchAthletes = async () => {
  isLoading.value = true;
  try {
    const res = await AthleteService.getAllAthletes();
    if (res.data) {
      athletes.value = res.data;
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

const filteredAthletes = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return athletes.value.filter(
    a =>
      a.firstName.toLowerCase().includes(query) ||
      a.lastName.toLowerCase().includes(query)
  );
});

const navigateToAddAthlete = () => {
  router.push('/athletes/add')
}


onMounted(fetchAthletes)
</script>

