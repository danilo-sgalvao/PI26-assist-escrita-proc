import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { TermoDeCiencia } from './TermoDeCiencia'

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

test('mostra o termo e confirma a conexão com /api/health', async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true })
  vi.stubGlobal('fetch', fetchMock)

  render(<TermoDeCiencia />)

  expect(screen.getByRole('heading', { name: 'Termo de ciência' })).toBeInTheDocument()
  expect(screen.getByText(/consentimento de seu responsável/)).toBeInTheDocument()
  expect(await screen.findByRole('status')).toHaveTextContent('API disponível.')
  expect(fetchMock).toHaveBeenCalledWith('/api/health', { credentials: 'same-origin' })
})

test('informa quando a API está indisponível', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('sem conexão')))
  render(<TermoDeCiencia />)
  expect(await screen.findByRole('status')).toHaveTextContent('API indisponível no momento.')
})
