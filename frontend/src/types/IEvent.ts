import type {IEventType} from "@/types/IEventType";

export interface IEvent {
  id: number;
  event_id?: number;
  name: string;
  event_type: IEventType;
  comb_event_var_a?: number;
  comb_event_var_b?: number;
  comb_event_var_c?: number;
  upper_event?: IEvent;
}
