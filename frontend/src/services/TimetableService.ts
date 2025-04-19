import type { ICompetitionEvent } from '@/types/ICompetitionEvent';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import type { ITimetableEntry } from "@/types/ITimetableEntry";
import type {IRound} from "@/types/IRound";
import {handleApiError} from "@/utils/apiErrorHandler";


export default class TimetableService {

  static async getTimetableByCompetition(competitionId: number): Promise<IResultObject<ICompetitionEvent[]>> {
    try {
      const response = await apiClient.get<ICompetitionEvent[]>(`timetable/?competition_id=${competitionId}`);
      return {data: response.data};
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getTimetableEntryById(entryId: number): Promise<IResultObject<ICompetitionEvent>> {
    try {
      const response = await apiClient.get<ICompetitionEvent>(`timetable/${entryId}/`);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async addTimetableEntry(entry: ITimetableEntry): Promise<IResultObject<ICompetitionEvent>> {
    try {
      const payload = {
        competition_id: entry.competitionId,
        event_id: entry.eventId,
        age_class_id: entry.ageClassId,
        start_time: entry.startTime,
        number_of_rounds: entry.numberOfRounds,
        athlete_max_count: entry.athleteMaxCount,
        wind_measurement: entry.windMeasurement,
      };
      const response = await apiClient.post<ICompetitionEvent>(`timetable/`, payload);
      return { data: response.data };  // Response contains the full ICompetitionEvent object
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async updateTimetableEntry(entryId: number, updatedEntry: Partial<ITimetableEntry>): Promise<IResultObject<ICompetitionEvent>> {
    try {
        const payload = {
        competition_id: updatedEntry.competitionId,
        event_id: updatedEntry.eventId,
        age_class_id: updatedEntry.ageClassId,
        start_time: updatedEntry.startTime,
        number_of_rounds: updatedEntry.numberOfRounds,
        athlete_max_count: updatedEntry.athleteMaxCount,
        wind_measurement: updatedEntry.windMeasurement,
          comments: updatedEntry.comments,
          attempts_for_finalists: updatedEntry.attemptsForFinalists,
          regrouping: updatedEntry.regrouping,
          number_of_attempts: updatedEntry.numberOfAttempts
      };
      const response = await apiClient.put<ICompetitionEvent>(`timetable/${entryId}/`, payload);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async markRegroupingDone(competitionEventId: number): Promise<IResultObject<ICompetitionEvent>> {
    try{
      const response = await apiClient.patch(`/timetable/${competitionEventId}/`, {
      regrouping_done: true
    });
          return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async getRoundsByCompetitionEvent(competitionEventId: number): Promise<IResultObject<IRound[]>> {
    try {
        const response = await apiClient.get<IRound[]>(`rounds/?competition_event_id=${competitionEventId}`);
        return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
}
}
