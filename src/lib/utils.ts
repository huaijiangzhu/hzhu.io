import strftime from "strftime";

export function formatDate(date: Date | string): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return strftime("%B %Y", d);
}

export function formatFullDate(date: Date | string): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return strftime("%B %d, %Y", d);
}
