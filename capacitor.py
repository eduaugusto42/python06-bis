#!/usr/bin/env python3

from ex3 import TransformCreatureFactory
from ex3.capabilities import TransformCapability


def main() -> None:
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")
    for label, entity in [("base", base), ("evolved", evolved)]:
        print(f"{label}:")
        print(entity.describe())
        print(entity.attack())
        if not isinstance(entity, TransformCapability):
            raise TypeError("entity cannot transform")
        print(entity.transform())
        print(entity.attack())
        print(entity.revert())


if __name__ == "__main__":
    main()
