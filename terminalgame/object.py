from typing import Dict

import terminalgame.world


class Object:
    def __init__(
        self, x: int, y: int, sign: str, mapping: Dict[str, terminalgame.Action] = None
    ):
        assert len(sign) == 1

        self._oldx = self._x = x
        self._oldy = self._y = y
        self.sign = sign
        self.mapping = mapping

        self.__register()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._oldx = self._x
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._oldy = self._y
        self._y = value

    @property
    def xy(self):
        return self._x, self._y

    def destroy(self):
        self.x = None
        self.y = None

    def tick(self):
        self._oldx = self._x
        self._oldy = self._y

    @property
    def has_moved(self):
        return self._oldx != self._x or self._oldy != self._y

    @property
    def is_destroyed(self):
        return self._x is None and self._y is None

    def __register(self):
        terminalgame.world.World.instance.register(self)
