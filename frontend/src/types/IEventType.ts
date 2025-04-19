export interface IEventType {
  id: number;
  name:string;
  upper_event_type?: IEventType;
}
