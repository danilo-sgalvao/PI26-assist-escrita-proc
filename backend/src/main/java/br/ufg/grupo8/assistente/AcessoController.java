package br.ufg.grupo8.assistente;

import java.security.Principal;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api")
public class AcessoController {
    private final JdbcTemplate banco;
    public AcessoController(JdbcTemplate banco) { this.banco = banco; }

    @GetMapping("/health") Map<String, String> health() { return Map.of("status", "ok"); }
    @GetMapping("/csrf") CsrfToken csrf(CsrfToken token) { return token; }
    @GetMapping("/eu") Map<String, Object> eu(Authentication auth) {
        return Map.of("email", auth.getName(), "perfis", auth.getAuthorities().stream().map(Object::toString).toList());
    }
    @GetMapping("/professor") Map<String, String> professor(Authentication auth) {
        if (auth.getAuthorities().stream().noneMatch(a -> a.getAuthority().equals("ROLE_PROFESSOR"))) throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        return Map.of("perfil", "professor");
    }
    @GetMapping("/termo") Map<String, String> termo() {
        return Map.of("versao", Seguranca.VERSAO_TERMO, "texto", "São registrados versões, interações, colagens e tempo por etapa. O estudante e o professor responsável acessam os registros para acompanhamento pedagógico. O texto e o pedido de apoio podem ser processados por um serviço externo de IA. Para menores, é necessário consentimento prévio do responsável.");
    }
    @PostMapping("/termo/aceite") @ResponseStatus(HttpStatus.NO_CONTENT)
    void aceitar(Principal principal) {
        var usuarios = banco.queryForList("SELECT id, menor, consentimento_responsavel FROM usuario WHERE email=?", principal.getName());
        if (usuarios.isEmpty()) throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        var usuario = usuarios.getFirst();
        if (Boolean.TRUE.equals(usuario.get("menor")) && !Boolean.TRUE.equals(usuario.get("consentimento_responsavel"))) throw new ResponseStatusException(HttpStatus.FORBIDDEN);
        banco.update("INSERT INTO aceite_termo(usuario_id,versao) SELECT ?,? WHERE NOT EXISTS (SELECT 1 FROM aceite_termo WHERE usuario_id=? AND versao=?)", usuario.get("id"), Seguranca.VERSAO_TERMO, usuario.get("id"), Seguranca.VERSAO_TERMO);
    }
}
