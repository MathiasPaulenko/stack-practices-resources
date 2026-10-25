const now = new Date();
console.log(now.toISOString());                                   // 2026-06-10T14:30:00.000Z
console.log(new Intl.DateTimeFormat('es-ES', { timeZone: 'Europe/Madrid', dateStyle: 'short', timeStyle: 'short' }).format(now));
console.log(new Intl.DateTimeFormat('en-US', { dateStyle: 'short' }).format(now));
