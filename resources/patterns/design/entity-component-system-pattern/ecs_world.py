"""Minimal Entity-Component-System world in Python.

Companion runnable for https://stackpractices.com/patterns/entity-component-system-pattern/

An entity is just an ID. Components are pure data. Systems iterate the
entities that carry the components they need.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Type
from uuid import uuid4


# --- Components (pure data) -------------------------------------------------

@dataclass
class PositionComponent:
    x: float = 0.0
    y: float = 0.0


@dataclass
class VelocityComponent:
    vx: float = 0.0
    vy: float = 0.0


@dataclass
class HealthComponent:
    hp: int = 100
    max_hp: int = 100


@dataclass
class FlyingComponent:
    altitude: float = 0.0


# --- World ------------------------------------------------------------------

EntityId = str


class World:
    def __init__(self) -> None:
        self._entities: Dict[EntityId, Dict[Type, Any]] = {}
        self._systems: List["System"] = []

    def create_entity(self) -> EntityId:
        eid = str(uuid4())
        self._entities[eid] = {}
        return eid

    def add_component(self, entity: EntityId, component: Any) -> None:
        self._entities[entity][type(component)] = component

    def get_component(self, entity: EntityId, component_type: Type) -> Any:
        return self._entities[entity].get(component_type)

    def query(self, *component_types: Type) -> List[EntityId]:
        return [
            eid
            for eid, comps in self._entities.items()
            if all(ct in comps for ct in component_types)
        ]

    def add_system(self, system: "System") -> None:
        self._systems.append(system)

    def update(self, dt: float) -> None:
        for system in self._systems:
            system.update(self, dt)


# --- Systems ----------------------------------------------------------------

class System:
    def update(self, world: World, dt: float) -> None:
        raise NotImplementedError


class MovementSystem(System):
    def update(self, world: World, dt: float) -> None:
        for eid in world.query(PositionComponent, VelocityComponent):
            pos = world.get_component(eid, PositionComponent)
            vel = world.get_component(eid, VelocityComponent)
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt


class DamageSystem(System):
    def update(self, world: World, dt: float) -> None:
        for eid in world.query(HealthComponent):
            health = world.get_component(eid, HealthComponent)
            if health.hp <= 0:
                print(f"Entity {eid} destroyed")


# --- Demo -------------------------------------------------------------------

if __name__ == "__main__":
    world = World()
    world.add_system(MovementSystem())
    world.add_system(DamageSystem())

    player = world.create_entity()
    world.add_component(player, PositionComponent(0, 0))
    world.add_component(player, VelocityComponent(5, 0))
    world.add_component(player, HealthComponent(100, 100))

    world.update(1.0)
    pos = world.get_component(player, PositionComponent)
    print(f"Player position after 1s: ({pos.x}, {pos.y})")  # (5.0, 0.0)

    # Runtime flexibility: attach a component, no new class needed
    world.add_component(player, FlyingComponent())
    print("Player can now fly:", world.get_component(player, FlyingComponent) is not None)
