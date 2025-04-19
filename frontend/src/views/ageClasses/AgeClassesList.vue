<template>
  <div class="container mx-auto max-w-5xl px-4">
    <h1>Vanuseklassid</h1>
    <button @click="navigateToAddAgeClass" class="btn btn-primary">Lisa vanuseklass</button>
    <table class="table mt-3">
      <thead>
        <tr>
          <th>#</th>
          <th>Nimetus</th>
          <th>Min vanus (a)</th>
          <th>Max vanus (a)</th>
          <th>Sugu</th>
          <th>Muuda</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ageclass, index) in ageClasses" :key="ageclass.id">
          <td>{{ index + 1 }}</td> <!-- Display the index + 1 -->
        <td>{{ ageclass.name }}</td>
        <td>{{ ageclass.minimum_age }}</td>
        <td>{{ ageclass.maximum_age }}</td>
        <td>{{ ageclass.sex }}</td>
          <td>
            <RouterLink className="nav-link text-dark" :to="`/ageclasses/edit/${ageclass.id}/`"
              >Muuda</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AgeClassService from '@/services/AgeClassService'
import { useRouter } from 'vue-router'
import type { IAgeClass } from "@/types/IAgeClass";

const ageClasses = ref<IAgeClass[]>([]);
const router = useRouter()
const errors = ref<string[]>([]);
const isLoading = ref(false);

const fetchAgeClasses = async () => {
  isLoading.value = true;
  try {
    const res = await AgeClassService.getAllAgeClasses();
    if (res.data) {
      ageClasses.value = res.data;
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

const navigateToAddAgeClass = () => {
  router.push('/ageclasses/add')
}


onMounted(() => {
  fetchAgeClasses()
})
</script>

