import { Link, Route, Switch } from 'wouter'
import { TermoDeCiencia } from './pages/TermoDeCiencia'
import './styles.css'

export function App() {
  return (
    <>
      <header className="cabecalho">
        <Link href="/">Assistente de Escrita Processual</Link>
      </header>
      <Switch>
        <Route path="/" component={TermoDeCiencia} />
        <Route path="/termo-de-ciencia" component={TermoDeCiencia} />
        <Route><main><h1>Página não encontrada</h1><Link href="/">Voltar ao início</Link></main></Route>
      </Switch>
    </>
  )
}
