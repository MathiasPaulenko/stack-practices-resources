// Spring audit filter: correlation ID via MDC + request log + audit record for non-GET ops.
// Requires spring-boot-starter-web + slf4j (Logback) on the classpath.
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.UUID;

@Component
public class AuditFilter extends OncePerRequestFilter {
    private static final Logger logger = LoggerFactory.getLogger("api.requests");
    private static final Logger auditLogger = LoggerFactory.getLogger("api.audit");

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        String correlationId = request.getHeader("X-Correlation-Id");
        if (correlationId == null) correlationId = UUID.randomUUID().toString();

        MDC.put("correlationId", correlationId);
        response.setHeader("X-Correlation-Id", correlationId);

        long start = System.currentTimeMillis();
        try {
            filterChain.doFilter(request, response);
        } finally {
            logger.info("method={} path={} status={} duration={}ms",
                request.getMethod(),
                request.getRequestURI(),
                response.getStatus(),
                System.currentTimeMillis() - start);

            // Audit record: only for state-changing or sensitive operations
            if (!"GET".equals(request.getMethod()) && !"HEAD".equals(request.getMethod())) {
                auditLogger.info("correlationId={} actor={} action={} resource={} outcome={} ip={}",
                    correlationId,
                    request.getUserPrincipal() != null
                        ? request.getUserPrincipal().getName() : "anonymous",
                    request.getMethod(),
                    request.getRequestURI(),
                    response.getStatus() < 400 ? "success" : "failure",
                    request.getRemoteAddr());
            }
            MDC.clear();
        }
    }
}
