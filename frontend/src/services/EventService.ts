import type { IEvent } from '@/types/IEvent';
import type { IResultObject } from '@/types/IResultObject';
import apiClient from './ApiClient';
import {handleApiError} from "@/utils/apiErrorHandler";


export default class AthleteService {
  static async getAllEvents(): Promise<IResultObject<IEvent[]>> {
    try {
      const response = await apiClient.get('/events/');
      if (response.status < 300) {
        const data: IEvent[] = response.data.map((event: any) => ({
          id: event.event_id,
          name: event.name,
        }));
        return { data };
      }
      return { errors: [response.status.toString() + ' ' + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }
}
