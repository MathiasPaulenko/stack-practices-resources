// SentryConfig.java — Sentry SDK configuration for Spring Boot.
//
// This class shows how to initialize the Sentry SDK with sensitive data
// filtering, user context, breadcrumbs, and manual error capture.
//
// Usage:
//   Annotate your configuration class with @Configuration and import this bean.

import io.sentry.Sentry;
import io.sentry.spring.tracing.SentryTracingConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SentryConfig {

    @Bean
    public Sentry.OptionsConfiguration sentryOptions() {
        return options -> {
            options.setDsn("https://your-dsn@sentry.io/123");
            options.setEnvironment("production");
            options.setRelease("order-service@1.2.3");
            options.setTracesSampleRate(0.1);
            options.setBeforeSend((event, hint) -> {
                if (event.getRequest() != null) {
                    event.getRequest().getHeaders().remove("Authorization");
                    event.getRequest().getHeaders().remove("Cookie");
                }
                return event;
            });
        };
    }
}
