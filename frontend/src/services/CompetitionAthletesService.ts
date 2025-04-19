import apiClient from "./ApiClient";
import type { ICompetitionAthlete } from "@/types/ICompetitionAthlete";
import type { IResultObject } from "@/types/IResultObject";
import type {ICompetitionEventAthlete} from "@/types/ICompetitionEventAthlete";
import {handleApiError} from "@/utils/apiErrorHandler";

export default class CompetitionAthletesService {
  static async getAthletesByCompetition(competitionId: number): Promise<IResultObject<ICompetitionAthlete[]>> {
    try {
      const response = await apiClient.get<ICompetitionAthlete[]>(`competition-athletes/?competition_id=${competitionId}`);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async getAthleteEventsByCompetitionAthlete(competitionAthleteId: number): Promise<IResultObject<ICompetitionAthlete>> {
    try {
      const response = await apiClient.get<ICompetitionAthlete[]>(`competition-athletes/?competition_athlete_id=${competitionAthleteId}`);
      return { data: response.data[0] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getAthletesByEvent(competitionEventId: number): Promise<IResultObject<ICompetitionAthlete[]>> {
    try {
      const response = await apiClient.get<ICompetitionAthlete[]>(`competition-athletes/?competition_event_id=${competitionEventId}`);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async addCompetitionAthlete(entry: ICompetitionAthlete): Promise<IResultObject<ICompetitionAthlete>> {
    try {
      const response = await apiClient.post<ICompetitionAthlete>(`competition-athletes/`, entry);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async createOrGetCompetitionAthlete(competitionId: number, athleteId: number, bibNumber: number, collectiveId: number | null): Promise<ICompetitionAthlete | null> {
    try {
      const payload: Record<string, any> = { competition_id: competitionId, athlete_id: athleteId , BIB_number: bibNumber};
      if (collectiveId !== null) {
        payload.collective_id = collectiveId;
      }
      const response = await apiClient.post<ICompetitionAthlete>(`competition-athletes/`, payload);
      return response.data;
    } catch (error: any) {
      console.error("Failed to create/get CompetitionAthlete:", error);
      return null;
    }
  }


  static async addAthleteToEvent(entry: ICompetitionEventAthlete): Promise<IResultObject<ICompetitionEventAthlete>> {
    try {
      const response = await apiClient.post<ICompetitionEventAthlete>(`competition-event-athletes/`, entry);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async removeAthleteFromEvent(competitionEventAthleteId: number): Promise<boolean> {
    try {
      const response = await apiClient.delete(`competition-event-athletes/${competitionEventAthleteId}/`);
      return response.status === 204;
    } catch (error: any) {
      console.error("Failed to remove athlete from event:", error);
      return false;
    }
  }

  static async assignRoundsAndLanes(data: any) {
    try {
      const response = await apiClient.post("competition-athletes/assign-rounds-lanes/", data);
      return response.status === 200;
    } catch (error) {
      console.error("Failed to assign rounds/lanes:", error);
      return false;
    }
  }


}
