import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.annotation.WebFilter;
import java.io.IOException;

/**
 * Chain of Responsibility — Java Servlet Filter variant.
 *
 * FilterChain.doFilter() is literally the pattern's next(): calling it
 * forwards the request to the next filter (or the servlet), skipping it
 * short-circuits the chain. Register the filter with @WebFilter or web.xml;
 * the container owns the ordering contract.
 */
@WebFilter("/api/*")
public class AuthFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest http = (HttpServletRequest) req;
        String token = http.getHeader("Authorization");

        if (token == null || !token.startsWith("Bearer ")) {
            ((HttpServletResponse) res).sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return; // short-circuit: nothing downstream executes
        }

        req.setAttribute("user", token.substring(7)); // request-scoped state
        chain.doFilter(req, res);                   // next()
    }
}
