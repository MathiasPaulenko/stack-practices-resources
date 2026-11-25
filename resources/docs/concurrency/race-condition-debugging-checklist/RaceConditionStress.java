import org.openjdk.jcstress.annotations.*;
import org.openjdk.jcstress.infra.results.II_Result;

// jcstress memory-model test (section 2.3 of the checklist).
// Runs both actors under every legal interleaving the JVM can produce.
// The "0, 0" outcome is forbidden: if it shows up even once, the code is
// broken and that trace is a real execution, not a theoretical one.
//
// Run with the jcstress Maven/Gradle harness; see
// https://openjdk.org/projects/code-tools/jcstress/
@JCStressTest
@Outcome(id = "1, 1", expect = Expect.ACCEPTABLE, desc = "Sequential")
@Outcome(id = "0, 1", expect = Expect.ACCEPTABLE, desc = "Writer first")
@Outcome(id = "1, 0", expect = Expect.ACCEPTABLE, desc = "Reader first")
@Outcome(id = "0, 0", expect = Expect.FORBIDDEN, desc = "Race condition")
@State
public class RaceConditionStress {
    int x = 0;
    int y = 0;

    @Actor
    public void actor1() {
        x = 1;
        y = 1;
    }

    @Actor
    public void actor2(II_Result r) {
        r.r1 = y;
        r.r2 = x;
    }
}
