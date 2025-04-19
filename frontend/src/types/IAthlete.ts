import type {ICompetitionEvent} from "@/types/ICompetitionEvent";
import type {ICollective} from "@/types/ICollective";

export interface IAthlete {
  id: number;
  firstName: string;
  lastName: string;
  dateOfBirth?: string;
  sex: string;
  collective?: ICollective;
  assigned_events?: ICompetitionEvent[];
}
