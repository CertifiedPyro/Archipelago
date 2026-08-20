from options import Difficulty, Moneysanity

from .bases import PipTestBase


class TestNormalLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_normal, "moneysanity": Moneysanity.option_true}


class TestHardLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_hard, "moneysanity": Moneysanity.option_true}


class TestExpertLogic(PipTestBase):
    options = {"difficulty": Difficulty.option_expert, "moneysanity": Moneysanity.option_true}
