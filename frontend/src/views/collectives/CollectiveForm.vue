<template>
  <div class="container" style="max-width: 600px;">
    <h1>{{ isEdit ? 'Muuda kollektiivi' : 'Lisa kollektiiv' }}</h1>
    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="name" class="form-label">Nimetus:</label>
        <input
          v-model="collective.name"
          type="text"
          id="name"
          class="form-control"
          placeholder="Sisesta kollektiivi nimi"
        />

        <label for="abbreviation" class="form-label">Lühend (4 tähte):</label>
        <input
          v-model="collective.abbreviation"
          type="text"
          id="abbreviation"
          class="form-control"
        />

        <label for="additionalInformation" class="form-label">Kommentaar:</label>
        <input
          v-model="collective.additionalInformation"
          type="text"
          id="additionalInformation"
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
import type {ICollective} from "@/types/ICollective";
import CollectiveService from "@/services/CollectiveService";
import {useToast} from "vue-toastification";

const collective = ref<ICollective>({

});
const isEdit = ref(false)
const route = useRoute()
const router = useRouter()
const toast = useToast();

const fetchCollective = async () => {
  if (route.params.id) {
    isEdit.value = true
    const response = await CollectiveService.getCollectiveById(route.params.id);
    if (response.data) {
      collective.value = response.data
    }
  }
}

const submitForm = async () => {

  if (isEdit.value) {
    await CollectiveService.updateCollective(route.params.id, collective.value)
  } else {
    const response = await CollectiveService.createCollective(collective.value)
    if (response.errors) {
      response.errors.forEach((err: string) => {
        toast.error(err);
      });
      return;
    }
  }
  await router.push('/collectives')
}

onMounted(() => {
  fetchCollective()
})

</script>
