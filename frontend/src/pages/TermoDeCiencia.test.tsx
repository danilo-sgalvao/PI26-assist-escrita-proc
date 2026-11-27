import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { TermoDeCiencia } from './TermoDeCiencia'

afterEach(() => {
  cleanup()
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

test('mostra o termo e confirma a conexão com GET /saude da API configurada', async () => {
  vi.stubEnv('VITE_API_URL', 'https://api.exemplo/v1')
  const fetchMock = vi.fn().mockResolvedValue({ ok: true })
  vi.stubGlobal('fetch', fetchMock)

  render(<TermoDeCiencia />)

  expect(screen.getByRole('heading', { name: 'Termo de ciência' })).toBeInTheDocument()
  expect(screen.getByText(/consentimento de seu responsável/)).toBeInTheDocument()
  expect(await screen.findByRole('status')).toHaveTextContent('API disponível.')
  expect(fetchMock).toHaveBeenCalledWith('https://api.exemplo/v1/saude', { credentials: 'same-origin' })
})

test('naoDeveAnunciarApiDisponivelSemApiConfigurada_DEF001', async () => {
  vi.stubEnv('VITE_API_URL', '')
  const fetchMock = vi.fn().mockResolvedValue({ ok: true })
  vi.stubGlobal('fetch', fetchMock)

  render(<TermoDeCiencia />)

  expect(await screen.findByRole('status')).toHaveTextContent('API indisponível no momento.')
  expect(fetchMock).not.toHaveBeenCalled()
})

test('informa quando a API está indisponível', async () => {
  vi.stubEnv('VITE_API_URL', 'https://api.exemplo/v1')
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('sem conexão')))
  render(<TermoDeCiencia />)
  expect(await screen.findByRole('status')).toHaveTextContent('API indisponível no momento.')
})
