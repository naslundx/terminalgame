import curses
from contextlib import contextmanager
from time import sleep
from typing import List, Tuple, TYPE_CHECKING

from .actions import Action
from .properties import Property

if TYPE_CHECKING:
    from .object import Object


class World:
    class __World:
        def __init__(self, fps: int, render: bool = True):
            self.fps = fps
            self._objects: List[Object] = []
            self._draw_queue: List[Tuple[int, int, str]] = []
            self.running = True
            self._window = None
            self._height, self._width = 50, 80  # s.getmaxyx()
            self._key = None

            if render:
                _ = curses.initscr()
                curses.curs_set(0)
                self._window = curses.newwin(self._height, self._width, 0, 0)
                self._window.keypad(True)
                self._window.timeout(1000 // self.fps)

        def register(self, obj: "Object"):
            assert obj not in self._objects

            self._objects.append(obj)
            self._draw_queue.append((obj.x, obj.y, obj.sign))

        def get_properties(self, x: int, y: int) -> List[Property]:
            for o in self._objects:
                if o.xy == (x, y) and not o.is_destroyed:
                    return o.properties[:]
            return []

        def draw(self):
            while self._draw_queue:
                x, y, s = self._draw_queue.pop()
                if self._window:
                    if x in range(0, self.width) and y in range(0, self.height):
                        self._window.addch(y, x, s)
                else:
                    print(x, y, s)

        def tick(self):
            # Handle keypress mapping
            key = self.keypress
            if key:
                for obj in (o for o in self._objects if o.mapping):
                    if key in obj.mapping:
                        new_x, new_y = obj.x, obj.y
                        action = obj.mapping[key]
                        if action == Action.MOVE_UP:
                            new_y -= 1
                        if action == Action.MOVE_DOWN:
                            new_y += 1
                        if action == Action.MOVE_LEFT:
                            new_x -= 1
                        if action == Action.MOVE_RIGHT:
                            new_x += 1
                        if Property.SOLID not in self.get_properties(new_x, new_y):
                            obj.x, obj.y = new_x, new_y

            # Update draw queue
            for obj in self._objects:
                if obj.is_destroyed:
                    self._draw_queue.append((obj._oldx, obj._oldy, " "))
                elif obj.has_moved:
                    self._draw_queue.append((obj._oldx, obj._oldy, " "))
                    self._draw_queue.append((obj.x, obj.y, obj.sign))

                obj.tick()

            # Render
            self.draw()

            # Remove destroyed objects
            self._objects = [o for o in self._objects if not o.is_destroyed]

            # Get keypress
            if self._window:
                self._key = self._window.getch()
            else:
                sleep(1.0 / self.fps)
                self._key = None

            return self.running

        def quit(self):
            self.running = False
            if self._window:
                curses.endwin()
                self._window = False

        @property
        def width(self):
            return self._width

        @property
        def height(self):
            return self._height

        @property
        def keypress(self):
            return self._key if self._key != -1 else None

    instance = None

    def __init__(self, *args, **kwargs):
        assert not World.instance
        World.instance = World.__World(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    @contextmanager
    def renderer(self):
        try:
            yield self
        finally:
            self.quit()
