import type { IAgeClass } from '@/types/IAgeClass';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";

export default class AgeClassService {
  static async getAllAgeClasses(): Promise<IResultObject<IAgeClass[]>> {
    try {
      const response = await apiClient.get('/age-classes/');
      if (response.status < 300) {
        const data: IAgeClass[] = response.data.map((age_class: any) => ({
          id: age_class.age_class_id,
          name: age_class.name,
          maximum_age: age_class.maximum_age,
          minimum_age: age_class.minimum_age,
          sex: age_class.sex
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async getAgeClassById(id: number): Promise<IResultObject<IAgeClass>> {
    try {
      const response = await apiClient.get(`/age-classes/${id}/`);
      if (response.status < 300) {
        return { data: response.data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async createAgeClass(ageclass: IAgeClass): Promise<IResultObject<IAgeClass>> {
    try {
      const payload = {
        name: ageclass.name,
        minimum_age: ageclass.minimum_age,
        maximum_age: ageclass.maximum_age,
        sex: ageclass.sex,
      };
      const response = await apiClient.post('/age-classes/', payload);
      if (response.status < 300) {
        return { data: response.data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async updateAgeClass(id: number, ageclass: IAgeClass): Promise<IResultObject<IAgeClass>> {
    try {

      const response = await apiClient.put(`/age-classes/${id}/`, ageclass);
      if (response.status < 300) {
        return {data: response.data};
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }
}