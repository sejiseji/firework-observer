from __future__ import annotations

from abc import ABC, abstractmethod

from pyxel_goal_game.input.controls import Controls


class Scene(ABC):
    @abstractmethod
    def update(self, controls: Controls) -> None:
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError
