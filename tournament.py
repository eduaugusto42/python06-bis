#!/usr/bin/env python3

from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (AggressiveStrategy, BattleStrategy, InvalidEntityError,
                 NormalStrategy)


Opponent = tuple[CreatureFactory, BattleStrategy]


def format_opponents(opponents: list[Opponent]) -> str:
    """Format the opponent list exactly like the subject."""
    labels = [
        f"({factory.create_base().name}+{strategy.name})"
        for factory, strategy in opponents
    ]
    return "[ " + ", ".join(labels) + " ]"


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                factory_a, strategy_a = opponents[i]
                factory_b, strategy_b = opponents[j]

                entity_a = factory_a.create_base()
                entity_b = factory_b.create_base()

                print("* Battle *")
                print(entity_a.describe())
                print("vs.")
                print(entity_b.describe())
                print("now fight!")

                strategy_a.act(entity_a)
                strategy_b.act(entity_b)
    except InvalidEntityError as error:
        print(f"Battle error, aborting tournament: {error}")


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    basic: list[Opponent] = [
        (FlameFactory(), NormalStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    print(format_opponents(basic))
    print()
    battle(basic)

    print("\nTournament 1 (error)")
    error: list[Opponent] = [
        (TransformCreatureFactory(), AggressiveStrategy()),
        (FlameFactory(), AggressiveStrategy()),
    ]
    print(format_opponents(error))
    print()
    battle(error)
