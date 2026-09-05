use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "deploy-cli", version = "1.0.0", about = "CLI for app deployments")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Deploy to an environment
    Deploy {
        /// Target environment
        #[arg(value_enum)]
        environment: Environment,

        /// App version
        #[arg(short, long, default_value = "latest")]
        version: String,

        /// Simulate without changes
        #[arg(long)]
        dry_run: bool,
    },
}

#[derive(clap::ValueEnum, Clone)]
enum Environment {
    Dev,
    Staging,
    Prod,
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Deploy {
            environment,
            version,
            dry_run,
        } => {
            println!("Deploying {} to {:?}", version, environment);
            if dry_run {
                println!("(dry run mode)");
            }
        }
    }
}
