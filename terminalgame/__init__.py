import terminalgame.mappings

from .actions import Action
from .object import Object
from .player import Player
from .world import World


from importlib.metadata import version

try:
    __version__ = version(__name__)
except:  # pylint: disable=bare-except
    pass
