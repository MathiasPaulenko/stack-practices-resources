import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class AgentToolSelection {

    record Tool(String name, String description, String category, Map<String, String> parameters) {}

    static final Map<String, Tool> TOOL_REGISTRY = Map.of(
        "web_search", new Tool("web_search", "Search the web", "research", Map.of("query", "string")),
        "code_search", new Tool("code_search", "Search codebase", "research", Map.of("pattern", "string")),
        "read_file", new Tool("read_file", "Read file", "file_ops", Map.of("path", "string")),
        "write_file", new Tool("write_file", "Write file", "file_ops", Map.of("path", "string", "content", "string")),
        "run_tests", new Tool("run_tests", "Execute tests", "execution", Map.of("testFile", "string")),
        "deploy", new Tool("deploy", "Deploy app", "execution", Map.of("environment", "string")),
        "calculator", new Tool("calculator", "Math calculations", "utility", Map.of("expression", "string")),
        "sql_query", new Tool("sql_query", "Execute SQL", "data", Map.of("query", "string"))
    );

    static final Map<String, List<String>> PHASE_TOOLS = Map.of(
        "planning", List.of("web_search", "code_search", "calculator"),
        "implementation", List.of("read_file", "write_file", "code_search"),
        "testing", List.of("read_file", "run_tests", "code_search"),
        "deployment", List.of("run_tests", "deploy", "read_file"),
        "analysis", List.of("sql_query", "calculator", "web_search")
    );

    record AgentState(String task, String phase, List<String> history) {}

    static List<Tool> selectToolsByPhase(AgentState state) {
        return PHASE_TOOLS.getOrDefault(state.phase(), List.of())
            .stream()
            .map(TOOL_REGISTRY::get)
            .filter(Objects::nonNull)
            .toList();
    }

    static List<Tool> selectToolsByKeywords(AgentState state) {
        String text = (state.task() + " " + String.join(" ", state.history())).toLowerCase();
        Map<String, List<String>> keywordMap = Map.of(
            "search|find|look up|research", List.of("web_search", "code_search"),
            "read|open|view|inspect", List.of("read_file"),
            "write|create|modify|update|edit", List.of("write_file", "read_file"),
            "test|spec|assert|validate", List.of("run_tests", "read_file"),
            "deploy|release|publish|ship", List.of("deploy", "run_tests"),
            "calculate|compute|math|sum|average", List.of("calculator"),
            "query|database|sql|select|join", List.of("sql_query")
        );

        Set<String> selected = new LinkedHashSet<>();
        for (var entry : keywordMap.entrySet()) {
            if (Pattern.compile(entry.getKey()).matcher(text).find()) {
                selected.addAll(entry.getValue());
            }
        }

        if (selected.isEmpty()) {
            selected.addAll(PHASE_TOOLS.getOrDefault(state.phase(), List.of("web_search")));
        }

        return selected.stream()
            .map(TOOL_REGISTRY::get)
            .filter(Objects::nonNull)
            .toList();
    }

    static String formatToolsForPrompt(List<Tool> tools) {
        return tools.stream()
            .map(t -> {
                String params = t.parameters().entrySet().stream()
                    .map(e -> e.getKey() + ": " + e.getValue())
                    .collect(Collectors.joining(", "));
                return "- " + t.name() + "(" + params + "): " + t.description();
            })
            .collect(Collectors.joining("\n"));
    }

    public static void main(String[] args) {
        var state = new AgentState(
            "Find all Python files with SQL injection vulnerabilities and fix them",
            "implementation",
            List.of("Found 3 files with raw SQL queries")
        );

        var tools = selectToolsByKeywords(state);
        System.out.println("Selected " + tools.size() + " tools:");
        tools.forEach(t -> System.out.println("  " + t.name() + ": " + t.description()));
        System.out.println("\nFormatted for prompt:");
        System.out.println(formatToolsForPrompt(tools));
    }
}
