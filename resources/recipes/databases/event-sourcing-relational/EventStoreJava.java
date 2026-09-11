package com.stackpractices.eventsourcing;

import jakarta.persistence.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Event sourcing implementation for SQL Server with Spring.
 * Provides optimistic concurrency, event replay, and snapshot support.
 */
class ConcurrencyException extends RuntimeException {
    ConcurrencyException(String message) { super(message); }
}

@Entity
@Table(name = "events")
public class EventEntity {
    @Id private UUID id;
    private UUID aggregateId;
    private String eventType;
    @Column(columnDefinition = "nvarchar(max)")
    private String payload;
    private int version;
    private Instant occurredAt;

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getAggregateId() { return aggregateId; }
    public void setAggregateId(UUID aggregateId) { this.aggregateId = aggregateId; }
    public String getEventType() { return eventType; }
    public void setEventType(String eventType) { this.eventType = eventType; }
    public String getPayload() { return payload; }
    public void setPayload(String payload) { this.payload = payload; }
    public int getVersion() { return version; }
    public void setVersion(int version) { this.version = version; }
    public Instant getOccurredAt() { return occurredAt; }
    public void setOccurredAt(Instant occurredAt) { this.occurredAt = occurredAt; }
}

interface EventRepository {
    int countByAggregateId(UUID aggregateId);
    List<EventEntity> findByAggregateIdOrderByVersionAsc(UUID aggregateId);
    List<EventEntity> findByAggregateIdAndVersionGreaterThanOrderByVersionAsc(UUID aggregateId, int version);
}

interface SnapshotRepository {
    Optional<Snapshot> findTopByAggregateIdOrderByVersionDesc(UUID aggregateId);
}

class Snapshot {
    private UUID aggregateId;
    private int version;
    private String state;
    public int getVersion() { return version; }
    public String getState() { return state; }
}

class AccountState {
    private int balance;
    AccountState(int balance) { this.balance = balance; }
    public int getBalance() { return balance; }
    public void setBalance(int balance) { this.balance = balance; }
}

@Service
public class EventStore {
    private final EventRepository repo;

    public EventStore(EventRepository repo) { this.repo = repo; }

    @Transactional
    public void append(UUID aggregateId, String eventType, String payload, Integer expectedVersion) {
        int currentVersion = repo.countByAggregateId(aggregateId);
        if (expectedVersion != null && currentVersion != expectedVersion) {
            throw new ConcurrencyException("Expected " + expectedVersion + ", found " + currentVersion);
        }

        EventEntity event = new EventEntity();
        event.setId(UUID.randomUUID());
        event.setAggregateId(aggregateId);
        event.setEventType(eventType);
        event.setPayload(payload);
        event.setVersion(currentVersion + 1);
        event.setOccurredAt(Instant.now());
        repo.save(event);
    }

    public List<EventEntity> getEvents(UUID aggregateId) {
        return repo.findByAggregateIdOrderByVersionAsc(aggregateId);
    }

    public List<EventEntity> getEventsSince(UUID aggregateId, int version) {
        return repo.findByAggregateIdAndVersionGreaterThanOrderByVersionAsc(aggregateId, version);
    }
}

@Service
public class SnapshotService {
    private final EventStore eventStore;
    private final SnapshotRepository snapshotRepo;

    public SnapshotService(EventStore eventStore, SnapshotRepository snapshotRepo) {
        this.eventStore = eventStore;
        this.snapshotRepo = snapshotRepo;
    }

    public AccountState rebuildState(UUID accountId) {
        Optional<Snapshot> snapshot = snapshotRepo
            .findTopByAggregateIdOrderByVersionDesc(accountId);

        int startVersion = snapshot.map(Snapshot::getVersion).orElse(0);
        AccountState state = new AccountState(0);

        List<EventEntity> events = eventStore.getEventsSince(accountId, startVersion);

        for (EventEntity event : events) {
            state = applyEvent(state, event);
        }
        return state;
    }

    private AccountState applyEvent(AccountState state, EventEntity event) {
        // Apply event payload to state based on event type
        return state;
    }
}
