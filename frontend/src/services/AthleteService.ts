import type { IAthlete } from '@/types/IAthlete';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";


export default class AthleteService {
  static async getAllAthletes(): Promise<IResultObject<IAthlete[]>> {
    try {
      const response = await apiClient.get('/athletes/');
      if (response.status < 300) {
        const data: IAthlete[] = response.data.map((athlete: any) => ({
          id: athlete.athlete_id,
          firstName: athlete.first_name,
          lastName: athlete.last_name,
          dateOfBirth: athlete.date_of_birth,
          sex: athlete.sex,
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getAthleteById(id: number): Promise<IResultObject<IAthlete>> {
    try {
      const response = await apiClient.get(`/athletes/${id}/`);
      if (response.status < 300) {
        const data: IAthlete = {
          id: response.data.athlete_id,
          firstName: response.data.first_name,
          lastName: response.data.last_name,
          dateOfBirth: response.data.date_of_birth,
          sex: response.data.sex
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async createAthlete(athlete: IAthlete): Promise<IResultObject<IAthlete>> {
    try {
      const payload = {
        first_name: athlete.firstName,
        last_name: athlete.lastName,
        date_of_birth: athlete.dateOfBirth,
        sex: athlete.sex,
      };
      const response = await apiClient.post('/athletes/', payload);
      if (response.status < 300) {
        const data: IAthlete = {
          id: response.data.athlete_id,
          firstName: response.data.first_name,
          lastName: response.data.last_name,
          dateOfBirth: response.data.date_of_birth,
          sex: response.data.sex,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async updateAthlete(id: number, athlete: IAthlete): Promise<IResultObject<IAthlete>> {
    try {
      const payload = {
        first_name: athlete.firstName,
        last_name: athlete.lastName,
        date_of_birth: athlete.dateOfBirth,
        sex: athlete.sex
      };
      const response = await apiClient.patch(`/athletes/${id}/`, payload);
      if (response.status < 300) {
        const data: IAthlete = {
          id: response.data.athlete_id,
          firstName: response.data.first_name,
          lastName: response.data.last_name,
          dateOfBirth: response.data.date_of_birth,
          sex: response.data.sex
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

}
