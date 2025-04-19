import type { ICompetition } from '@/types/ICompetition';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";


export default class CompetitionService {
    static async getAllCompetitions(): Promise<IResultObject<ICompetition[]>> {
    try {
      const response = await apiClient.get('/competitions/');
      if (response.status < 300) {
        const data: ICompetition[] = response.data.map((competition: any) => ({
          id: competition.competition_id,
          name: competition.name,
          comments: competition.comments,
          active: competition.active,
          startDate: competition.start_time,
          endDate: competition.end_time,
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getCompetitionById(id: number): Promise<IResultObject<ICompetition>> {
    try {
      const response = await apiClient.get(`/competitions/${id}/`);
      if (response.status < 300) {
        const data: ICompetition = {
          id: response.data.competition_id,
          name: response.data.name,
          active: response.data.active,
          comments: response.data.comments,
          startDate: response.data.start_time,
          endDate: response.data.end_time
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async createCompetition(competition: ICompetition): Promise<IResultObject<ICompetition>> {
    try {
      const payload = {
          name: competition.name,
          active: competition.active,
          comments: competition.comments,
          start_time: competition.startDate,
          end_time: competition.endDate,
      };
      const response = await apiClient.post('/competitions/', payload);
      if (response.status < 300) {
        const data: ICompetition = {
          id: response.data.competition_id,
          name: response.data.name,
          comments: response.data.comments,
          active: response.data.active,
          startDate: response.data.startDate,
          endDate: response.data.endDate
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async updateCompetition(id: number, competition: ICompetition): Promise<IResultObject<ICompetition>> {
    try {
      const payload = {
          name: competition.name,
          active: competition.active,
          comments: competition.comments,
          start_time: competition.startDate,
          end_time: competition.endDate,
      };
      const response = await apiClient.patch(`/competitions/${id}/`, payload);
      if (response.status < 300) {
        const data: ICompetition = {
          id: response.data.competition_id,
          name: response.data.name,
          comments: response.data.comments,
          active: response.data.active,
          startDate: response.data.startDate,
          endDate: response.data.endDate
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }
}
