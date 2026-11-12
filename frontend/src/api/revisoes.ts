export type Sessao = { idToken: string; accessToken: string; sub: string }
export type Desafio = { challengeSession: string; username: string }
export type Revisao = { id_producao: string; status: string; sugestoes: string[] }
const api = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
export async function entrar(email: string, senha: string): Promise<Sessao | Desafio> {
  const region = import.meta.env.VITE_COGNITO_REGION, clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
  if (!region || !clientId) throw new Error('O acesso ainda não foi configurado. Procure a equipe responsável.')
  const response = await fetch(`https://cognito-idp.${region}.amazonaws.com/`, { method: 'POST', headers: { 'Content-Type': 'application/x-amz-json-1.1', 'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth' }, body: JSON.stringify({ ClientId: clientId, AuthFlow: 'USER_PASSWORD_AUTH', AuthParameters: { USERNAME: email.trim(), PASSWORD: senha } }) })
  const data = await response.json()
  if (!response.ok) throw new Error('Não foi possível entrar. Verifique seus dados e tente novamente.')
  if (data.ChallengeName === 'NEW_PASSWORD_REQUIRED' && data.Session) return { challengeSession: data.Session, username: data.ChallengeParameters?.USER_ID_FOR_SRP || email.trim() }
  if (data.ChallengeName) throw new Error('Sua conta requer uma etapa adicional de acesso. Procure a equipe responsável.')
  return sessaoDe(data.AuthenticationResult)
}
function sessaoDe(resultado: { IdToken: string; AccessToken: string }): Sessao {
  const { IdToken: idToken, AccessToken: accessToken } = resultado || {}
  if (!idToken || !accessToken) throw new Error('Não foi possível concluir o acesso.')
  const parte = idToken.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
  const sub = JSON.parse(atob(parte.padEnd(Math.ceil(parte.length / 4) * 4, '='))).sub
  if (!sub) throw new Error('Não foi possível concluir o acesso.')
  return { idToken, accessToken, sub }
}
export async function definirSenha(desafio: Desafio, novaSenha: string): Promise<Sessao> {
  const data = await cognitoSenha(desafio, novaSenha)
  return sessaoDe(data.AuthenticationResult)
}
async function cognitoSenha(desafio: Desafio, novaSenha: string) {
  const region = import.meta.env.VITE_COGNITO_REGION, clientId = import.meta.env.VITE_COGNITO_CLIENT_ID
  const response = await fetch(`https://cognito-idp.${region}.amazonaws.com/`, { method: 'POST', headers: { 'Content-Type': 'application/x-amz-json-1.1', 'X-Amz-Target': 'AWSCognitoIdentityProviderService.RespondToAuthChallenge' }, body: JSON.stringify({ ClientId: clientId, ChallengeName: 'NEW_PASSWORD_REQUIRED', Session: desafio.challengeSession, ChallengeResponses: { USERNAME: desafio.username, NEW_PASSWORD: novaSenha } }) })
  if (!response.ok) throw new Error('Não foi possível definir a senha. Verifique os requisitos de segurança e tente novamente.')
  const data = await response.json()
  if (data.ChallengeName) throw new Error('Sua conta requer uma etapa adicional de acesso. Procure a equipe responsável.')
  return data
}

async function request<T>(path: string, token: string, options: RequestInit = {}): Promise<T> {
  if (!api) throw new Error('A conexão com a API ainda não foi configurada.')
  const response = await fetch(`${api}${path}`, { ...options, headers: { 'Content-Type': 'application/json', Authorization: token, ...options.headers } })
  if (!response.ok) throw new Error(response.status === 401 || response.status === 403 ? 'Sua sessão expirou ou você não tem acesso. Entre novamente.' : 'Não foi possível concluir a operação. Tente novamente.')
  return response.json() as Promise<T>
}
export const enviar = (texto: string, token: string) => request<Revisao>('/producoes', token, { method: 'POST', body: JSON.stringify({ texto, consentimento: true }) })
export const consultar = (id: string, token: string) => request<Revisao>(`/producoes/${encodeURIComponent(id)}`, token)
export function conectar(token: string): WebSocket | null {
  const endpoint = import.meta.env.VITE_WEBSOCKET_URL
  if (!endpoint) return null
  const url = new URL(endpoint)
  if (url.protocol !== 'wss:' && !(url.protocol === 'ws:' && ['localhost', '127.0.0.1'].includes(url.hostname))) throw new Error('Endereço WebSocket inválido.')
  url.searchParams.set('token', token)
  return new WebSocket(url)
}
