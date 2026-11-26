package br.ufg.grupo8.assistente;

import java.io.IOException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.authentication.AnonymousAuthenticationFilter;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.web.filter.OncePerRequestFilter;

@Configuration
public class Seguranca {
    static final String VERSAO_TERMO = "1";

    @Bean PasswordEncoder senha() { return new BCryptPasswordEncoder(); }

    @Bean UserDetailsService usuarios(JdbcTemplate banco) {
        return email -> banco.query("SELECT email, senha_hash, perfil, ativo FROM usuario WHERE lower(email) = lower(?)", rs -> {
            if (!rs.next()) throw new UsernameNotFoundException("Credenciais inválidas");
            return User.withUsername(rs.getString("email")).password(rs.getString("senha_hash"))
                    .roles(rs.getString("perfil")).disabled(!rs.getBoolean("ativo")).build();
        }, email);
    }

    @Bean DaoAuthenticationProvider autenticacao(UserDetailsService usuarios, PasswordEncoder senha) {
        var provedor = new DaoAuthenticationProvider(usuarios);
        provedor.setPasswordEncoder(senha);
        return provedor;
    }

    @Bean SecurityFilterChain filtros(HttpSecurity http, JdbcTemplate banco) throws Exception {
        var csrf = CookieCsrfTokenRepository.withHttpOnlyFalse();
        http.csrf(c -> c.csrfTokenRepository(csrf))
            .authorizeHttpRequests(a -> a.requestMatchers("/api/health", "/api/csrf", "/api/login").permitAll()
                    .requestMatchers("/api/termo/**").hasRole("ESTUDANTE").anyRequest().authenticated())
            .formLogin(f -> f.loginProcessingUrl("/api/login").successHandler((req, res, auth) -> res.setStatus(204))
                    .failureHandler((req, res, ex) -> res.sendError(401)).permitAll())
            .logout(l -> l.logoutUrl("/api/logout").logoutSuccessHandler((req, res, auth) -> res.setStatus(204)))
            .exceptionHandling(e -> e.authenticationEntryPoint((req, res, ex) -> res.sendError(401)))
            .addFilterAfter(new FiltroTermo(banco), AnonymousAuthenticationFilter.class);
        return http.build();
    }

    static class FiltroTermo extends OncePerRequestFilter {
        private final JdbcTemplate banco;
        FiltroTermo(JdbcTemplate banco) { this.banco = banco; }
        @Override protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws ServletException, IOException {
            var auth = org.springframework.security.core.context.SecurityContextHolder.getContext().getAuthentication();
            String caminho = req.getRequestURI();
            if (auth != null && auth.isAuthenticated() && auth.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_ESTUDANTE"))
                    && !caminho.equals("/api/termo") && !caminho.equals("/api/termo/aceite")
                    && !caminho.equals("/api/logout") && !caminho.equals("/api/csrf") && !caminho.equals("/api/health")) {
                Integer aceito = banco.queryForObject("SELECT count(*) FROM aceite_termo a JOIN usuario u ON u.id=a.usuario_id WHERE u.email=? AND a.versao=?", Integer.class, auth.getName(), VERSAO_TERMO);
                if (aceito == null || aceito == 0) { res.sendError(403, "Aceite do termo necessário"); return; }
            }
            chain.doFilter(req, res);
        }
    }
}
