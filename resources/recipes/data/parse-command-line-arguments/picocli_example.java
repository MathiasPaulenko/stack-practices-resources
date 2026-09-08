// picocli example: annotation-based CLI with subcommands
// Maven: info.picocli:picocli:4.7.6

import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;
import picocli.CommandLine.Parameters;
import java.util.concurrent.Callable;

@Command(
    name = "mytool",
    mixinStandardHelpOptions = true,
    version = "1.0.0",
    subcommands = {PushCommand.class, PullCommand.class}
)
public class picocli_example implements Callable<Integer> {

    @Parameters(index = "0", description = "Input file path")
    private String input;

    @Option(names = {"-o", "--output"}, defaultValue = "out.txt", description = "Output file path")
    private String output;

    @Option(names = {"-v", "--verbose"}, description = "Verbose logging")
    private boolean verbose;

    @Override
    public Integer call() {
        System.out.printf("Input: %s, Output: %s, Verbose: %b%n", input, output, verbose);
        return 0;
    }

    public static void main(String[] args) {
        int exitCode = new CommandLine(new picocli_example()).execute(args);
        System.exit(exitCode);
    }
}

@Command(name = "push", mixinStandardHelpOptions = true, description = "Push to remote")
class PushCommand implements Callable<Integer> {

    @Option(names = "--force", description = "Force push")
    private boolean force;

    @Override
    public Integer call() {
        System.out.printf("Pushing (force: %b)%n", force);
        return 0;
    }
}

@Command(name = "pull", mixinStandardHelpOptions = true, description = "Pull from remote")
class PullCommand implements Callable<Integer> {

    @Option(names = "--depth", defaultValue = "1", description = "Clone depth")
    private int depth;

    @Override
    public Integer call() {
        System.out.printf("Pulling (depth: %d)%n", depth);
        return 0;
    }
}
