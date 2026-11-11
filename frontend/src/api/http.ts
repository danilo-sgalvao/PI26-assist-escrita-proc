export async function getJson<T>(path: `/api/${string}`): Promise<T> {
  const response = await fetch(path, {
    credentials: 'same-origin',
    headers: { Accept: 'application/json' },
  })

  if (!response.ok) {
    throw new Error(`A API respondeu com o código ${response.status}.`)
  }

  return response.json() as Promise<T>
}

export async function verificarSaude(): Promise<void> {
  const response = await fetch('/api/health', { credentials: 'same-origin' })
  if (!response.ok) {
    throw new Error(`A API respondeu com o código ${response.status}.`)
  }
}
