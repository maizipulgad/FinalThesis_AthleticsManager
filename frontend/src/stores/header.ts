import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useHeaderStore = defineStore('header', () => {
  const selectedCompetitionId = ref<number | null>(null);

  // Set the selected competition ID
  const setSelectedCompetition = (competitionId: number | null) => {
    selectedCompetitionId.value = competitionId;
  };

  return {
    selectedCompetitionId,
    setSelectedCompetition,
  };
});
