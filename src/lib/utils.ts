import strftime from "strftime";

const utc = strftime.utc();

export function formatDate(date: Date | string): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return utc("%B %Y", d);
}

export function formatFullDate(date: Date | string): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return utc("%B %d, %Y", d);
}
