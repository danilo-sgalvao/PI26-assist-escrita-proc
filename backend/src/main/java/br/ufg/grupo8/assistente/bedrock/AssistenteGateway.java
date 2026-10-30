package br.ufg.grupo8.assistente.bedrock;

/** Porta de transporte; respostas brutas exigem validação antes de qualquer exibição. */
public interface AssistenteGateway {
    Resultado gerar(String instrucao, String mensagem);
    record Resultado(String texto, Integer tokensEntrada, Integer tokensSaida) {}
}
