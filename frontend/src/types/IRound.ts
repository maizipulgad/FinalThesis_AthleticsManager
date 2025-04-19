export interface IRound {
  id: number;
  name?: string;
  roundNumber: number;
  competitionEventId: number;
  startTime: string;
  endTime?: string;
  upperRoundId?: number;
  numberOfSubRounds?: number;
  numberOfMaxAthletes?: number;
  printout?: string;
}
