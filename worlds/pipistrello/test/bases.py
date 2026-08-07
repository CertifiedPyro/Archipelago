from test.bases import WorldTestBase

from ..world import PipWorld


class PipTestBase(WorldTestBase):
    game = "Pipistrello and the Cursed Yoyo"
    world: PipWorld
