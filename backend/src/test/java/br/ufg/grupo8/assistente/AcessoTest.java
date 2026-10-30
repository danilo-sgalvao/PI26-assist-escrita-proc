package br.ufg.grupo8.assistente;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class AcessoTest {
    @Autowired MockMvc mvc;
    @Autowired JdbcTemplate banco;
    @Autowired PasswordEncoder senha;

    @BeforeEach void preparar() {
        banco.update("DELETE FROM aceite_termo");
        banco.update("DELETE FROM usuario");
        banco.update("INSERT INTO usuario(email,senha_hash,perfil,menor,consentimento_responsavel) VALUES (?,?,?,?,?)", "aluno@teste.local", senha.encode("senha"), "ESTUDANTE", false, false);
        banco.update("INSERT INTO usuario(email,senha_hash,perfil,menor,consentimento_responsavel) VALUES (?,?,?,?,?)", "menor@teste.local", senha.encode("senha"), "ESTUDANTE", true, false);
        banco.update("INSERT INTO usuario(email,senha_hash,perfil) VALUES (?,?,?)", "professor@teste.local", senha.encode("senha"), "PROFESSOR");
    }
    @Test void deveExigirAutenticacao() throws Exception {
        mvc.perform(get("/api/eu")).andExpect(status().isUnauthorized());
    }
    @Test void deveAutenticarPorSessaoERejeitarSenhaIncorreta() throws Exception {
        mvc.perform(post("/api/login").with(csrf()).param("username", "professor@teste.local").param("password", "errada")).andExpect(status().isUnauthorized());
        var resultado = mvc.perform(post("/api/login").with(csrf()).param("username", "professor@teste.local").param("password", "senha")).andExpect(status().isNoContent()).andReturn();
        mvc.perform(get("/api/eu").session((org.springframework.mock.web.MockHttpSession) resultado.getRequest().getSession(false))).andExpect(status().isOk());
    }
    @Test void deveBloquearEstudanteAteAceiteEImpedirAcessoDeProfessor() throws Exception {
        var aluno = user("aluno@teste.local").roles("ESTUDANTE");
        mvc.perform(get("/api/eu").with(aluno)).andExpect(status().isForbidden());
        mvc.perform(get("/api/termo").with(aluno)).andExpect(status().isOk());
        mvc.perform(post("/api/termo/aceite").with(aluno)).andExpect(status().isForbidden());
        mvc.perform(post("/api/termo/aceite").with(aluno).with(csrf())).andExpect(status().isNoContent());
        mvc.perform(get("/api/eu").with(aluno)).andExpect(status().isOk());
        mvc.perform(get("/api/professor").with(aluno)).andExpect(status().isForbidden());
    }
    @Test void deveExigirConsentimentoPrevioParaMenor() throws Exception {
        var menor = user("menor@teste.local").roles("ESTUDANTE");
        mvc.perform(post("/api/termo/aceite").with(menor).with(csrf())).andExpect(status().isForbidden());
        banco.update("UPDATE usuario SET consentimento_responsavel=true WHERE email=?", "menor@teste.local");
        mvc.perform(post("/api/termo/aceite").with(menor).with(csrf())).andExpect(status().isNoContent());
    }
    @Test void professorPodeAcessarSuaAreaMasNaoAceitarTermoDeEstudante() throws Exception {
        var professor = user("professor@teste.local").roles("PROFESSOR");
        mvc.perform(get("/api/professor").with(professor)).andExpect(status().isOk());
        mvc.perform(post("/api/termo/aceite").with(professor).with(csrf())).andExpect(status().isForbidden());
    }
}
