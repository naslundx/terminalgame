import terminalgame

world = terminalgame.World(fps=10, render=True)

player = terminalgame.Player(
    x=world.width // 6, y=world.height // 6, sign="X", mapping=terminalgame.mappings.MOVE_BY_ARROW,
)

with world.renderer():
    while world.tick():
        pass
