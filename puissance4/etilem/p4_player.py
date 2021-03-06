# coding: utf-8
# pylint: disable=c0103
"""
module de joueur
"""

from p4_config import SPRITE

class Player:
    """
    Joueur, humain ou machine
    """

    def __init__(self, code):
        self.code = code
        self.sprite = SPRITE[self.code]
