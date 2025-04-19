export function handleApiError(error: any): string[] {
  if (error.response?.data) {
    const raw = error.response.data;

    const messages = Object.entries(raw).flatMap(([field, errs]) => {
      if (Array.isArray(errs)) {
        return errs;
      } else if (typeof errs === 'string') {
        return [errs];
      }
      return [];
    });

    return messages.length > 0 ? messages : ['An unknown error occurred.'];
  }
  return ['A network error occurred. Please try again.'];
}
