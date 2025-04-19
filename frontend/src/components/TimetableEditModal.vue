<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal" tabindex="-1" style="display: block;">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Muuda võistlusala</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="event" class="form-label">Ala</label>
                  <select v-model.number="form.eventId" class="form-select" required @change="console.log('🎯 Selected Event:', form.eventId)">
                    <option v-for="event in events" :key="event.id" :value="Number(event.id)">
                        {{ event.name }}
                    </option>
                  </select>
              </div>

              <div class="mb-3">
                <label for="ageClass" class="form-label">Vanuseklass</label>
                <select v-model.number="form.ageClassId" class="form-select" required @change="console.log('🎯 Selected Age Class:', form.ageClassId)">
                  <option v-for="ageClass in ageClasses" :key="ageClass.id" :value="Number(ageClass.id)">
                        {{ ageClass.name }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label for="startTime" class="form-label">Algusaeg</label>
                <input v-model="form.startTime" type="datetime-local" class="form-control" required />
              </div>

              <div class="mb-3">
                <label for="endTime" class="form-label">Lõppaeg</label>
                <input v-model="form.endTime" type="datetime-local" class="form-control" />
              </div>

              <div class="mb-3">
                <input v-model="form.windMeasurement" type="checkbox" class="form-check-input" id="windMeasurement" />
                <label class="form-check-label" for="windMeasurement">Tuule mõõtmine</label>
              </div>

              <div class="mb-3">
                <input v-model="form.regrouping" type="checkbox" class="form-check-input" id="regrouping" />
                <label class="form-check-label" for="regrouping">Re-grupeerimine</label>
              </div>

              <div class="mb-3">
                <label for="numberOfRounds" class="form-label">Jooksude/gruppide arv</label>
                <input v-model="form.numberOfRounds" type="number" class="form-control" min="1" />
              </div>

              <div class="mb-3">
                <label for="athleteMaxCount" class="form-label">Max Võistlejaid ühe jooksu/grupi kohta</label>
                <input v-model="form.athleteMaxCount" type="number" class="form-control" min="1" />
              </div>

              <div class="mb-3">
                <label for="numberOfAttempts" class="form-label">Katsete arv</label>
                <input v-model="form.numberOfAttempts" type="number" class="form-control" min="1" />
              </div>

              <div class="mb-3">
                <label for="attemptsForFinalists" class="form-label">Finaalkatsete arv</label>
                <input v-model="form.attemptsForFinalists" type="number" class="form-control" min="1" />
              </div>

              <div class="mb-3">
                <label for="comments" class="form-label">Kommentaar</label>
                <input v-model="form.comments" type="text" class="form-control" />
              </div>

              <button type="submit" class="btn btn-primary">Salvesta muudatused</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, watch, onMounted } from 'vue';
import TimetableService from '@/services/TimetableService';
import EventService from '@/services/EventService';
import AgeClassService from '@/services/AgeClassService';
import type { IEvent } from '@/types/IEvent';
import type { IAgeClass } from '@/types/IAgeClass';
import type { ICompetitionEvent } from '@/types/ICompetitionEvent';
import { formatDateForInput } from '@/utils/Helper';


const props = defineProps<{ entry: ICompetitionEvent | null }>();
const emit = defineEmits(['close', 'entry-updated']);

const closeModal = () => {
  emit('close');
};

const form = ref({
  eventId: props.entry?.event?.event_id ?? null,
  ageClassId: props.entry?.age_class?.age_class_id ?? null,
  startTime: props.entry?.start_time ? formatDateForInput(props.entry.start_time) : '',
  endTime: props.entry?.end_time ? formatDateForInput(props.entry.end_time) : '',
  windMeasurement: props.entry?.wind_measurement ?? false,
  numberOfRounds: props.entry?.number_of_rounds ?? 1,
  numberOfAttempts: props.entry?.number_of_attempts ?? 3,
  athleteMaxCount: props.entry?.athlete_max_count ?? 0,
  attemptsForFinalists: props.entry?.finalists_attempt_count ?? 0,
  regrouping: props.entry?.regrouping ?? false,
  comments: props.entry?.comments ?? null,

});

const events = ref<IEvent[]>([]);
const ageClasses = ref<IAgeClass[]>([]);

watch(() => props.entry, (newEntry) => {
  if (newEntry) {

    form.value.eventId = newEntry.event?.event_id ?? newEntry.event?.id ?? null;
    form.value.ageClassId = newEntry.age_class?.age_class_id ?? newEntry.age_class?.id ?? null;

    form.value.startTime = newEntry.start_time ? formatDateForInput(newEntry.start_time) : '';
    form.value.endTime = newEntry.end_time ? formatDateForInput(newEntry.end_time) : '';
    form.value.windMeasurement = newEntry.wind_measurement ?? false;
    form.value.numberOfRounds = newEntry.number_of_rounds ?? 1;
    form.value.numberOfAttempts = newEntry.number_of_attempts ?? 3;
    form.value.athleteMaxCount = newEntry.athlete_max_count ?? 0;
    form.value.regrouping = newEntry.regrouping ?? false;
    form.value.attemptsForFinalists = newEntry.finalists_attempt_count ?? 0;
    form.value.comments = newEntry.comments ?? null;
  }
}, { immediate: true });

onMounted(async () => {

  try {
    const eventsResponse = await EventService.getAllEvents();
    if (eventsResponse.data) events.value = eventsResponse.data;

    const ageClassesResponse = await AgeClassService.getAllAgeClasses();
    if (ageClassesResponse.data) ageClasses.value = ageClassesResponse.data;
  } catch (error) {
    console.error('Error fetching events or age classes:', error);
  }
});

const submitForm = async () => {
  if (!props.entry) return;

  const updatedEntry = {
    eventId: form.value.eventId,
    ageClassId: form.value.ageClassId,
    startTime: new Date(form.value.startTime).toISOString(),
    endTime: form.value.endTime ? new Date(form.value.endTime).toISOString() : null,
    windMeasurement: form.value.windMeasurement,
    numberOfRounds: form.value.numberOfRounds,
    athleteMaxCount: form.value.athleteMaxCount,
    regrouping: form.value.regrouping,
    attemptsForFinalists: form.value.attemptsForFinalists,
    numberOfAttempts: form.value.numberOfAttempts,
    comments: form.value.comments
  };

  try {
    console.log("Props.entry", props.entry.competition_event_id);
    const response = await TimetableService.updateTimetableEntry(props.entry.competition_event_id, updatedEntry);

    if (response.data) {
      emit('entry-updated', response.data);
      emit('close');
    } else {
      alert('Failed to update timetable entry.');
    }
  } catch (error) {
    console.error('Error updating timetable entry:', error);
    alert('An error occurred while updating the entry.');
  }
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

form .mb-3 {
  display: flex;
  align-items: center;
  gap: 1rem;
}

form .form-label {
  width: 150px;
  margin-bottom: 0;
}

form .form-control,
form .form-select {
  width: 10%;
  min-width: 250px;
}


</style>







