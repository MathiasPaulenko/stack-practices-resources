import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

@SpringBootApplication
@RestController
public class Server {
    private final CopyOnWriteArrayList<SseEmitter> emitters = new CopyOnWriteArrayList<>();
    private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();

    @GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamEvents() {
        SseEmitter emitter = new SseEmitter(0L);
        emitters.add(emitter);

        emitter.onCompletion(() -> emitters.remove(emitter));
        emitter.onTimeout(() -> emitters.remove(emitter));
        emitter.onError((e) -> emitters.remove(emitter));

        scheduler.scheduleAtFixedRate(() -> {
            try {
                long id = System.currentTimeMillis();
                emitter.send(SseEmitter.event()
                    .id(String.valueOf(id))
                    .data("{\"message\": \"Update " + id + "\"}"));
            } catch (IOException e) {
                emitters.remove(emitter);
            }
        }, 0, 2, TimeUnit.SECONDS);

        return emitter;
    }

    @GetMapping("/publish/{message}")
    public String publish(@PathVariable String message) {
        for (SseEmitter emitter : emitters) {
            try {
                emitter.send(SseEmitter.event().data(message));
            } catch (IOException e) {
                emitters.remove(emitter);
            }
        }
        return "{\"published\": " + emitters.size() + "}";
    }

    public static void main(String[] args) {
        SpringApplication.run(Server.class, args);
    }
}
