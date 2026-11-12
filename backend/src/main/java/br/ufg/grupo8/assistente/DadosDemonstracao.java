package br.ufg.grupo8.assistente;

import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@Profile("demo")
class DadosDemonstracao {
    @Bean ApplicationRunner criarDados(JdbcTemplate banco, PasswordEncoder codificador, Environment env) {
        return args -> {
            String senha = env.getRequiredProperty("DEMO_PASSWORD");
            if (senha.length() < 12) throw new IllegalStateException("DEMO_PASSWORD deve ter pelo menos 12 caracteres.");
            for (String perfil : new String[]{"ESTUDANTE", "PROFESSOR"}) {
                String email = perfil.toLowerCase() + "@demo.local";
                banco.update("INSERT INTO usuario(email,senha_hash,perfil) SELECT ?,?,? WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE email=?)", email, codificador.encode(senha), perfil, email);
            }
        };
    }
}
