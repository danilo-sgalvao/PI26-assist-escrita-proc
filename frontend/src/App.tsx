import { Route, Switch } from 'wouter'
import { TermoDeCiencia } from './pages/TermoDeCiencia'
import { Escrita } from './pages/Escrita'
import './styles.css'
export function App() { return <Switch><Route path="/" component={Escrita} /><Route path="/termo-de-ciencia"><header className="cabecalho"><a href="/">← Voltar à escrita</a></header><TermoDeCiencia /></Route><Route><main><h1>Página não encontrada</h1><a href="/">Voltar ao início</a></main></Route></Switch> }
