import { fireEvent, render, screen, waitFor, cleanup } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { Escrita } from './Escrita'
import * as api from '../api/revisoes'

vi.mock('../api/revisoes', () => ({ entrar: vi.fn(), definirSenha: vi.fn(), enviar: vi.fn(), consultar: vi.fn(), conectar: vi.fn(() => null) }))
afterEach(() => { cleanup(); vi.clearAllMocks(); sessionStorage.clear() })

test('envia versão somente com ciência e apresenta revisão recebida', async () => {
  vi.mocked(api.entrar).mockResolvedValue({ sub: 'aluno', idToken: 'id', accessToken: 'access' })
  vi.mocked(api.enviar).mockResolvedValue({ id_producao: 'versao-1', status: 'PROCESSANDO', sugestoes: [] })
  vi.mocked(api.consultar).mockResolvedValue({ id_producao: 'versao-1', status: 'CONCLUIDO', sugestoes: ['Revise os parágrafos.'] })
  render(<Escrita />)
  fireEvent.change(screen.getByLabelText('E-mail'), { target: { value: 'aluno@exemplo.com' } })
  fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'senha' } })
  fireEvent.click(screen.getByRole('button', { name: /entrar no meu espaço/i }))
  const texto = await screen.findByLabelText(/sua redação/i)
  fireEvent.change(texto, { target: { value: 'Meu texto de teste.' } })
  const botao = screen.getByRole('button', { name: /enviar para revisão/i })
  expect(botao).toBeDisabled()
  fireEvent.click(screen.getByRole('checkbox'))
  fireEvent.click(botao)
  await waitFor(() => expect(api.enviar).toHaveBeenCalledWith('Meu texto de teste.', 'id'))
  expect(await screen.findByText('Revise os parágrafos.')).toBeInTheDocument()
  expect(screen.getByText('Revisão disponível')).toBeInTheDocument()
})

test('mostra falha de envio sem perder o texto', async () => {
  vi.mocked(api.entrar).mockResolvedValue({ sub: 'aluno', idToken: 'id', accessToken: 'access' })
  vi.mocked(api.enviar).mockRejectedValue(new Error('Serviço indisponível.'))
  render(<Escrita />)
  fireEvent.change(screen.getByLabelText('E-mail'), { target: { value: 'aluno@exemplo.com' } })
  fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'senha' } })
  fireEvent.click(screen.getByRole('button', { name: /entrar no meu espaço/i }))
  const texto = await screen.findByLabelText(/sua redação/i)
  fireEvent.change(texto, { target: { value: 'Minha redação.' } })
  fireEvent.click(screen.getByRole('checkbox'))
  fireEvent.click(screen.getByRole('button', { name: /enviar para revisão/i }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Serviço indisponível.')
  expect(texto).toHaveValue('Minha redação.')
})

test('permite definir nova senha no primeiro acesso', async () => {
  vi.mocked(api.entrar).mockResolvedValue({ challengeSession: 'sessao', username: 'aluno' })
  vi.mocked(api.definirSenha).mockResolvedValue({ sub: 'aluno', idToken: 'id', accessToken: 'access' })
  render(<Escrita />)
  fireEvent.change(screen.getByLabelText('E-mail'), { target: { value: 'aluno@exemplo.com' } })
  fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'temporaria' } })
  fireEvent.click(screen.getByRole('button', { name: /entrar no meu espaço/i }))
  fireEvent.change(await screen.findByLabelText('Nova senha'), { target: { value: 'novaSenha1!' } })
  fireEvent.click(screen.getByRole('button', { name: /definir senha e entrar/i }))
  expect(await screen.findByLabelText(/sua redação/i)).toBeInTheDocument()
  expect(api.definirSenha).toHaveBeenCalledWith({ challengeSession: 'sessao', username: 'aluno' }, 'novaSenha1!')
})
