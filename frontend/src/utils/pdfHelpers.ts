import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import type { ICompetitionAthlete } from "@/types/ICompetitionAthlete";

export function generateStartListPDF(
  roundName: string,
  competitionEventName: string,
  athletes: ICompetitionAthlete[],
  numberOfAttempts: number,
  windMeasurement: boolean
) {
  const doc = new jsPDF({ orientation: "landscape" });
  const title = `${competitionEventName} - ${roundName} - Stardiprotokoll`;

  doc.text(title, 14, 16);

  const head = [
    ["#", "BIB", "Võistleja", "Sünniaeg", "Kollektiiv", ...generateAttemptHeaders(numberOfAttempts, windMeasurement)]
  ];

  const body = athletes.map((athlete, index) => [
    index + 1,
    athlete.BIB_number ?? "-",
    `${athlete.athlete.first_name} ${athlete.athlete.last_name}`,
    athlete.athlete.date_of_birth ?? "-",
    typeof athlete.collective === "string" ? athlete.collective : athlete.collective?.name ?? "-",
    ...generateAttemptFields(numberOfAttempts, windMeasurement)
  ]);

  autoTable(doc, {
    startY: 22,
    head,
    body,
    theme: "grid",
  });

  doc.save(`${competitionEventName}_${roundName}_Stardiprotokoll.pdf`);
}

export function generateResultsListPDF(
  athletes: ICompetitionAthlete[],
  competitionEventName: string,
  windMeasurement: boolean,
  maxAttempts: number,
  competitionEventId: number
) {
  const doc = new jsPDF({ orientation: "landscape" });
  const title = `${competitionEventName} - Tulemused`;
  doc.text(title, 14, 16);
  const head = [
    ["#", "BIB", "Võistleja", "Kollektiiv", ...generateAttemptHeaders(maxAttempts, windMeasurement), "Parim"]
  ];

  const body = athletes.map((athlete, index) => {
    const assignedEvent = athlete.assigned_events?.find(
      (e) => e.competition_event_id === competitionEventId
    );


    const attemptValues: string[] = [];

    for (let i = 1; i <= maxAttempts; i++) {
      const result = assignedEvent?.results.find(r => r.attempt_nr === i);

      const resultVal = result?.result_as_number ? Number(result.result_as_number).toFixed(2) : "-";
      attemptValues.push(resultVal);

      if (windMeasurement) {
        const wind = result?.wind_as_number;
        const windVal = wind !== null && wind !== undefined
          ? (Number(wind) >= 0 ? `+${Number(wind).toFixed(1)}` : Number(wind).toFixed(1))
          : "-";
        attemptValues.push(windVal);
      }
    }


    return [
      index + 1,
      athlete.BIB_number ?? "-",
      `${athlete.athlete.first_name} ${athlete.athlete.last_name}`,
      typeof athlete.collective === "string" ? athlete.collective : athlete.collective?.name ?? "-",
      ...attemptValues,
      getBestResult(athlete, competitionEventId) ?? "-"
    ];
  });

  autoTable(doc, {
    startY: 22,
    head,
    body,
    theme: "grid",
  });

  doc.save(`${competitionEventName}_Tulemused.pdf`);
}

function generateAttemptHeaders(attempts: number, wind: boolean): string[] {
  const headers: string[] = [];
  for (let i = 1; i <= attempts; i++) {
    headers.push(`Katse ${i}`);
    if (wind) headers.push(`Tuul ${i}`);
  }
  return headers;
}

function generateAttemptFields(attempts: number, wind: boolean): string[] {
  const fields: string[] = [];
  for (let i = 1; i <= attempts; i++) {
    fields.push("");
    if (wind) fields.push("");
  }
  return fields;
}

function getBestResult(athlete: ICompetitionAthlete, competitionEventId: number): string | null {
  const event = athlete.assigned_events?.find(
    (e) => e.competition_event_id === competitionEventId
  );
  if (!event?.results) return null;

  const best = event.results.reduce((max, r) => {
    const num = parseFloat(r.result_as_number);
    return isNaN(num) ? max : Math.max(max, num);
  }, -Infinity);

  return best === -Infinity ? null : best.toFixed(2);
}