# coding: utf-8
# pylint: disable=c0103,r0913
"""
module de recherche de grille résolue
Auteur principal: Thierry Parmentelat (@parmentelat sur GitHub)
"""

from p4_config import LENGTH

def directions():
    """
    Génère les directions de recherche
    """
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                yield dx, dy

def solved(board, player, length=LENGTH):
    """
    Teste si la grille est résolue
    """
    for x, y in board.cases():
        for direction in directions():
            if has_n_in_dir(board, player, x, y, direction, length):
                return True
    return False

def has_n_in_dir(board, player, x, y, direction, n):
    """
    Teste si n jetons du joueur sont alignés dans une direction donnée
    """
    if n == 0:
        return True
    if not board.is_valid((x, y)):
        return False
    if board.grille[x][y] != player:
        return False
    dx, dy = direction
    return has_n_in_dir(board, player, x+dx, y+dy, direction, n-1)
