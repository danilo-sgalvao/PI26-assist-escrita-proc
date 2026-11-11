package br.ufg.grupo8.assistente.bedrock;

import java.util.Objects;
import software.amazon.awssdk.core.exception.SdkException;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.*;

/** Transporte Bedrock Converse. Não substitui o guardrail de autoria. */
public final class BedrockGateway implements AssistenteGateway {
    private final BedrockRuntimeClient cliente;
    private final String modelo;
    private final int limiteTokens;

    public BedrockGateway(BedrockRuntimeClient cliente, String modelo, int limiteTokens) {
        this.cliente = Objects.requireNonNull(cliente);
        if (modelo == null || modelo.isBlank()) throw new IllegalArgumentException("Modelo Bedrock obrigatório");
        if (limiteTokens < 1 || limiteTokens > 4096) throw new IllegalArgumentException("Limite de tokens inválido");
        this.modelo = modelo;
        this.limiteTokens = limiteTokens;
    }

    @Override public Resultado gerar(String instrucao, String mensagem) {
        if (instrucao == null || instrucao.isBlank() || mensagem == null || mensagem.isBlank()
                || instrucao.length() > 8000 || mensagem.length() > 16000) {
            throw new IllegalArgumentException("Instrução ou mensagem vazia ou acima do limite");
        }
        var pedido = ConverseRequest.builder().modelId(modelo)
                .system(SystemContentBlock.fromText(instrucao))
                .messages(Message.builder().role(ConversationRole.USER).content(ContentBlock.fromText(mensagem)).build())
                .inferenceConfig(InferenceConfiguration.builder().maxTokens(limiteTokens).temperature(0.0f).build())
                .build();
        final ConverseResponse resposta;
        try { resposta = cliente.converse(pedido); }
        catch (SdkException erro) { throw new BedrockIndisponivelException(erro); }
        if ((resposta.stopReason() != StopReason.END_TURN && resposta.stopReason() != StopReason.STOP_SEQUENCE)
                || resposta.output() == null || resposta.output().message() == null) {
            throw new BedrockIndisponivelException(null);
        }
        String texto = resposta.output().message().content().stream().map(ContentBlock::text)
                .filter(Objects::nonNull).reduce((a, b) -> a + "\n" + b).orElse("").trim();
        if (texto.isEmpty()) throw new BedrockIndisponivelException(null);
        var uso = resposta.usage();
        return new Resultado(texto, uso == null ? null : uso.inputTokens(), uso == null ? null : uso.outputTokens());
    }
}
