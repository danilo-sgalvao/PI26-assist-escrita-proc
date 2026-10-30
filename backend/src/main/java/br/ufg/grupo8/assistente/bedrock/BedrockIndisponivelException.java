package br.ufg.grupo8.assistente.bedrock;

/** Erro genérico que não inclui o texto enviado nem detalhes da resposta. */
public final class BedrockIndisponivelException extends RuntimeException {
    public BedrockIndisponivelException(Throwable causa) {
        super("Serviço de IA indisponível ou resposta não utilizável", causa);
    }
}
