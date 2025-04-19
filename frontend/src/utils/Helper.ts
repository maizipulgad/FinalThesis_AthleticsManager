export const formatDate = (dateString: string): string => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('et-EE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatDateShort = (dateString: string): string => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const formatDateDOB = (dateString: string): string => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('et-EE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

export function formatDateForInput(isoString: string): string {
  if (!isoString) return '';

  const date = new Date(isoString);

  // Get date components
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${year}-${month}-${day}T${hours}:${minutes}`; // Format for datetime-local input
}

export function parseTimeStringToSeconds(timeStr: string): number | null {
  if (!timeStr) return null;

  const parts = timeStr.split(':').map(p => p.trim());
  let total = 0;

  try {
    if (parts.length === 3) {
      // hh:mm:ss.xxx
      total += parseInt(parts[0]) * 3600; // hours
      total += parseInt(parts[1]) * 60;   // minutes
      total += parseFloat(parts[2]);      // seconds.xxx
    } else if (parts.length === 2) {
      // mm:ss.xxx
      total += parseInt(parts[0]) * 60;
      total += parseFloat(parts[1]);
    } else if (parts.length === 1) {
      // ss.xxx
      total += parseFloat(parts[0]);
    }
    return Math.round(total * 1000) / 1000; // round to thousandths
  } catch (e) {
    console.error("Invalid time string:", timeStr);
    return null;
  }
}


function formatSecondsToTimeString(
  totalSeconds: number,
  precision: "hundredths" | "thousandths" = "thousandths"
): string {
  if (isNaN(totalSeconds)) return "-";

  const rounded =
    precision === "hundredths"
      ? Math.ceil(totalSeconds * 100) / 100
      : totalSeconds;

  const decimals = precision === "hundredths" ? 2 : 3;

  const hours = Math.floor(rounded / 3600);
  const minutes = Math.floor((rounded % 3600) / 60);
  const seconds = (rounded % 60).toFixed(decimals);

  const pad = (n: number) => n.toString().padStart(2, "0");

  if (hours > 0) {
    return `${pad(hours)}:${pad(minutes)}:${seconds.padStart(decimals + 3, "0")}`;
  } else if (minutes > 0) {
    return `${pad(minutes)}:${seconds.padStart(decimals + 3, "0")}`;
  } else {
    return seconds;
  }
}

export function formatSecondsToTimeStringHundredths(seconds: number): string {
  return formatSecondsToTimeString(seconds, "hundredths");

}

export function formatSecondsToTimeStringThousandths(seconds: number): string {
  return formatSecondsToTimeString(seconds, "thousandths");

}