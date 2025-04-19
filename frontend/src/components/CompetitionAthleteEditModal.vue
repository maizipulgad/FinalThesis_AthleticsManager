<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-dialog" @click.stop>
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Muuda võistleja alasid</h5>
          <button type="button" class="btn-close top-right" @click="closeModal"></button>
        </div>

          <h3 class="modal-title-name">Edit Assigned Events for {{ athlete?.athlete.first_name }} {{ athlete?.athlete.last_name }}</h3>

        <div v-if="athlete" class="event-list">
          <label v-for="event in athlete.assigned_events" :key="event.competition_event_competition_athlete_id" class="event-checkbox">
            <input type="checkbox" v-model="selectedEventsToRemove" :value="event.competition_event_competition_athlete_id" />
            {{ event.event_name }} ({{ event.age_class }})
          </label>
        </div>

        <div class="modal-buttons">
          <button class="btn btn-danger" @click="removeSelectedEvents">Save Changes</button>
          <button class="btn btn-secondary cancel-btn" @click="$emit('close')">Cancel</button>
        </div>


      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import CompetitionAthletesService from "@/services/CompetitionAthletesService";
import { useToast } from "vue-toastification";
import {computed, ref, watch} from "vue";
import type {ICompetitionAthlete} from "@/types/ICompetitionAthlete";

const props = defineProps<{
  athlete: ICompetitionAthlete | null;
}>();

const assignedEvents = computed(() => props.athlete?.assigned_events || []);

const emit = defineEmits(['close', 'entry-updated']);

const toast = useToast();
const selectedEventsToRemove = ref([]);

watch(() => props.athlete, (newAthlete) => {
  if (newAthlete) {
    selectedEventsToRemove.value = [];
  }
}, { immediate: true });

const closeModal = () => {
  emit('close');
};
const removeSelectedEvents = async () => {
  if (selectedEventsToRemove.value.length === 0) {
    toast.warning("Please select at least one event to remove.");
    return;
  }

  try {
    for (const eventId of selectedEventsToRemove.value) {
      const success = await CompetitionAthletesService.removeAthleteFromEvent(eventId);

      if (!success) {
        toast.error(`Failed to remove event ID: ${eventId}`);
        return;
      }
    }

    toast.success("Selected events removed successfully!");
    emit("entry-updated"); // Refresh data
    emit("close"); // Close modal
  } catch (error) {
    toast.error("Failed to remove events. Please try again.");
    console.error(error);
  }
};


</script>


<style scoped>
.modal-overlay {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.btn-close.top-right {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.modal-title-name {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

.event-list {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Adds space between checkboxes */
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 🔹 Aligns "Cancel" button to the right */
.cancel-btn {
  margin-left: auto;
}
</style>







