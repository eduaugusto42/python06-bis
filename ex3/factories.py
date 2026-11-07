from abc import ABC, abstractmethod
from .creatures import Creature, Flameling, Pyrodon
from .capabilities import Shiftling, Morphagon


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        """Create a base creature."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create a evolved creature."""


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
