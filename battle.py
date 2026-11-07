#!/usr/bin/env python3

from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing factory")
    print(base.describe())
    print(base.attack())

    print(evolved.describe())
    print(evolved.attack())


def battle(
    factory_a: CreatureFactory,
    factory_b: CreatureFactory,
) -> None:
    a = factory_a.create_base()
    b = factory_b.create_base()

    print("Testing battle")
    print(a.describe())
    print("vs.")
    print(b.describe())
    print("fight!")
    print(a.attack())
    print(b.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    test_factory(flame)
    print()
    test_factory(transform)
    print()
    battle(flame, transform)
