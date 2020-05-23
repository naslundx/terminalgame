from random import randint
from time import sleep
import terminalgame

world = terminalgame.World(
    fps=10,
    render=True
)

player = terminalgame.Player(x=0, y=0, sign="X", mapping=terminalgame.mappings.MOVE_BY_ARROW)

width, height = 16, 16  # world.width, world.height
START = (0, 0)
GOAL = (width, height)
walls = [START]

current = START
direction = randint(1, 2)  # 0 = LEFT, 1 = RIGHT, 2 = DOWN
while current != GOAL:
    x, y = current
    if direction == 1 and (x + 1, y) not in walls and (x + 2, y) not in walls and x + 2 <= width:
        walls.append((x + 1, y))
        walls.append((x + 2, y))
        current = (x+2, y)
    elif direction == 0 and (x - 1, y) not in walls and (x - 2, y) not in walls and x - 2 >= 0 and y < height:
        walls.append((x - 1, y))
        walls.append((x - 2, y))
        current = (x-2, y)
    elif direction == 2 and (x, y + 1) not in walls and (x, y + 2) not in walls and y + 2 <= height:
        walls.append((x, y + 1))
        walls.append((x, y + 2))
        current = (x, y + 2)

    direction = randint(0, 2) 

for x in range(width + 1):
    for y in range(height + 1):
        if (x, y) not in walls:
            terminalgame.Object(x=x, y=y, sign="#", properties=[terminalgame.Property.SOLID])

terminalgame.Object(x=x, y=y, sign="O")      

with world.renderer():
    while world.tick():
        if player.xy == GOAL:
            world.quit()
