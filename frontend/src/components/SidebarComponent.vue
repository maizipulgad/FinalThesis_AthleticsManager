<template>
  <aside class="bg-light p-3 border-end" style="width: 320px">
    <nav>
      <ul class="list-unstyled">
        <li v-for="competition_event in timetableSorted" :key="competition_event.id" class="d-flex justify-content-between align-items-center list-group-item">
          <router-link :to="{ name: 'CompetitionEventAthletes', params: { competition_event_id: competition_event.competition_event_id } }" class="competition-event-link">
            {{ formatDateShort(competition_event.start_time) }} {{ competition_event.age_class.sex }} {{ competition_event.event.name }} {{ competition_event.comments }}
          </router-link>

          <button @click="openEditModal(competition_event)" class="btn btn-sm btn-link text-end">Muuda</button>

        </li>
      </ul>
      <button @click="showModal = true" class="btn btn-primary btn-sm">[LISA]</button>
      <TimeTableModal v-if="showModal" @close="showModal = false" @entry-added="fetchTimetable" />

      <TimetableEditModal v-if="isEditModalOpen && selectedEntry" :entry="selectedEntry" @close="isEditModalOpen = false" @entry-updated="fetchTimetable" />
    </nav>
  </aside>
</template>

<style scoped>
aside {
  height: 100vh;
}
</style>


<script setup lang="ts">
import {ref, onMounted, watch, computed} from 'vue';
import TimetableService from '@/services/TimetableService';
import { useHeaderStore } from '@/stores/header';
import { formatDateShort } from '@/utils/Helper';
import type { ICompetitionEvent } from "@/types/ICompetitionEvent";
import TimeTableModal from '@/components/TimeTableModal.vue';
import TimetableEditModal from './TimetableEditModal.vue';


const timetable = ref<ICompetitionEvent[]>([]);
const headerStore = useHeaderStore();
const showModal = ref(false);
const isEditModalOpen = ref(false);
const selectedEntry = ref<ICompetitionEvent | null>(null);


const fetchTimetable = async () => {
  if (headerStore.selectedCompetitionId) {
    const response = await TimetableService.getTimetableByCompetition(headerStore.selectedCompetitionId);
    if (response.data) {
      timetable.value = response.data;
    }
  } else {
    timetable.value = [];
  }
};

const timetableSorted = computed(() => {
  return [...timetable.value].sort((a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime());
});

// Watch for competition changes and fetch timetable accordingly
watch(() => headerStore.selectedCompetitionId, fetchTimetable);

const openEditModal = (entry: ICompetitionEvent) => {
  selectedEntry.value = entry;
  isEditModalOpen.value = true;
};

onMounted(() => {
  if (headerStore.selectedCompetitionId) {
    fetchTimetable();
  }
});
</script>