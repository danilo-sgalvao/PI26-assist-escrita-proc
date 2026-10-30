"""Verificações da extração e da recuperação documental, sem serviços externos."""
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from zipfile import ZipFile

from ferramentas import rag


class ExtracaoTest(unittest.TestCase):
    def test_cabecalhos_irmaos_nao_se_tornam_ancestrais(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "fonte.md"
            arquivo.write_text("## Raiz\n### Um\nconteúdo\n### Dois\ntexto\n## Outra\nfim", encoding="utf-8")
            unidades = rag.extrair(arquivo)
        self.assertEqual(unidades[2]["secao"], "Raiz > Dois")
        self.assertEqual(unidades[3]["secao"], "Outra")

    def test_markdown_preserva_secao_linhas_e_conteudo_dos_trechos(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "fonte.md"
            conteudo = "# Documento\n\n## RF09 Autoria\n" + "Orientação sem reescrever.\n" * 200
            arquivo.write_text(conteudo, encoding="utf-8")
            unidades = rag.extrair(arquivo)
        trechos = list(rag.segmentar(unidades))
        self.assertGreater(len(trechos), 1)
        self.assertTrue(all(len(t["texto"]) <= rag.TAMANHO_TRECHO for t in trechos))
        self.assertIn("RF09 Autoria", trechos[-1]["secao"])
        self.assertEqual(trechos[-1]["localizacao"]["tipo"], "linhas")
        self.assertEqual(trechos[-1]["localizacao"]["fim"], 203)
        for linha in conteudo.splitlines():
            if linha.strip():
                self.assertTrue(any(linha in t["texto"] for t in trechos))

    def test_docx_preserva_ordem_paragrafos_e_tabelas(self):
        xml = '''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
        <w:p><w:r><w:t>Antes</w:t></w:r></w:p>
        <w:tbl><w:tr><w:tc><w:p><w:r><w:t>RF01</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
        <w:p><w:r><w:t>Depois</w:t></w:r></w:p></w:body></w:document>'''
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "fonte.docx"
            with ZipFile(arquivo, "w") as pacote:
                pacote.writestr("word/document.xml", xml)
            unidades = rag.extrair(arquivo)
        self.assertEqual([u["texto"] for u in unidades], ["Antes", "RF01", "Depois"])
        self.assertEqual(unidades[-1]["localizacao"]["inicio"], 3)


class BuscaTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.indice = Path(self.pasta.name) / "indice.sqlite3"
        trechos = []
        for id_, estado, texto in [
            ("ers-v2", "vigente", "RN02: a IA orienta sem reescrever. Autoria e proteção."),
            ("ers-v2-word", "representacao", "RN02: a IA orienta sem reescrever. Autoria e proteção."),
            ("plano-v1", "historico", "O modelo local será executado via Ollama.")]:
            trechos.append({"id": id_+":0001", "fonte_id": id_, "estado": estado,
                            "texto": texto, "secao": "Regras", "precedencia": 2,
                            "caminho": id_+".md", "localizacao": {"tipo":"linhas", "inicio":1, "fim":1}})
        trechos.append({"id":"ruido:0001", "fonte_id":"ruido", "estado":"vigente", "texto":"Reescrever.",
                        "secao":"Reescrever", "precedencia":2, "caminho":"ruido.md",
                        "localizacao":{"tipo":"linhas", "inicio":1, "fim":1}})
        rag.indexar(trechos, self.indice)

    def test_busca_sem_acentos_com_origem_e_sem_copias(self):
        encontrados = rag.buscar("Qual a protecao da autoria?", indice=self.indice)
        self.assertEqual([t["fonte_id"] for t in encontrados], ["ers-v2"])
        self.assertEqual(encontrados[0]["localizacao"]["inicio"], 1)

    def test_historico_apenas_quando_solicitado(self):
        self.assertEqual(rag.buscar("Ollama", indice=self.indice), [])
        self.assertEqual(rag.buscar("Ollama", historico=True, indice=self.indice)[0]["estado"], "historico")

    def test_identificador_e_pergunta_sem_evidencias(self):
        self.assertEqual(rag.buscar("RN02", indice=self.indice)[0]["fonte_id"], "ers-v2")
        self.assertEqual(rag.buscar("fotossintese", indice=self.indice), [])
        self.assertEqual(rag.buscar('" OR * --', indice=self.indice), [])
        self.assertEqual(rag.buscar("qual e a", indice=self.indice), [])

    def test_consulta_por_id_exclui_trecho_que_so_casa_com_palavra_generica(self):
        encontrados = rag.buscar("RN02 reescrever", indice=self.indice)
        self.assertEqual([t["fonte_id"] for t in encontrados], ["ers-v2"])

    def test_identificador_com_hifen(self):
        trecho = {"id":"adr:1", "fonte_id":"adr", "estado":"vigente", "texto":"ADR-006: provedor e modelo pendentes.",
                  "secao":"ADR-006", "precedencia":1, "caminho":"adr.md",
                  "localizacao":{"tipo":"linhas", "inicio":1, "fim":1}}
        rag.indexar([trecho], self.indice)
        self.assertEqual(rag.buscar("ADR-006 provedor", indice=self.indice)[0]["fonte_id"], "adr")


class AtualizacaoTest(unittest.TestCase):
    def test_construcao_reproduzivel_e_deteccao_de_documento_alterado(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            base = raiz / "conhecimento"
            gerado = base / "gerado"
            (raiz / "docs").mkdir()
            (raiz / "docs/guia.md").write_text("# Guia\n\nPreservar autoria.\n", encoding="utf-8")
            (raiz / "CLAUDE.md").write_text("# Contexto\n\nHistórico imutável.\n", encoding="utf-8")
            fontes = [{"id": "guia", "caminho": "docs/guia.md", "estado": "vigente"},
                      {"id": "contexto", "caminho": "CLAUDE.md", "estado": "vigente"}]
            rag.escrever_json(base / "fontes.json", fontes)
            with patch.multiple(rag, RAIZ=raiz, BASE=base, GERADO=gerado):
                _, trechos = rag.construir()
                rag.indexar(trechos, gerado / "indice.sqlite3")
                self.assertEqual(rag.verificar()["fontes"], 2)
                primeira_geracao = (gerado / "trechos.jsonl").read_bytes()
                rag.construir()
                self.assertEqual(primeira_geracao, (gerado / "trechos.jsonl").read_bytes())
                (raiz / "docs/guia.md").write_text("# Guia\n\nTexto alterado.\n", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Fonte alterada"):
                    rag.verificar()

    def test_politica_de_contexto_inclui_divergencia_rf15_e_pendencias(self):
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            (base / "politica-rag.md").write_text("Cite as fontes.", encoding="utf-8")
            trecho = {"id":"decisoes:1", "fonte_id":"decisoes-v1-2", "estado":"vigente",
                      "caminho":"decisoes.md", "secao":"Decisões > B. Decisões",
                      "texto":"B2: RF15 usa textos internos; B5 e B10 pendentes.",
                      "localizacao":{"tipo":"linhas", "inicio":1, "fim":2}}
            with patch.object(rag, "BASE", base), patch.object(rag, "carregar_trechos", return_value=[trecho]):
                resultado = rag.contexto("Quais fontes?", [])
            self.assertIn("RF15 usa textos internos", resultado)
            self.assertIn("B5 e B10 pendentes", resultado)
            self.assertIn("Nenhum trecho relevante", resultado)


if __name__ == "__main__":
    unittest.main()
