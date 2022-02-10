"""
Module to generate rotations.
"""
import zeal.data as zd
import zeal.core as zc


class Rotation:
    """Class to hold rotations."""
    ca: zc.CombatAnalyser
    rankings: dict
    rankings_raw: dict

    def __init__(self, combat_analyser):
        self.ca = combat_analyser
        self.rankings = combat_analyser.rank_actions()
        self.rankings_raw = combat_analyser.rank_actions(normalise=False)



