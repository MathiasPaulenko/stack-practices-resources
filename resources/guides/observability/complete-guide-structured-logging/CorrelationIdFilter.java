// CorrelationIdFilter.java — MDC-based correlation IDs
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.UUID;

@Component
public class CorrelationIdFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String requestId = httpRequest.getHeader("X-Request-ID");
        if (requestId == null || requestId.isEmpty()) {
            requestId = UUID.randomUUID().toString();
        }

        MDC.put("request_id", requestId);
        MDC.put("service", "order-service");

        // MDC.put() rejects null values — only set user_id when present.
        String userId = extractUserId(httpRequest);
        if (userId != null) {
            MDC.put("user_id", userId);
        }

        httpResponse.setHeader("X-Request-ID", requestId);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear(); // required — the worker thread gets reused
        }
    }

    private String extractUserId(HttpServletRequest request) {
        Object user = request.getSession(false) != null
            ? request.getSession(false).getAttribute("userId")
            : null;
        return user != null ? user.toString() : null;
    }
}
