import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;
import java.util.concurrent.Callable;

@Command(
    name = "deploy-cli",
    description = "CLI for app deployments",
    version = "1.0.0",
    mixinStandardHelpOptions = true)
public class DeployCli implements Callable<Integer> {

    @Parameters(index = "0", description = "Target environment")
    private String environment;

    @Option(names = {"-v", "--version"}, defaultValue = "latest", description = "App version")
    private String version;

    @Option(names = "--dry-run", description = "Simulate without changes")
    private boolean dryRun;

    @Option(names = {"-V", "--verbose"}, description = "Verbose output")
    private boolean verbose;

    @Override
    public Integer call() {
        System.out.printf("Deploying %s to %s%n", version, environment);
        if (dryRun) System.out.println("(dry run mode)");
        return 0;
    }

    public static void main(String[] args) {
        int exitCode = new CommandLine(new DeployCli()).execute(args);
        System.exit(exitCode);
    }
}
