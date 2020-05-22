import curses

from terminalgame.actions import Action

MOVE_BY_ARROW = {
    curses.KEY_DOWN: Action.MOVE_DOWN,
    curses.KEY_UP: Action.MOVE_UP,
    curses.KEY_LEFT: Action.MOVE_LEFT,
    curses.KEY_RIGHT: Action.MOVE_RIGHT,
}
