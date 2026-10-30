package br.ufg.grupo8.assistente;

import java.time.Duration;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.ContentBlock;
import software.amazon.awssdk.services.bedrockruntime.model.ConversationRole;
import software.amazon.awssdk.services.bedrockruntime.model.Message;

/** Experimento isolado, somente com dados sintéticos; não é endpoint da aplicação. */
public class ExperimentoBedrock {
    public static void main(String[] args) {
        String regiao = System.getenv("AWS_REGION");
        String modelo = System.getenv("BEDROCK_MODEL_ID");
        if (regiao == null || regiao.isBlank() || modelo == null || modelo.isBlank()) {
            throw new IllegalArgumentException("Configure AWS_REGION e BEDROCK_MODEL_ID para o experimento.");
        }
        long inicio = System.nanoTime();
        try (var cliente = BedrockRuntimeClient.builder().region(Region.of(regiao))
                .overrideConfiguration(c -> c.apiCallTimeout(Duration.ofSeconds(30))).build()) {
            var mensagem = Message.builder().role(ConversationRole.USER)
                    .content(ContentBlock.fromText("Em uma frase, explique o que é uma tese em um texto argumentativo.")) .build();
            var resposta = cliente.converse(r -> r.modelId(modelo).messages(mensagem)
                    .inferenceConfig(c -> c.maxTokens(100).temperature(0.0F)));
            System.out.printf("Chamada concluída. Latência: %d ms. Tokens de entrada: %d; saída: %d.%n",
                    (System.nanoTime() - inicio) / 1_000_000, resposta.usage().inputTokens(), resposta.usage().outputTokens());
            System.out.println("Resposta sintética: " + resposta.output().message().content().getFirst().text());
        }
    }
}
