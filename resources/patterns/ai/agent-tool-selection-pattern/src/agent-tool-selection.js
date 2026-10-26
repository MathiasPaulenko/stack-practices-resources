class Tool {
  constructor(name, description, category, parameters = {}) {
    this.name = name;
    this.description = description;
    this.category = category;
    this.parameters = parameters;
  }
}

const TOOL_REGISTRY = {
  web_search: new Tool("web_search", "Search the web", "research", { query: "string", maxResults: "int" }),
  code_search: new Tool("code_search", "Search codebase", "research", { pattern: "string", language: "string" }),
  read_file: new Tool("read_file", "Read file contents", "file_ops", { path: "string" }),
  write_file: new Tool("write_file", "Write to file", "file_ops", { path: "string", content: "string" }),
  run_tests: new Tool("run_tests", "Execute tests", "execution", { testFile: "string", filter: "string" }),
  deploy: new Tool("deploy", "Deploy app", "execution", { environment: "string", version: "string" }),
  calculator: new Tool("calculator", "Math calculations", "utility", { expression: "string" }),
  sql_query: new Tool("sql_query", "Execute SQL", "data", { query: "string", database: "string" }),
};

const PHASE_TOOLS = {
  planning: ["web_search", "code_search", "calculator"],
  implementation: ["read_file", "write_file", "code_search"],
  testing: ["read_file", "run_tests", "code_search"],
  deployment: ["run_tests", "deploy", "read_file"],
  analysis: ["sql_query", "calculator", "web_search"],
};

function selectToolsByPhase(state) {
  const names = PHASE_TOOLS[state.phase] || [];
  return names.map(n => TOOL_REGISTRY[n]).filter(Boolean);
}

function selectToolsByKeywords(state) {
  const text = (state.task + " " + state.history.join(" ")).toLowerCase();

  const keywordMap = {
    "search|find|look up|research": ["web_search", "code_search"],
    "read|open|view|inspect": ["read_file"],
    "write|create|modify|update|edit": ["write_file", "read_file"],
    "test|spec|assert|validate": ["run_tests", "read_file"],
    "deploy|release|publish|ship": ["deploy", "run_tests"],
    "calculate|compute|math|sum|average": ["calculator"],
    "query|database|sql|select|join": ["sql_query"],
  };

  const selected = new Set();
  for (const [pattern, tools] of Object.entries(keywordMap)) {
    if (new RegExp(pattern).test(text)) {
      tools.forEach(t => selected.add(t));
    }
  }

  if (selected.size === 0) {
    (PHASE_TOOLS[state.phase] || ["web_search"]).forEach(t => selected.add(t));
  }

  return [...selected].map(n => TOOL_REGISTRY[n]).filter(Boolean);
}

class ToolSelector {
  constructor(strategy = "phase") {
    this.strategy = strategy;
  }

  select(state) {
    if (this.strategy === "phase") return selectToolsByPhase(state);
    if (this.strategy === "keyword") return selectToolsByKeywords(state);
    return Object.values(TOOL_REGISTRY);
  }

  formatToolsForPrompt(tools) {
    return tools
      .map(t => {
        const params = Object.entries(t.parameters)
          .map(([k, v]) => `${k}: ${v}`)
          .join(", ");
        return `- ${t.name}(${params}): ${t.description}`;
      })
      .join("\n");
  }
}

// Usage
const state = {
  task: "Find all Python files with SQL injection vulnerabilities and fix them",
  phase: "implementation",
  history: ["Found 3 files with raw SQL queries"],
};

const selector = new ToolSelector("keyword");
const tools = selector.select(state);

console.log(`Selected ${tools.length} tools:`);
tools.forEach(t => console.log(`  ${t.name}: ${t.description}`));

console.log("\nFormatted for prompt:");
console.log(selector.formatToolsForPrompt(tools));
