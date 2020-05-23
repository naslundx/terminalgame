import curses
from random import randint
import terminalgame


world = terminalgame.World(
    fps=10,
    # render=False
)

snake = terminalgame.Player(
    x=world.width // 5,
    y=world.height // 3,
    sign='X'
)

tail = [
    terminalgame.Object(x=snake.x-1, y=snake.y, sign='x'),
    terminalgame.Object(x=snake.x-2, y=snake.y, sign='x')
]

foods = []
for _ in range(3):
    foods.append(terminalgame.Object(x=randint(1, world.width - 1), y=randint(1, world.height - 1), sign='O'))

key = curses.KEY_RIGHT

with world.renderer():
    while world.tick():
        # What direction are we moving?
        key = key if not world.keypress else world.keypress

        # Stop if we hit the edge or ourself
        if snake.x in (0, world.width) or snake.y in (0, world.height) or snake.xy in (t.xy for t in tail):
            world.lose()

        # Move
        if key == curses.KEY_DOWN:
            snake.y += 1
        if key == curses.KEY_UP:
            snake.y -= 1
        if key == curses.KEY_LEFT:
            snake.x -= 1
        if key == curses.KEY_RIGHT:
            snake.x += 1
        
        # Update the front of the tail
        tail.insert(0, terminalgame.Object(x=snake._oldx, y=snake._oldy, sign='x'))

        # Check if we ate food
        ate_food = False
        for i, food in enumerate(foods):
            if snake.xy == food.xy:
                ate_food = True
            while food.xy in [t.xy for t in tail]:
                food.x, food.y = randint(1, world.width - 1), randint(1, world.height - 1)

        if not ate_food:
            tail.pop().destroy()
