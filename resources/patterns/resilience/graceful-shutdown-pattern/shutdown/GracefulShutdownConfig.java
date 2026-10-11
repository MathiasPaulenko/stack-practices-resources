// GracefulShutdownConfig.java — Spring Boot graceful shutdown
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.boot.web.server.Shutdown;

@Configuration
public class GracefulShutdownConfig
    implements WebServerFactoryCustomizer<TomcatServletWebServerFactory> {

    @Override
    public void customize(TomcatServletWebServerFactory factory) {
        factory.setShutdown(Shutdown.GRACEFUL);
        // Spring will wait for active requests to complete
    }
}

// application.properties
// server.shutdown=graceful
// spring.lifecycle.timeout-per-shutdown-phase=30s
