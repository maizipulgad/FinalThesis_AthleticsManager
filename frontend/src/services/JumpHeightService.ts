import apiClient from "./ApiClient";
import type { IJumpHeight } from "@/types/IJumpHeight";
import type { IResultObject } from "@/types/IResultObject";
import {handleApiError} from "@/utils/apiErrorHandler";

export default class JumpHeightService {
  static async getHeightsByRound(roundId: number): Promise<IResultObject<IJumpHeight[]>> {
    try {
      const response = await apiClient.get(`/jump-heights/?round_id=${roundId}`);
      if (response.status < 300) {
        return { data: response.data };
      }
      return { errors: [response.status + " " + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async saveHeights(heights: any): Promise<IResultObject<IJumpHeight[]>> {
    try {
      const response = await apiClient.post("/jump-heights/bulk_create/", heights);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }
}
