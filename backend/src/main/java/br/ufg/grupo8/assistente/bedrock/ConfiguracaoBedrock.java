package br.ufg.grupo8.assistente.bedrock;

import java.time.Duration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

@Configuration
@ConditionalOnProperty(name = "assistente.bedrock.habilitado", havingValue = "true")
public class ConfiguracaoBedrock {
    @Bean(destroyMethod = "close")
    BedrockRuntimeClient clienteBedrock(@Value("${assistente.bedrock.regiao}") String regiao,
                                         @Value("${assistente.bedrock.timeout-segundos:30}") int timeout) {
        if (regiao.isBlank() || timeout < 1 || timeout > 120) throw new IllegalArgumentException("Região ou timeout Bedrock inválido");
        return BedrockRuntimeClient.builder().region(Region.of(regiao))
                .overrideConfiguration(c -> c.apiCallTimeout(Duration.ofSeconds(timeout)))
                .build();
    }
    @Bean AssistenteGateway assistenteGateway(BedrockRuntimeClient cliente,
            @Value("${assistente.bedrock.modelo}") String modelo,
            @Value("${assistente.bedrock.max-tokens:256}") int limiteTokens) {
        return new BedrockGateway(cliente, modelo, limiteTokens);
    }
}
