import io.micrometer.core.aop.CountedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// TimedAspect comes from Spring Boot's MetricsAspectAutoConfiguration —
// only @Counted needs an explicit bean. Declaring TimedAspect here too
// would just register a duplicate.
@Configuration
public class MetricsConfig {

    @Bean
    public CountedAspect countedAspect(MeterRegistry registry) {
        return new CountedAspect(registry);
    }
}
