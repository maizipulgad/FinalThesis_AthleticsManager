import type { IAthlete } from "@/types/IAthlete";
import type {ICompetition} from "@/types/ICompetition";
import type {IResult} from "@/types/IResult";

export interface ICompetitionEventAssignment {
  competition_event_id: number;
  event_name: string;
  age_class: string;
  competition_event_competition_athlete_id: number;
  results: IResult[];
}
export interface ICompetitionAthlete {
  competition_athlete_id: number;
  competition: ICompetition;
  athlete: IAthlete;
  BIB_number?: number;
  collective?: string;
  assigned_events?: ICompetitionEventAssignment[];
  resultInput?: number;
  results?: IResult[];

}