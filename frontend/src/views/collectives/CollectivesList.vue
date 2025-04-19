<template>
  <div class="container mx-auto max-w-5xl px-4">
    <h1>Kollektiivid</h1>
    <button @click="navigateToAddCollective" class="btn btn-primary">Lisa kollektiiv</button>
    <table class="table mt-3">
      <thead>
        <tr>
          <th>#</th>
          <th>Nimetus</th>
          <th>Lühend</th>
          <th>Kommentaar</th>
          <th>Muuda</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(collective, index) in collectives" :key="collective.id">
          <td>{{ index + 1 }}</td> <!-- Display the index + 1 -->
        <td>{{ collective.name }}</td>
        <td>{{ collective.abbreviation }}</td>
        <td>{{ collective.additionalInformation }}</td>
          <td>
            <RouterLink className="nav-link text-dark" :to="`/collectives/edit/${collective.id}/`"
              >Muuda</RouterLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { ICollective } from "@/types/ICollective";
import CollectiveService from "@/services/CollectiveService";


const collectives = ref<ICollective[]>([]);
const router = useRouter()
const errors = ref<string[]>([]);
const isLoading = ref(false);


const fetchCollectives = async () => {
  isLoading.value = true;
  try {
    const res = await CollectiveService.getAllCollectives();
    if (res.data) {
      collectives.value = res.data;
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

const navigateToAddCollective = () => {
  router.push('/collectives/add')
}


onMounted(() => {
  fetchCollectives()
})
</script>

