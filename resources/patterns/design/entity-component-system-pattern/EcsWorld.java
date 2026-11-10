import java.util.*;

/**
 * Minimal Entity-Component-System world in Java.
 * Companion runnable for https://stackpractices.com/patterns/entity-component-system-pattern/
 *
 * An entity is just an ID. Components are pure data. Systems iterate the
 * entities that carry the components they need.
 */

class PositionComponent {
    float x, y;
    PositionComponent(float x, float y) { this.x = x; this.y = y; }
}

class VelocityComponent {
    float vx, vy;
    VelocityComponent(float vx, float vy) { this.vx = vx; this.vy = vy; }
}

class HealthComponent {
    int hp, maxHp;
    HealthComponent(int hp, int maxHp) { this.hp = hp; this.maxHp = maxHp; }
}

class EcsWorld {
    private final Map<UUID, Map<Class<?>, Object>> entities = new HashMap<>();
    private final List<EcsSystem> systems = new ArrayList<>();

    public UUID createEntity() {
        UUID id = UUID.randomUUID();
        entities.put(id, new HashMap<>());
        return id;
    }

    public void addComponent(UUID entity, Object component) {
        entities.get(entity).put(component.getClass(), component);
    }

    @SuppressWarnings("unchecked")
    public <T> T getComponent(UUID entity, Class<T> type) {
        return (T) entities.get(entity).get(type);
    }

    public List<UUID> query(Class<?>... types) {
        List<UUID> result = new ArrayList<>();
        for (Map.Entry<UUID, Map<Class<?>, Object>> entry : entities.entrySet()) {
            boolean hasAll = true;
            for (Class<?> type : types) {
                if (!entry.getValue().containsKey(type)) {
                    hasAll = false;
                    break;
                }
            }
            if (hasAll) result.add(entry.getKey());
        }
        return result;
    }

    public void addSystem(EcsSystem system) {
        systems.add(system);
    }

    public void update(float dt) {
        for (EcsSystem system : systems) system.update(this, dt);
    }
}

abstract class EcsSystem {
    abstract void update(EcsWorld world, float dt);
}

class MovementSystem extends EcsSystem {
    void update(EcsWorld world, float dt) {
        for (UUID eid : world.query(PositionComponent.class, VelocityComponent.class)) {
            PositionComponent pos = world.getComponent(eid, PositionComponent.class);
            VelocityComponent vel = world.getComponent(eid, VelocityComponent.class);
            pos.x += vel.vx * dt;
            pos.y += vel.vy * dt;
        }
    }
}

class DamageSystem extends EcsSystem {
    void update(EcsWorld world, float dt) {
        for (UUID eid : world.query(HealthComponent.class)) {
            HealthComponent health = world.getComponent(eid, HealthComponent.class);
            if (health.hp <= 0) {
                System.out.println("Entity " + eid + " destroyed");
            }
        }
    }
}

class Demo {
    public static void main(String[] args) {
        EcsWorld world = new EcsWorld();
        world.addSystem(new MovementSystem());
        world.addSystem(new DamageSystem());

        UUID player = world.createEntity();
        world.addComponent(player, new PositionComponent(0, 0));
        world.addComponent(player, new VelocityComponent(5, 0));
        world.addComponent(player, new HealthComponent(100, 100));

        world.update(1.0f);
        PositionComponent pos = world.getComponent(player, PositionComponent.class);
        System.out.println("Player position after 1s: (" + pos.x + ", " + pos.y + ")");
    }
}
