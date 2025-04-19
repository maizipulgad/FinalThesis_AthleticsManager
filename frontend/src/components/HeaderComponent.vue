<template>
  <div class="sticky-lg-top">
  <header class="d-flex justify-content-between align-items-center p-3 border-bottom">
    <h3 class="mb-0">Athletics Manager "M403"</h3>
    <nav>
      <ul class="d-flex list-unstyled mb-0">
        <li v-if="authStore.userRoles.includes('EKJL') ?? false" class="me-3">
          <router-link to="/athletes" class="text-decoration-none">
            Võistlejad
          </router-link>
        </li>
        <li class="me-3">
          <router-link to="/competitions" class="text-decoration-none">
            Võistlused
          </router-link>
        </li>
        <li class="me-3">
          <router-link to="/age-classes" class="text-decoration-none">
            Vanuseklassid
          </router-link>
        </li>
        <li class="me-3">
          <router-link to="/collectives" class="text-decoration-none">
            Kollektiivid
          </router-link>
        </li>
        <li class="me-3">
          <router-link to="/competition-athletes" class="text-decoration-none">
            LISA Võistleja võistlusele
          </router-link>
        </li>

      </ul>
    </nav>
    <div class="d-flex align-items-center justify-content-end gap-2">
    <select v-model="selectedCompetitionId" @change="onCompetitionChange" class="form-select d-inline-block me-3">
      <option disabled value="null">Vali võistlus</option>

      <option
        v-for="competition in competitions.filter((comp) => comp.active)"
        :key="competition.id"
        :value="competition.id"
      >
        {{ competition.name }}
      </option>
    </select>
      <button class="btn btn-outline-secondary" @click="logout">Logout</button>
    </div>
  </header>
  </div>
</template>


<script setup lang="ts">
import { onMounted, ref} from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import CompetitionService from '@/services/CompetitionService';
import type { ICompetition } from '@/types/ICompetition';
import { useHeaderStore } from '@/stores/header';

const competitions = ref<ICompetition[]>([]);
const selectedCompetitionId = ref<number | null>(null);
const router = useRouter();
const authStore = useAuthStore();
const headerStore = useHeaderStore();

onMounted(async () => {
  try {
    const res = await CompetitionService.getAllCompetitions();
    if (res.data) {
      competitions.value = res.data;

      const savedCompetitionId = localStorage.getItem("selectedCompetitionId");

      if (savedCompetitionId) {
        const parsedCompetitionId = Number(savedCompetitionId);

        if (competitions.value.some(c => c.id === parsedCompetitionId)) {
          selectedCompetitionId.value = parsedCompetitionId;
          headerStore.setSelectedCompetition(parsedCompetitionId);
        }
      }
    }
  } catch (error) {
    console.error("Error fetching competitions:", error);
  }
});

const onCompetitionChange = () => {
  const selectedCompetition = competitions.value.find(
    (competition) => competition.id === selectedCompetitionId.value
  );

  headerStore.setSelectedCompetition(selectedCompetitionId.value);

  if (selectedCompetitionId.value) {
    localStorage.setItem("selectedCompetitionId", selectedCompetitionId.value.toString());
  } else {
    localStorage.removeItem("selectedCompetitionId");
  }
};

const logout = () => {
  authStore.clear();
  router.push('/login');
};
</script>

<style scoped>
header {
  background-color: var(--bs-light);
}
</style>
