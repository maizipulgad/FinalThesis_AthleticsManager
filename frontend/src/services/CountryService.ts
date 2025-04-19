import type { ICountry } from '@/types/ICountry.ts';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";


export default class CountryService {
  static async getAllCountries(): Promise<IResultObject<ICountry[]>> {
    try {
      const response = await apiClient.get('/countries/');
      if (response.status < 300) {
        const data: ICountry[] = response.data.map((country: any) => ({
          id: country.country_id,
          name: country.name,
          abbreviation: country.abbreviation,
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async getCountryById(id: number): Promise<IResultObject<ICountry>> {
    try {
      const response = await apiClient.get(`/countries/${id}/`);
      if (response.status < 300) {
        const data: ICountry = {
          id: response.data.country_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

    static async createCountry(country: ICountry): Promise<IResultObject<ICountry>> {
    try {
      const payload = {
          name: country.name,
          abbreviation: country.abbreviation,
      };
      const response = await apiClient.post('/countries/', payload);
      if (response.status < 300) {
        const data: ICountry = {
          id: response.data.country_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async updateCountry(id: number, country: ICountry): Promise<IResultObject<ICountry>> {
    try {
      const payload = {
          name: country.name,
          abbreviation: country.abbreviation,
      };
      const response = await apiClient.patch(`/countries/${id}/`, payload);
      if (response.status < 300) {
        const data: ICountry = {
          id: response.data.country_id,
          name: response.data.name,
          abbreviation: response.data.abbreviation,
        };
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

}
