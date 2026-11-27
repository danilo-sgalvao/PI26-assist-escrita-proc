// GET /saude é a rota de verificação exposta pela API REST da stack SAM (infra/template.yaml).
// Sem VITE_API_URL não há para onde enviar a verificação: a SPA é servida pelo CloudFront,
// que não encaminha rotas para a API, então a falha é explícita em vez de consultar a própria origem (DEF-001).
export async function verificarSaude(): Promise<void> {
  const api = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
  if (!api) throw new Error('A URL da API não foi configurada (VITE_API_URL).')
  const response = await fetch(`${api}/saude`, { credentials: 'same-origin' })
  if (!response.ok) throw new Error(`A API respondeu com o código ${response.status}.`)
}
