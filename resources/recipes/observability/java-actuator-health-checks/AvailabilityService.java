import org.springframework.boot.availability.ApplicationAvailability;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.LivenessState;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

@Service
public class AvailabilityService {

    private final ApplicationAvailability availability;
    private final ApplicationEventPublisher publisher;

    public AvailabilityService(ApplicationAvailability availability,
                               ApplicationEventPublisher publisher) {
        this.availability = availability;
        this.publisher = publisher;
    }

    @EventListener
    public void onLivenessChange(AvailabilityChangeEvent<LivenessState> event) {
        // e.g. stop background work while Kubernetes restarts us
    }

    @EventListener
    public void onReadinessChange(AvailabilityChangeEvent<ReadinessState> event) {
        // e.g. pause consuming from the queue while unready
    }

    public void markUnready() {
        AvailabilityChangeEvent.publish(
            publisher, this, ReadinessState.REFUSING_TRAFFIC
        );
    }
}
