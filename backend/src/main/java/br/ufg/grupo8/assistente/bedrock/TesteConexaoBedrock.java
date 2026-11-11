package br.ufg.grupo8.assistente.bedrock;

import java.time.Duration;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

/** Comando de diagnóstico com conteúdo sintético fixo. */
public final class TesteConexaoBedrock {
    public static void main(String[] args) {
        String regiao = System.getenv("AWS_REGION");
        String modelo = System.getenv("BEDROCK_MODEL_ID");
        if (regiao == null || regiao.isBlank() || modelo == null || modelo.isBlank())
            throw new IllegalArgumentException("Defina AWS_REGION e BEDROCK_MODEL_ID");
        try (var cliente = BedrockRuntimeClient.builder().region(Region.of(regiao))
                .overrideConfiguration(c -> c.apiCallTimeout(Duration.ofSeconds(30))).build()) {
            var gateway = new BedrockGateway(cliente, modelo, 128);
            long inicio = System.nanoTime();
            var resultado = gateway.gerar("Explique conceitos em português, de forma breve.",
                    "O que é uma tese em um texto argumentativo?");
            System.out.printf("Conexão concluída em %d ms; tokens de entrada=%s; saída=%s%n",
                    (System.nanoTime() - inicio) / 1_000_000, resultado.tokensEntrada(), resultado.tokensSaida());
            System.out.println("Resposta ao teste sintético: " + resultado.texto());
        }
    }
}
