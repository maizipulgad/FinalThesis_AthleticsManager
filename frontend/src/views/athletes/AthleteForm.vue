<template>
  <div class="container" style="max-width: 600px;">
    <h1>{{ isEdit ? 'Muuda võistlejat' : 'Lisa võistleja' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="first_name" class="form-label">Eesnimi:</label>
        <input
          v-model="athlete.firstName"
          type="text"
          id="first_name"
          class="form-control"
          placeholder="Sisesta eesnimi"
        />

        <label for="last_name" class="form-label">Perenimi:</label>
        <input
          v-model="athlete.lastName"
          type="text"
          id="last_name"
          class="form-control"
          placeholder="Sisesta perenimi"
        />

        <label for="date_of_birth" class="form-label">Sünniaeg:</label>
        <input
          v-model="athlete.dateOfBirth"
          type="date"
          id="date_of_birth"
          class="form-control"
        />

        <label for="sex" class="form-label">Sugu:</label>
        <input
          v-model="athlete.sex"
          type="text"
          id="sex"
          class="form-control"
        />

      </div>
      <button type="submit" class="btn btn-primary" data-testid="submit-btn">{{ isEdit ? 'Muuda' : 'Lisa' }}</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AthleteService from '@/services/AthleteService'
import type {IAthlete} from "@/types/IAthlete";

const athlete = ref<IAthlete>({

});

const isEdit = ref(false)
const route = useRoute()
const router = useRouter()

const fetchAthlete = async () => {
  if (route.params.id) {
    console.log("Fetching athlete with ID:", route.params.id);


    isEdit.value = true
    const response = await AthleteService.getAthleteById(route.params.id)
    if (response.data) {
      athlete.value = response.data
    }
  }
}

const submitForm = async () => {
  if (isEdit.value) {
    await AthleteService.updateAthlete(route.params.id, athlete.value)
  } else {
    await AthleteService.createAthlete(athlete.value)
  }
  await router.push('/athletes')
}

onMounted(fetchAthlete)
</script>
