<template>
  <div class="container" style="max-width: 600px;">
    <h1>{{ isEdit ? 'Muuda vanuseklassi' : 'Lisa vanuseklass' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="name" class="form-label">Nimi:</label>
        <input
          v-model="ageclass.name"
          type="text"
          id="name"
          class="form-control"
          placeholder="Sisesta võistlusklassi nimi"
        />

        <label for="minimum_age" class="form-label">Min iga (aastates):</label>
        <input
          v-model="ageclass.minimum_age"
          type="number"
          id="minimum_age"
          class="form-control"
        />

        <label for="maximum_age" class="form-label">Max iga (aastates):</label>
        <input
          v-model="ageclass.maximum_age"
          type="number"
          id="maximum_age"
          class="form-control"
        />

        <label for="sex" class="form-label">Sugu:</label>
        <input
          v-model="ageclass.sex"
          type="text"
          id="sex"
          class="form-control"
        />

      </div>
      <button type="submit" class="btn btn-primary">{{ isEdit ? 'Muuda' : 'Lisa' }}</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AgeClassService from '@/services/AgeClassService'
import type {IAgeClass} from "@/types/IAgeClass";

const ageclass = ref<IAgeClass>({

});
const isEdit = ref(false)
const route = useRoute()
const router = useRouter()

const fetchAgeClass = async () => {
  if (route.params.id) {
    console.log("fetching age class with ID ", route.params.id)
    isEdit.value = true
    const response = await AgeClassService.getAgeClassById(route.params.id);
    if (response.data) {
      ageclass.value = response.data
    }
  }
}

const submitForm = async () => {

  if (isEdit.value) {
    await AgeClassService.updateAgeClass(route.params.id, ageclass.value)
  } else {
    await  AgeClassService.createAgeClass(ageclass.value)
  }
  await router.push('/age-classes')
}

onMounted(() => {
  console.log("Mounted correctly FORM!");
  fetchAgeClass()
})

</script>
