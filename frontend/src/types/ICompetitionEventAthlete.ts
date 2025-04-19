import type {ICompetitionEvent} from "@/types/ICompetitionEvent";
import type {ICompetitionAthlete} from "@/types/ICompetitionAthlete";

export interface ICompetitionEventAthlete {
  competition_event_athlete_id?: number;
  competition_event?: ICompetitionEvent;
  competition_athlete?: ICompetitionAthlete;
  competition_event_id?: number,
  competition_athlete_id?: number,
}