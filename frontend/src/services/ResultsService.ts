import apiClient from "./ApiClient";
import type { IResultObject } from "@/types/IResultObject";
import type {IResult} from "@/types/IResult";
import {handleApiError} from "@/utils/apiErrorHandler";

export default class ResultsService {
  static async saveResults(results: IResult[]): Promise<IResultObject<IResult[]>> {
    try {
      const response = await apiClient.post("/results/bulk_update_results/", results);
      return { data: response.data };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async getResultsByRound(roundId: number): Promise<IResultObject<IResult[]>> {
    try {
      const response = await apiClient.get(`/results/?round=${roundId}`);
      if (response.status < 300) {
        const data: IResult[] = response.data.map((r: any) => ({
          result_id: r.result_id,
          competition_event_competition_athlete_id: r.competition_event_competition_athlete,
          round_id: r.round,
          starting_height: r.starting_height,
          result_as_number: parseFloat(r.result_as_number),
          wind_as_number: r.wind_as_number !== null ? parseFloat(r.wind_as_number) : null,
          round_number: r.round_number,
          lane_or_order_number: r.lane_or_order_number,
          attempt_nr: r.attempt_nr,
          points_from_result: r.points_from_result,
          result_as_char: r.result_as_char,
          BIB_number: r.BIB_number,
          athlete: r.athlete,
        }));
        return { data };
      }
      return { errors: [response.status + " " + response.statusText] };
    } catch (error: any) {
        return { errors: handleApiError(error) };
    }
  }

  static async getResultsByCompetitionEvent(eventId: number): Promise<IResultObject<IResult[]>> {
    try {
      const response = await apiClient.get(`/results/?competition_event=${eventId}`);
      if (response.status < 300) {
        return { data: response.data };
      }
      return { errors: [response.status + ' ' + response.statusText] };
      } catch (error: any) {
       return { errors: handleApiError(error) };
    }
  }
}
