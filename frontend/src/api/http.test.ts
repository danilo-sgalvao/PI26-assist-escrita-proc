import { afterEach, expect, test, vi } from 'vitest'
import { verificarSaude } from './http'

afterEach(() => {
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

test('deveConsultarRotaSaudeDaApiConfigurada_DEF001', async () => {
  vi.stubEnv('VITE_API_URL', 'https://api.exemplo/v1/')
  const fetchMock = vi.fn().mockResolvedValue({ ok: true })
  vi.stubGlobal('fetch', fetchMock)

  await verificarSaude()

  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(fetchMock.mock.calls[0][0]).toBe('https://api.exemplo/v1/saude')
})

test('naoDeveRecorrerARotaInexistenteApiHealthSemApiConfigurada_DEF001', async () => {
  vi.stubEnv('VITE_API_URL', '')
  const fetchMock = vi.fn().mockResolvedValue({ ok: true })
  vi.stubGlobal('fetch', fetchMock)

  await expect(verificarSaude()).rejects.toThrow('VITE_API_URL')
  expect(fetchMock).not.toHaveBeenCalled()
})

test('deveFalharQuandoSaudeNaoResponde200_DEF001', async () => {
  vi.stubEnv('VITE_API_URL', 'https://api.exemplo/v1')
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 404 }))

  await expect(verificarSaude()).rejects.toThrow('404')
})
