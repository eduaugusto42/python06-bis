from abc import ABC, abstractmethod

from ex3.capabilities import TransformCapability
from ex3.creatures import Creature


class InvalidEntityError(Exception):
    """A strategy was asked to act on an incompatible creature."""


class BattleStrategy(ABC):
    @property
    def name(self) -> str:
        """Return the strategy name without the 'Strategy' suffix."""
        return type(self).__name__.removesuffix("Strategy")

    def _invalid(self, entity: Creature) -> InvalidEntityError:
        return InvalidEntityError(
            f"Invalid Creature '{entity.name}' for this "
            f"{self.name.lower()} strategy"
        )

    @abstractmethod
    def is_valid(self, entity: Creature) -> bool:
        """Report whether this strategy can act on the creature."""

    @abstractmethod
    def act(self, entity: Creature) -> None:
        """Perform this strategy's battle action."""


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, Creature)

    def act(self, entity: Creature) -> None:
        if not self.is_valid(entity):
            raise self._invalid(entity)
        print(entity.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Creature) -> bool:
        return isinstance(entity, TransformCapability)

    def act(self, entity: Creature) -> None:
        if not isinstance(entity, TransformCapability):
            raise self._invalid(entity)

        print(entity.transform())
        try:
            print(entity.attack())
        finally:
            print(entity.revert())
