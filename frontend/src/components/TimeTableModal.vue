<template>
    <div class="modal-overlay" @click="closeModal">
      <div class="modal" tabindex="-1" style="display: block;">
        <div class="modal-dialog" @click.stop>
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Lisa võistlusala</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="submitForm">
                <div class="mb-3">
                  <label for="event" class="form-label">Ala</label>
                  <select v-model="form.eventId" class="form-select" required>
                    <option v-for="event in events" :key="event.id" :value="event.id">
                      {{ event.name }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="ageClass" class="form-label">Vanuseklass</label>
                  <select v-model="form.ageClassId" @change="logAgeClass" class="form-select" required>
                    <option v-for="ageClass in ageClasses" :key="ageClass.id" :value="ageClass.id">
                      {{ ageClass.name }}
                    </option>
                  </select>
                </div>

                <div class="mb-3">
                  <label for="startTime" class="form-label">Algusaeg</label>
                  <input
                    v-model="form.startTime"
                    type="datetime-local"
                    class="form-control"
                    required
                  />
                </div>

                <button type="submit" class="btn btn-primary">Lisa</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
  
  <script setup lang="ts">
import { ref, onMounted } from 'vue';
import TimetableService from '@/services/TimetableService';
import EventService from '@/services/EventService';
import AgeClassService from '@/services/AgeClassService';
import type {IEvent} from "@/types/IEvent";
import type {IAgeClass} from "@/types/IAgeClass";
import {useHeaderStore} from "@/stores/header";

const headerStore = useHeaderStore();
const emit = defineEmits(['close', 'entry-added']);

const form = ref({
  eventId: 0,
  ageClassId: 0,
  startTime: '',
});

const closeModal = () => {
  emit('close');
};

const events = ref<IEvent[]>([]);
const ageClasses = ref<IAgeClass[]>([]);

// Fetch events and age classes
onMounted(async () => {
  const eventsResponse = await EventService.getAllEvents();
  if (eventsResponse.data) events.value = eventsResponse.data;

  const ageClassesResponse = await AgeClassService.getAllAgeClasses();
  if (ageClassesResponse.data) ageClasses.value = ageClassesResponse.data;
});

const submitForm = async () => {

  const timetableEntry = {
    competitionId: headerStore.selectedCompetitionId,
    eventId: form.value.eventId,
    ageClassId: form.value.ageClassId,
    startTime: form.value.startTime,
  };

  const response = await TimetableService.addTimetableEntry(timetableEntry);

  if (response.data) {
    emit('entry-added', response.data);
    emit('close');
  } else {
    alert('Failed to add timetable entry.');
  }
};

const logAgeClass = () => {
  console.log("Selected Age Class ID:", form.value.ageClassId);
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-dialog {
  max-width: 500px;
}
</style>
