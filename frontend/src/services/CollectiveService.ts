import type { ICollective } from '@/types/ICollective';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import { handleApiError } from '@/utils/apiErrorHandler';


export default class CollectiveService {
  static async getAllCollectives(): Promise<IResultObject<ICollective[]>> {
    try {
      const response = await apiClient.get('/collectives/');
      if (response.status < 300) {
        const data: ICollective[] = response.data.map((collective: any) => ({
          id: collective.collective_id,
          name: collective.name,
          abbreviation: collective.abbreviation,
          additionalInformation: collective.additional_information,
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getCollectiveById(id: number): Promise<IResultObject<ICollective>> {
    try {
      const response = await apiClient.get(`/collectives/${id}/`);
      if (response.status < 300) {
        const data: ICollective = {
          id: response.data.collective_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
          additionalInformation: response.data.additional_information,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async createCollective(collective: ICollective): Promise<IResultObject<ICollective>> {
    try {
      const payload = {
          name: collective.name,
          abbreviation: collective.abbreviation,
          additional_information: collective.additionalInformation,
      };
      const response = await apiClient.post('/collectives/', payload);
      if (response.status < 300) {
        const data: ICollective = {
          id: response.data.collective_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
          additionalInformation: response.data.additionalInformation,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };

      } catch (error: any) {
        return { errors: handleApiError(error) };
      }
  }

  static async updateCollective(id: number, collective: ICollective): Promise<IResultObject<ICollective>> {
    try {
      const payload = {
          name: collective.name,
          abbreviation: collective.abbreviation,
          additional_information: collective.additionalInformation,
      };
      const response = await apiClient.patch(`/collectives/${id}/`, payload);
      if (response.status < 300) {
        const data: ICollective = {
          id: response.data.collective_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
          additionalInformation: response.data.additionalInformation,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

}
