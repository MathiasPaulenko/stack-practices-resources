import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

interface Command {
    String process(HttpServletRequest req) throws ServletException;
}

class HomeCommand implements Command {
    public String process(HttpServletRequest req) {
        return "/WEB-INF/views/home.jsp";
    }
}

class UserCommand implements Command {
    public String process(HttpServletRequest req) {
        return "/WEB-INF/views/user.jsp";
    }
}

// Mapped to /* — every request in the app lands here.
@WebServlet("/*")
public class FrontControllerServlet extends HttpServlet {

    private final Map<String, Command> commands = new HashMap<>();

    @Override
    public void init() {
        commands.put("/", new HomeCommand());
        commands.put("/user", new UserCommand());
    }

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        // Shared preprocessing for every request
        if (!isAuthenticated(req)) {
            resp.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }

        Command command = commands.get(req.getPathInfo());
        if (command == null) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND);
            return;
        }
        // Dispatch: the command returns the view to render
        String view = command.process(req);
        req.getRequestDispatcher(view).forward(req, resp);
    }

    private boolean isAuthenticated(HttpServletRequest req) {
        return "Bearer valid".equals(req.getHeader("Authorization"));
    }
}
