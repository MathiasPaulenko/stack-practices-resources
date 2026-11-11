import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.oauth2.client.oidc.web.logout.OidcClientInitiatedLogoutSuccessHandler;
import org.springframework.security.oauth2.client.registration.ClientRegistrationRepository;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.context.annotation.Bean;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.core.oidc.user.OidcUser;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class FederatedIdentityApp {

    @GetMapping("/user")
    public String user(@AuthenticationPrincipal OidcUser principal) {
        if (principal == null) return "Not authenticated";
        return "Hello, " + principal.getFullName() + " (" + principal.getEmail() + ")";
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http,
            ClientRegistrationRepository repo) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/user").authenticated()
                .anyRequest().permitAll()
            )
            .oauth2Login(oauth -> {})
            .logout(logout -> logout
                .logoutSuccessHandler(
                    new OidcClientInitiatedLogoutSuccessHandler(repo)
                )
            );
        return http.build();
    }

    public static void main(String[] args) {
        SpringApplication.run(FederatedIdentityApp.class, args);
    }
}

// application.yml:
// spring.security.oauth2.client.registration.google.client-id=xxx
// spring.security.oauth2.client.registration.google.client-secret=xxx

