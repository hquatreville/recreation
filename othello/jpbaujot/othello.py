# -*- coding: utf-8 -*-

# pour dire à pylint de ne pas vérifier la présence des docstring
# pylint: disable=c0111
# vérifier avec
# $ pip3 install pylint
# $ pylint othello.py
# il reste quelques identificateurs qui ne sont pas casher, je vous laisse
# choisir de les rectifier ou pas

# @parmentelat : dans une version déjà modifiee (simplifiée en code) , j'ai pris en compte vos suggestions sur les adjacents et le test d'appartenance
# mais je ne sais pas ce que vous entendez par identificateurs pas casher : pouver vous préciser les lignes concernées

"""
Created on Sun Oct  7 21:07:27 2018
Evolutions avec prise en compte compteur et fin de jeu , mais reste à debugguer ...
@author: JP
"""
import numpy as np


class Grille:
    # classe pour gerer la grille
    def __init__(self):
        self.tableau = np.zeros((8, 8))
        self.tableau[3][3], self.tableau[4][4] = 2, 2
        self.tableau[3][4], self.tableau[4][3] = 1, 1
        self.pions = [". ", "X ", "O "]

    def __str__(self):
        nom_col = "  A B C D E F G H\n"
        msg = "\n" + nom_col
        for i in range(8):
            msg += f"{i+1} "
            for j in range(8):
                msg += self.pions[int(self.tableau[i][j])]
            msg += f" {i+1}\n"
        msg += nom_col
        return msg

    @staticmethod
    def adjacents():
        # liste des caseTableau ajdacentes en relatif
        return [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]

    def pose_test(self, forme, ligne, colonne):
        # verifie si pose d'un pion forme permet ou pas de retouner
        # des pions del'autre forme et renvoie booleen sur la pose possible
        # et un  tableau des nombre de pions retournables
        # @jpbaudot:
        # tableauRetournables est un exemple de ce que j'appelais un
        # symbole non-casher; PEP8 recommande d'utiliser plutôt
        # tableau_retournables
        tableauRetournables = np.zeros((8))
        # teste caseTableau jouee non vide
        if int(self.tableau[ligne][colonne]):
            # ◘print("erreur : case  non vide")
            return False, tableauRetournables

        # @jpbaudot:
        # de même dx et dy sont considérés comme trop courts
        # ce sont des remarques émises dans mon environnement par pylint
        # naturellement ce sont juste des guidelines :)
        for idx, (dx, dy) in enumerate(self.adjacents()):
            # caseTableau adj hors grille
            if not self.test_caseTableau(ligne+dx, colonne+dy):
                continue
            formeAdjacent = self.tableau[ligne+dx][colonne+dy]
            if not formeAdjacent == 3-forme:  # caseTableau adj vide ou meme forme
                continue

            # caseTableau adj de forme differente, on teste les caseTableau audelà ds cette direction
            i = 2
            while self.test_caseTableau(ligne+i*dx, colonne+i*dy):
                formeAdjacent = self.tableau[ligne+i*dx][colonne+i*dy]
                if formeAdjacent == 0:  # on tombe sur caseTableau vide = mauvaise direction
                    break  # on regarde les autres caseTableau adjacentes
                if formeAdjacent == forme:
                    tableauRetournables[idx] = i-1
                    break  # on regarde les autres caseTableau adjacentes
                i += 1  # on continue dans la direction

        # toujours sur la forme, on évite les lignes kilométriques:
        # Retourne True si on peut  retourner des pions False sinon,
        # liste contenant les pions retournables
        return (sum(tableauRetournables) > 0), tableauRetournables

    def pose(self, forme, ligne, colonne):
        # verifie si pose d'un pion forme permet ou pas de retouner
        # des pions del'autre forme , retourne les pions si possibles et retourne
        # un booleen pour dire si le tableau a été modifié ou pas

        result, tableauRetournables = self.pose_test(forme, ligne, colonne)
        if result:  # remplit les caseTableau du tableau
            for idx, (dx, dy) in enumerate(self.adjacents()):
                for j in range(int(tableauRetournables[idx])+1):
                    self.tableau[ligne+j*dx][colonne+j*dy] = forme
        return result

    # choisissez votre camp
    # soit test_case_tableau, soit testCaseTableau :)
    def test_caseTableau(self, x, y):
        # teste si une caseTableau est bien dans la grille
        return not (x < 0 or x > 7 or y < 0 or y > 7)

    def partie_terminee(self):
        # teste si toutes caseTableau occupées : aucune caseTableau à 0 ou jeu bloqué pour les 2
        return self.tableau_rempli() or self.jeu_bloque()

    def jeu_bloque(self):
        # teste si les 2 JoueurHumains sont bloqués
        return not (self.teste_pose_possible(1) or self.teste_pose_possible(2))

    def teste_pose_possible(self, forme):
        # renvoie le nombre de pions retournables sur l'ensemble de la grille pour une forme(forme) donnée
        return (sum([self.pose_test(forme, i, j)[0]
                     for i in range(8) for j in range(8)
                     if not self.tableau[i][j]]))

    def tableau_rempli(self):
        # verifie si le tableau est bien rempli
        # pas de parenthèses
        return np.count_nonzero(self.tableau == 0) == 0

    def compte_formes(self):
        # renvoie un tuple des nombres de croix et de ronds
        totalCroix, totalRond = np.count_nonzero(
            self.tableau == 1), np.count_nonzero(self.tableau == 2)
        return f"Croix = {totalCroix} Rond = {totalRond} "

    def case_retournable(self, forme, ligne, colonne):
        # teste si case peut etre retournee  au tour  suivant
        # necessite une deeepcopie de la grille pour poser pion
        # puis chercher une solution de retournement
        pass


class Jeu:
    def __init__(self):
        self.grille = Grille()
        print(self.grille)
        # version à 2 humains , evoluera avec possibilité AI et donc choix demarrer ou pas

        while True:
            premierJoueur = input("Qui joue les croix ? Humain =0 ou AI = 1")
            if self.saisieJoueurValide(premierJoueur):
                break
        while True:
            deuxiemeJoueur = input("Qui joue les ronds ? Humain =0 ou AI = 1")
            if self.saisieJoueurValide(deuxiemeJoueur):
                break

        J1 = JoueurHumain(
            "Croix") if premierJoueur == '0' else JoueurAI("Croix")
        J2 = JoueurHumain(
            "Rond") if deuxiemeJoueur == '0' else JoueurAI("Rond")

        self.Joueurs = [J1, J2]

    def saisieJoueurValide(self, saisie):
        return len(saisie) == 1 and saisie in '01'

    def partie(self):
        # partie principale
        indexJoueur = 0  # les X commencent
        condstop = False
        while not self.grille.partie_terminee() and not condstop:
            print(f"Compteur :"+self.grille.compte_formes())

            joueur = self.Joueurs[indexJoueur]
            # verifie si pose pion possible pour le joueur
            if not joueur.joue_test(self):
                indexJoueur = 1-indexJoueur
                continue

            if joueur.joue():
                print(self.grille)
                indexJoueur = 1-indexJoueur
                continue
            condstop = True

        print(f"Compteur final :"+self.grille.compte_formes())


class Joueur:
    formes = ["Croix", "Rond"]
    colonnes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    lignes = [str(i+1) for i in range(8)]

    def __init__(self, formeWord):
        self.formeWord = formeWord
        self.forme = self.formes.index(formeWord)+1

    def joue_test(self, jeu):
        # verifie la possibilité de poser du Joueur sinon passera son tour
        # sera une méthode commune aux 2 types de joueurs
        if jeu.grille.teste_pose_possible(self.forme):
            return True

        print(f"Joueur {self.formeWord} ne peut jouer")
        return False


class JoueurHumain(Joueur):

    def __init__(self, formeWord):
        Joueur.__init__(self, formeWord)

    def entree_valide(self, forme):
        # renvoie une saisie autorisée de la case ex A4 ou de l'arret 00

        while True:
            if len(caseTableau) != 2 or (caseTableau != '00' and
                                         (caseTableau[0]not in self.colonnes or caseTableau[1] not in self.lignes)):
            # toujours sur la forme, préférez coller deux chaines
            # (le compilateur n'en crée qu'une) plutôt qu'un \
            caseTableau = input(f"Joueur {self.formeWord} quelle case "
                                f"(ex: A4 ? (00 pour arreter) ").upper()

                print("ce n'est pas une case valide")
                continue
            return caseTableau

    def joue(self):
        # renvoie  un booleen pion posé = True arretjeu = False
        #  verifie une saisie correcte et retourne les pions

        while True:  # saisie entree case JoueurHumain
            caseTableau = self.entree_valide(self.forme)

            # condition arret
            if caseTableau == '00':
                print("OK on arrete")
                return False

            ligne = self.lignes.index(caseTableau[1])
            colonne = self.colonnes.index(caseTableau[0])
            # verifie pose possible et retourne les pions
            if jeu.grille.pose(self.forme, ligne, colonne):
                return True

            print("rejouez case non autorisée pour vous")


class JoueurAI(Joueur):

    def __init__(self, formeWord):
        Joueur.__init__(self, formeWord)

    def joue(self):
        # meme nom mais comportement different : va analyser les priorités essentiellement

        return self.priorites()

    def priorites(self):
        # joue max points sauf si permet à autre acceder au coup suivant
        # sur un coin ou un coté
        # pire cas case adjacente d'un coin si retournable : methode à creer dans grille

        # coins prioritaires
        maxPions = 0
        for l, c in [(x, y) for x in (0, 7) for y in (0, 7)]:
            # verifie pose possible et retourne les pions
            pose, retourne = jeu.grille.pose_test(self.forme, l, c)
            if sum(retourne) > maxPions:
                maxPions = sum(retourne)
                lmax, cmax = l, c
        if maxPions > 0:
            print(
                f"\nAI {self.formeWord} joue en {self.colonnes[cmax]}{self.lignes[lmax]}  ")
            return jeu.grille.pose(self.forme, lmax, cmax)

        # maxpoints sauf cases à éviter
        maxPions = 0
        for l, c in [(x, y) for x in range(8) for y in range(8)]:
            if (l, c) in self.cases_a_eviter():
                continue
            # verifie pose possible et retourne les pions
            pose, retourne = jeu.grille.pose_test(self.forme, l, c)
            if sum(retourne) > maxPions:
                maxPions = sum(retourne)
                lmax, cmax = l, c
        if maxPions > 0:
            print(
                f"\nAI {self.formeWord} joue en {self.colonnes[cmax]}{self.lignes[lmax]} ")
            return jeu.grille.pose(self.forme, lmax, cmax)

        # au pire cases à eviter
        maxPions = 0
        for (l, c) in self.cases_a_eviter():

            # verifie pose possible et retourne les pions
            pose, retourne = jeu.grille.pose_test(self.forme, l, c)
            if sum(retourne) > maxPions:
                maxPions = sum(retourne)
                lmax, cmax = l, c
        if maxPions > 0:
            print(
                f"\nAI {self.formeWord} joue en {self.colonnes[cmax]}{self.lignes[lmax]} ")
            return jeu.grille.pose(self.forme, lmax, cmax)

    @staticmethod
    def cases_a_eviter():
        return list(set([(x, y) for x in (1, 6) for y in (0, 7)]
                        + [(x, y) for x in (0, 7) for y in (1, 6)]
                        + [(x, y) for x in (1, 6) for y in range(1, 7)]
                        + [(x, y) for x in range(1, 7) for y in (1, 6)]))


jeu = Jeu()
jeu.partie()
