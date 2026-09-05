const { Command } = require("commander");
const program = new Command();

program.name("deploy-cli").description("CLI for app deployments").version("1.0.0");

program
  .command("deploy <environment>")
  .description("Deploy to an environment")
  .option("-v, --version <ver>", "App version", "latest")
  .option("--dry-run", "Simulate without changes", false)
  .option("--verbose", "Verbose output", false)
  .action((environment, options) => {
    console.log(`Deploying ${options.version} to ${environment}`);
    if (options.dryRun) console.log("(dry run mode)");
  });

program.parse();
