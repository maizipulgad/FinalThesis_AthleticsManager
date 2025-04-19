export interface ITimetableEntry {
  competitionId: number | null;
  eventId: number | null;
  ageClassId: number | null;
  startTime: string;
  numberOfRounds?: number | null;
  athleteMaxCount?: number | null;
  windMeasurement?: boolean;
  regrouping?: boolean;
  comments?: string | null;
  attemptsForFinalists: number;
  numberOfAttempts: number;
}


