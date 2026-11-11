package br.ufg.grupo8.assistente.bedrock;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Configuration;
import org.mockito.ArgumentCaptor;
import software.amazon.awssdk.core.exception.SdkClientException;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;
import software.amazon.awssdk.services.bedrockruntime.model.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class BedrockGatewayTest {
    private final BedrockRuntimeClient cliente = mock(BedrockRuntimeClient.class);
    private final BedrockGateway gateway = new BedrockGateway(cliente, "modelo-teste", 128);

    @Test void enviaInstrucaoEMensagemDelimitadasEDevolveUso() {
        var mensagem = Message.builder().role(ConversationRole.ASSISTANT).content(ContentBlock.fromText("Que ideia você quer defender?")).build();
        var resposta = ConverseResponse.builder().output(ConverseOutput.builder().message(mensagem).build())
                .stopReason(StopReason.END_TURN).usage(TokenUsage.builder().inputTokens(12).outputTokens(7).totalTokens(19).build()).build();
        when(cliente.converse(any(ConverseRequest.class))).thenReturn(resposta);
        var resultado = gateway.gerar("Oriente sem escrever", "Como começo?");
        var captor = ArgumentCaptor.forClass(ConverseRequest.class);
        verify(cliente).converse(captor.capture());
        var requisicao = captor.getValue();
        assertEquals("modelo-teste", requisicao.modelId());
        assertEquals("Oriente sem escrever", requisicao.system().getFirst().text());
        assertEquals(ConversationRole.USER, requisicao.messages().getFirst().role());
        assertEquals("Como começo?", requisicao.messages().getFirst().content().getFirst().text());
        assertEquals(128, requisicao.inferenceConfig().maxTokens());
        assertEquals("Que ideia você quer defender?", resultado.texto());
        assertEquals(12, resultado.tokensEntrada());
        assertEquals(7, resultado.tokensSaida());
    }

    @Test void falhaDeSdkRetornaErroGenerico() {
        when(cliente.converse(any(ConverseRequest.class))).thenThrow(SdkClientException.create("credencial ausente"));
        var erro = assertThrows(BedrockIndisponivelException.class, () -> gateway.gerar("instrução", "texto sintético"));
        assertFalse(erro.getMessage().contains("texto sintético"));
    }

    @Test void respostaBloqueadaOuVaziaNaoEhRetornada() {
        var mensagem = Message.builder().role(ConversationRole.ASSISTANT).content(ContentBlock.fromText("texto")).build();
        when(cliente.converse(any(ConverseRequest.class))).thenReturn(ConverseResponse.builder()
                .output(ConverseOutput.builder().message(mensagem).build()).stopReason(StopReason.GUARDRAIL_INTERVENED).build());
        assertThrows(BedrockIndisponivelException.class, () -> gateway.gerar("instrução", "mensagem"));
        when(cliente.converse(any(ConverseRequest.class))).thenReturn(ConverseResponse.builder()
                .output(ConverseOutput.builder().message(mensagem).build()).stopReason(StopReason.MAX_TOKENS).build());
        assertThrows(BedrockIndisponivelException.class, () -> gateway.gerar("instrução", "mensagem"));
        when(cliente.converse(any(ConverseRequest.class))).thenReturn(ConverseResponse.builder().build());
        assertThrows(BedrockIndisponivelException.class, () -> gateway.gerar("instrução", "mensagem"));
    }

    @Test void rejeitaConfiguracaoOuEntradaInvalidaSemChamarAws() {
        assertThrows(IllegalArgumentException.class, () -> new BedrockGateway(cliente, " ", 10));
        assertThrows(IllegalArgumentException.class, () -> new BedrockGateway(cliente, "modelo", 0));
        assertThrows(IllegalArgumentException.class, () -> gateway.gerar("instrução", " "));
        assertThrows(IllegalArgumentException.class, () -> gateway.gerar("instrução", "a".repeat(16001)));
        verifyNoInteractions(cliente);
    }

    @Test void habilitacaoEhExplicitaEExigeConfiguracao() {
        var runner = new ApplicationContextRunner().withUserConfiguration(ApenasBedrock.class);
        runner.run(contexto -> assertFalse(contexto.containsBean("assistenteGateway")));
        runner.withPropertyValues("assistente.bedrock.habilitado=true").run(contexto -> assertNotNull(contexto.getStartupFailure()));
        runner.withPropertyValues("assistente.bedrock.habilitado=true", "assistente.bedrock.regiao=us-east-1",
                "assistente.bedrock.modelo=modelo-teste").run(contexto -> assertNotNull(contexto.getBean(AssistenteGateway.class)));
    }
    @Configuration(proxyBeanMethods = false) @Import(ConfiguracaoBedrock.class) static class ApenasBedrock {}
}
