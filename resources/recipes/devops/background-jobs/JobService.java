import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

/**
 * Scheduled and async background jobs for the background-jobs recipe.
 * Requires @EnableScheduling on a @Configuration class.
 */
@Service
public class JobService {

    // Cron job: runs every day at 02:00
    @Scheduled(cron = "0 0 2 * * ?")
    public void cleanupOldLogs() {
        System.out.println("Running nightly cleanup");
    }

    // Fixed rate: runs every 5 minutes
    @Scheduled(fixedRate = 300_000)
    public void syncExternalData() {
        System.out.println("Syncing with external API");
    }

    // Fire-and-forget work inside a request goes through a pool
    public void runAsync(Runnable task, ThreadPoolTaskExecutor executor) {
        CompletableFuture.runAsync(task, executor);
    }
}
