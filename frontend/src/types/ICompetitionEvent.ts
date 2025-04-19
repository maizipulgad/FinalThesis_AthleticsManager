import type {ICompetition} from "@/types/ICompetition";
import type {IEvent} from "@/types/IEvent";
import type {IAgeClass} from "@/types/IAgeClass";
import type {IRound} from "@/types/IRound";

export interface ICompetitionEvent {
  id: number;
  competition_event_id: number,
  competition: ICompetition;
  event: IEvent;
  age_class: IAgeClass;
  event_type_name?: string,
  number_of_attempts?: number,
  start_time: string;
  end_time?: string;
  regrouping: boolean;
  regrouping_done: boolean;
  finalists_attempt_count: number;
  wind_measurement?: boolean;
  number_of_rounds?: number;
  athlete_max_count?: number;
  comments?: string;
  rounds?: IRound[];
}