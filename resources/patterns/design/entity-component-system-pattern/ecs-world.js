/**
 * Minimal Entity-Component-System world in JavaScript.
 * Companion runnable for https://stackpractices.com/patterns/entity-component-system-pattern/
 *
 * An entity is just an ID. Components are pure data. Systems iterate the
 * entities that carry the components they need.
 */

class PositionComponent {
  constructor(x = 0, y = 0) {
    this.x = x;
    this.y = y;
  }
}

class VelocityComponent {
  constructor(vx = 0, vy = 0) {
    this.vx = vx;
    this.vy = vy;
  }
}

class HealthComponent {
  constructor(hp = 100, maxHp = 100) {
    this.hp = hp;
    this.maxHp = maxHp;
  }
}

class FlyingComponent {
  constructor(altitude = 0) {
    this.altitude = altitude;
  }
}

class World {
  constructor() {
    this.entities = new Map();
    this.systems = [];
  }

  createEntity() {
    const id = crypto.randomUUID();
    this.entities.set(id, new Map());
    return id;
  }

  addComponent(entity, component) {
    this.entities.get(entity).set(component.constructor, component);
  }

  getComponent(entity, componentType) {
    return this.entities.get(entity).get(componentType);
  }

  query(...componentTypes) {
    const result = [];
    for (const [eid, components] of this.entities) {
      if (componentTypes.every((type) => components.has(type))) {
        result.push(eid);
      }
    }
    return result;
  }

  addSystem(system) {
    this.systems.push(system);
  }

  update(dt) {
    for (const system of this.systems) {
      system.update(this, dt);
    }
  }
}

class MovementSystem {
  update(world, dt) {
    for (const eid of world.query(PositionComponent, VelocityComponent)) {
      const pos = world.getComponent(eid, PositionComponent);
      const vel = world.getComponent(eid, VelocityComponent);
      pos.x += vel.vx * dt;
      pos.y += vel.vy * dt;
    }
  }
}

class DamageSystem {
  update(world, dt) {
    for (const eid of world.query(HealthComponent)) {
      const health = world.getComponent(eid, HealthComponent);
      if (health.hp <= 0) {
        console.log(`Entity ${eid} destroyed`);
      }
    }
  }
}

// Demo
const world = new World();
world.addSystem(new MovementSystem());
world.addSystem(new DamageSystem());

const player = world.createEntity();
world.addComponent(player, new PositionComponent(0, 0));
world.addComponent(player, new VelocityComponent(5, 0));
world.addComponent(player, new HealthComponent(100, 100));

world.update(1.0);
const pos = world.getComponent(player, PositionComponent);
console.log(`Player position after 1s: (${pos.x}, ${pos.y})`);

// Runtime flexibility: attach a component, no new class needed
world.addComponent(player, new FlyingComponent());
console.log("Player can now fly:", world.getComponent(player, FlyingComponent) !== undefined);
