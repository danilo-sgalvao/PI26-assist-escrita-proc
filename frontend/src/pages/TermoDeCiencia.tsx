import { useEffect, useState } from 'react'
import { verificarSaude } from '../api/http'

type EstadoDaApi = 'verificando' | 'disponivel' | 'indisponivel'

export function TermoDeCiencia() {
  const [estadoDaApi, setEstadoDaApi] = useState<EstadoDaApi>('verificando')

  useEffect(() => {
    let ativo = true
    verificarSaude()
      .then(() => { if (ativo) setEstadoDaApi('disponivel') })
      .catch(() => { if (ativo) setEstadoDaApi('indisponivel') })
    return () => { ativo = false }
  }, [])

  return (
    <main>
      <h1>Termo de ciência</h1>
      <p>Antes de usar a plataforma, saiba quais dados acompanham sua escrita.</p>
      <h2>O que é registrado</h2>
      <ul>
        <li>Versões do texto e a etapa em que foram salvas.</li>
        <li>Interações com o assistente e eventos de colagem.</li>
        <li>Tempo dedicado a cada etapa da atividade.</li>
      </ul>
      <h2>Quem acessa e para quê</h2>
      <p>Você pode consultar seus registros. O professor acompanha o processo para orientar a aprendizagem. Os indicadores não são notas nem rankings.</p>
      <p>As solicitações ao assistente podem ser processadas por um serviço externo de IA, sem seu nome ou outros identificadores. O assistente orienta, mas não escreve o texto por você.</p>
      <p>O uso da plataforma depende do aceite deste termo. Se você for menor de idade, também é necessário o consentimento de seu responsável.</p>
      <p role="status" aria-live="polite">
        {estadoDaApi === 'verificando' && 'Verificando conexão com a API…'}
        {estadoDaApi === 'disponivel' && 'API disponível.'}
        {estadoDaApi === 'indisponivel' && 'API indisponível no momento.'}
      </p>
    </main>
  )
}
