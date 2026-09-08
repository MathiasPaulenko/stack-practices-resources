// Commander.js example: fluent API with subcommands
// npm install commander

const { Command } = require("commander");

function buildProgram() {
  const program = new Command();

  program
    .name("mytool")
    .description("Process files")
    .version("1.0.0");

  program
    .argument("<input>", "Input file path")
    .option("-o, --output <file>", "Output file path", "out.txt")
    .option("-v, --verbose", "Enable verbose logging")
    .action((input, options) => {
      console.log(`Input: ${input}, Output: ${options.output}, Verbose: ${!!options.verbose}`);
    });

  program
    .command("push")
    .description("Push to remote")
    .option("--force", "Force push")
    .action((options) => {
      console.log(`Pushing (force: ${!!options.force})`);
    });

  program
    .command("pull")
    .description("Pull from remote")
    .option("--depth <n>", "Clone depth", "1")
    .action((options) => {
      console.log(`Pulling (depth: ${options.depth})`);
    });

  return program;
}

if (require.main === module) {
  buildProgram().parse();
}

module.exports = { buildProgram };
