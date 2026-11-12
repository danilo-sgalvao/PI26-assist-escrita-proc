import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lambdas"))
from comum import resposta


class CorsTest(unittest.TestCase):
    def test_resposta_de_sucesso_e_erro_tem_origem_configurada(self):
        with patch.dict(os.environ, {"FRONTEND_ORIGIN": "https://exemplo.cloudfront.net"}):
            for status in (200, 202, 400, 401, 503):
                resultado = resposta(status, {"mensagem": "teste"})
                self.assertEqual(resultado["headers"]["Access-Control-Allow-Origin"], "https://exemplo.cloudfront.net")
                self.assertEqual(resultado["headers"]["Access-Control-Allow-Headers"], "Content-Type,Authorization")
                self.assertEqual(resultado["headers"]["Access-Control-Allow-Methods"], "GET,POST,OPTIONS")


if __name__ == "__main__":
    unittest.main()
