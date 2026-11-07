import java.io.IOException;
import java.util.List;
import java.util.UUID;

import org.slf4j.MDC;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.filter.OncePerRequestFilter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Spring Boot correlation ID filter: reads X-Correlation-ID (or generates one),
 * stores it in SLF4J's MDC so every log line carries it, returns it on the
 * response, and clears the MDC afterwards to avoid thread-pool leaks.
 *
 * Logback pattern to surface the ID:
 *   <pattern>{"correlationId": "%X{correlationId}", "level": "%p", "message": "%m"}%n</pattern>
 */
@Component
public class CorrelationIdFilter extends OncePerRequestFilter {

    public static final String CORRELATION_ID_HEADER = "X-Correlation-ID";
    public static final String CORRELATION_ID_KEY = "correlationId";

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        String correlationId = request.getHeader(CORRELATION_ID_HEADER);
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString();
        }

        MDC.put(CORRELATION_ID_KEY, correlationId);
        response.setHeader(CORRELATION_ID_HEADER, correlationId);
        try {
            filterChain.doFilter(request, response);
        } finally {
            MDC.remove(CORRELATION_ID_KEY);
        }
    }

    /** RestTemplate that forwards the current correlation ID on every call. */
    @Bean
    public RestTemplate restTemplate() {
        RestTemplate restTemplate = new RestTemplate();
        restTemplate.setInterceptors(List.of((request, body, execution) -> {
            String correlationId = MDC.get(CORRELATION_ID_KEY);
            if (correlationId != null) {
                request.getHeaders().add(CORRELATION_ID_HEADER, correlationId);
            }
            return execution.execute(request, body);
        }));
        return restTemplate;
    }
}
