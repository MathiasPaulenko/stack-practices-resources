import org.junit.jupiter.api.extension.*;
import java.lang.reflect.Method;

public class RetryExtension implements InvocationInterceptor {

    private static final int MAX_RETRIES = 3;

    @Override
    public void interceptTestTemplateMethod(
            Invocation<Void> invocation,
            ReflectiveInvocationContext<Method> invocationContext,
            ExtensionContext extensionContext) throws Throwable {

        Throwable lastError = null;
        for (int attempt = 1; attempt <= MAX_RETRIES; attempt++) {
            try {
                invocation.proceed();
                return;
            } catch (Throwable t) {
                lastError = t;
                System.out.printf("Attempt %d failed: %s%n", attempt, t.getMessage());
            }
        }
        throw lastError;
    }
}
