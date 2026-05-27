## IMPORTATIONS                                                         ################################################
from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from chess import *
from Pièces import *
# --- VARIABLES GLOBALES POUR LES REGLES SPECIALES ---
dernier_coup = None       # ((i_depart, j_depart), (i_arrivee, j_arrivee), piece)



#Classe Joueur                                                          ################################################
class Joueur(object):
    def __init__(self, couleur: str) -> None:
        """
        Créé un joueur.

        Paramètres
        ----------
        couleur: str
            La couleur du joueur.
        """
        self.couleur=couleur

    def __repr__(self):
        return self.couleur

    def adv(self):
        if self.couleur=='n':
            return Joueur('b')
        return Joueur('n')

    def pieces_vivantes(self, E: list[list[Piece]]) -> list[Piece]:
        """

        :type E: object
        """
        L=[]
        sousliste: list[Piece]
        for piece in [piece for sousliste in E for piece in sousliste]:
            if piece!= None and piece.couleur==self.couleur:
                L.append(piece)
        return L



#CLASSE PIECE                                                           ################################################
class Piece(metaclass=ABCMeta):
    def __init__(self,couleur:str):
        """
        Créé une pièce.

        Paramètres
        ----------
        pos: tuple
            Les coordonnées auxquelles l'animal sera créé.

        capacité: int
            niveau de santé maximal de l'animal. Vaut 20 par défaut.
        """
        self.couleur=couleur
        self.a_bouge = False

    def position(self, E):
        """
        Renvoie la position d'une pièce sur un échiquier.

        Paramètres
        ----------
        pos: tuple
            Les coordonnées auxquelles l'animal sera créé.

        capacité: int
            niveau de santé maximal de l'animal. Vaut 20 par défaut.
        """
        for i in range(8):
            for j in range(8):
                if E[i][j]==self:
                    return i,j
        return None
        
    def notifier_deplacement(self):
    """Marque une pièce comme ayant déjà bougé (utile pour le roque)."""
        self.a_bouge = True
    
    def roi_en_echec(E, couleur):
        # trouve le roi
        for i in range(8):
            for j in range(8):
                p = E[i][j]
                if isinstance(p, Roi) and p.couleur == couleur:
                    roi = p
                    break
        rpos = roi.position(E)

    # regarde si une pièce adverse attaque le roi
        for i in range(8):
            for j in range(8):
                p = E[i][j]
                if p is not None and p.couleur != couleur:
                    if rpos in p.cases_accesibles(E):
                        return True
    return False


    def simuler_coup(E, i1, j1, i2, j2):
        # copie légère du plateau
        E2 = [ligne[:] for ligne in E]
        piece = E2[i1][j1]
        E2[i1][j1] = None
        E2[i2][j2] = piece
        return E2
    def filtrer_clouage(self, E, coups):
        i0, j0 = self.position(E)
        valides = []

        for i1, j1 in coups:
            if 0 <= i1 < 8 and 0 <= j1 < 8:
                E2 = simuler_coup(E, i0, j0, i1, j1)
            if not roi_en_echec(E2, self.couleur):
                valides.append((i1, j1))
        return valides
    
    @abstractmethod
    def cases_accessibles(self, E):
        pass






# Classe Tour
class Tour(Piece):
    def __repr__(self):
        return "♖" if self.couleur=='b' else "♜"
    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                if E[i+k][j]==None or E[i+k][j].couleur!=self.couleur:
                    L.append((i+k,j))
            except IndexError:
                pass
            try:
                if E[i][j+k]==None or E[i][j+k].couleur!=self.couleur:
                    L.append((i,j+k))
            except IndexError:
                pass
       return self.filtrer_clouage(E, L)

#CLASSE CAVALIER                                                                    ####################################
class Cavalier(Piece):
    def __repr__(self):
        return "♘" if self.couleur=='b' else "♞"


    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i-2,j-1),(i-2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2),(i+2,j-1),(i+2,j+1)]
        for k,l in aux:
            try:
                if E[k][l]==None or E[k][l].couleur!=self.couleur:
                    L.append((k,l))
            except IndexError:
                pass
        return self.filtrer_clouage(E, L)
#CLASSE FOU                                                                        #####################################
class Fou(Piece):
    def __repr__(self):
        return "♗" if self.couleur=='b' else "♝"
    def cases_accessibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                if E[i+k][j+k]==None or E[i+k][j+k].couleur!=self.couleur:
                    L.append((i+k,j+k))
            except IndexError:
                pass
            try:
                if E[i-k][j+k]==None or E[i-k][j+k].couleur!=self.couleur:
                    L.append((i-k,j+k))
            except IndexError:
                pass
        return self.filtrer_clouage(E, L)

#CLASSE DAME                                                                       #####################################
class Dame(Piece):
    def __repr__(self):
        return  "♕" if self.couleur=='b' else "♛"

    def cases_accessibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                if E[i+k][j+k]==None or E[i+k][j+k].couleur!=self.couleur:
                    L.append((i+k,j+k))
            except IndexError:
                pass
            try:
                if E[i-k][j+k]==None or E[i-k][j+k].couleur!=self.couleur:
                    L.append((i-k,j+k))
            except IndexError:
                pass
            try:
                if E[i+k][j]==None or E[i+k][j].couleur!=self.couleur:
                    L.append((i+k,j))
            except IndexError:
                pass
            try:
                if E[i][j+k]==None or E[i][j+k].couleur!=self.couleur:
                    L.append((i,j+k))
            except IndexError:
                pass
        return self.filtrer_clouage(E, L)


#CLASSE ROI                                                                        #####################################
class Roi(Piece):
    def __repr__(self):
        return "♔" if self.couleur=='b' else "♚"

    def est_menacee(self,E):
        k,l= self.position
        for i in range(8):
            for j in range(8):
                if not E[i][j].couleur==self.couleur:
                    if self.position(E) in E[i][j].cases_accessibles(E):
                        return True
        return False
    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i+1,j),(i-1,j),(i+1,j+1),(i,j+1),(i,j-1),(i-1,j-1),(i+1,j-1),(i-1,j+1)]
        for k,l in aux:
            try:
                if E[k][l] is None or E[k][l].couleur!=self.couleur : 
                        L.append((k,l))
            except IndexError:
                pass
        return self.filtrer_clouage(E, L)




#CLASSE PION                                                                       #####################################
class Pion(Piece):
    def __repr__(self):
        return "♙" if self.couleur=='b' else "♟"

    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        if self.couleur=='n':
            aux=[(i-1,j),(i-1,j-1),(i-1,j+1)]
            for k,l in aux:
                try:
                    if E[k][l]==None or E[k][l].couleur!=self.couleur:
                        L.append((k, l))
                except IndexError:
                    pass

            if self.position(E)[1]==positions_initiales[self][1]: ### A revoir, deplacement de deux cases si le pion est sur sa colonne initiale
                try:
                    if E[i-2][j]==None or E[i-2][j].couleur!=self.couleur:
                        L.append((i-2,j))
                except IndexError:
                    pass
        else:
            aux=[(i+1,j),(i+1,j-1),(i+1,j+1)]
            for i,j in aux:
                try:
                    if E[i+1][j]==None or E[i+1][j].couleur!=self.couleur:
                        L .append((i+1,j))
                except IndexError:
                    pass
            if self.position(E)[1]==self.position(E)[1]: ### A revoir, deplacement de deux cases si le pion est sur sa colonne initiale
                pass
        return L









#@static method c'est pour les méthodes indépendantes du self et de la classe
#map(fonction, iterable1, iterable2, ...): fonction intégrée qui permet d'appliquer une fonction à chaque élément d'un itérable (liste, tuple, chaîne de caractères, etc.) et de renvoyer un nouvel itérable (un objet map) contenant les résultats.
#__new__: constructeur et __init__: initialisateur







