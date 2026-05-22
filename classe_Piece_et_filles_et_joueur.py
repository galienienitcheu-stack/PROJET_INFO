## IMPORTATIONS                                                         ################################################
from abc import ABC, abstractmethod
import numpy as np
from chess import *


# dictionnaire de correspondance entre les lignes sur l'échiquier et les lignes dans le tableau numpy modélisant l'échiquier
dico={"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8}

#Classe Joueur                                                          ################################################
class Joueur(object):
    def __init__(self,couleur:str):
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

    def pieces_vivantes(self, E):
        L=[]
        pieces_Echiquier=[piece for sousliste in E for piece in sousliste]
        for piece in pieces_Echiquier:
            if piece.couleur==self.couleur:
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
    @abstractmethod
    def cases_accesibles(self, E):
        pass









# Classe Tour
class Tour(Piece):
    def __repr__(self):
        return "T"+self.couleur
    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                L.append((i+k,j))
                a=E[i + k][j]
            except IndexError:
                pass
            try:
                L.append((i,j+k))
                a=E[i][j + k]
            except IndexError:
                pass
        return L

#CLASSE CAVALIER                                                                    ####################################
class Cavalier(Piece):
    def __repr__(self):
        return "C"+self.couleur

    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i-2,j-1),(i-2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2),(i+2,j-1),(i+2,j+1)]
        for k,l in aux:
            try:
                if E[k][l]==None:
                    L.append((k,l))
            except IndexError:
                pass
        return L
#CLASSE FOU                                                                        #####################################
class Fou(Piece):
    def __repr__(self):
        return "F"+self.couleur
    def cases_accesibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                L.append((i+k,j+k))
            except IndexError:
                pass
            try:
                L.append((i-k,j+k))
            except IndexError:
                pass
        return L

#CLASSE DAME                                                                       #####################################
class Dame(Piece):
    def __repr__(self):
        return "D"+self.couleur

    def cases_accesibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                if E[i+k][j+k]==None:
                    L.append((i+k,j+k))
            except IndexError:
                pass
            try:
                if E[i-k][j+k]==None:
                    L.append((i-k,j+k))
            except IndexError:
                pass
            try:
                if E[i+k][j]==None:
                    L.append((i+k,j))
            except IndexError:
                pass
            try:
                if E[i][j+k]==None:
                    L.append((i,j+k))
            except IndexError:
                pass
        return L


#CLASSE ROI                                                                        #####################################
class Roi(Piece):
    def __repr__(self):
        return "R"+self.couleur

    def est_menacee(self,E):
        for i in range(8):
            for j in range(8):
                if not E[i][j].couleur==self.couleur:
                    if self.position(E) in E[i][j].cases_accessibles(E):
                        return True
        return False
    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i+1,j),(i-1,j),(i+1,j+1),(i,j+1),(i,j-1),(i-1,j-1),(i+1,j-1),(i-1,j+1)]
        for k,l in aux:
            try:
                if E[k][l]==None or E[k][l].couleur!=self.couleur:
                    self.position=k,l
                    if est_menacee(self,E)==False:
                        L.append((k,l))
                    self.position=ki,j
            except IndexError:
                pass
        return L




#CLASSE PION                                                                       #####################################
class Pion(Piece):
    def __repr__(self):
        return "P",self.couleur

    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        if self.couleur=='n':
            aux=[(i-1,j),(i-1,j-1),(i-1,j+1)]
            for k,l in aux:
                try:
                    if E[i-1][j]==None or E[i-1][j].couleur!=self.couleur:
                        L = [(i - 1, j)]
                except IndexError:
                    pass

            if self.position(E)[1]==self.position(E)[1]: ### A revoir, deplacement de deux cases si le pion est sur sa colonne initiale
                try:
                    if E[i-2][j]==None or E[i-2][j].couleur!=self.couleur:
                        L.append((i-2,j))
                except IndexError:
                    pass
        else:
            aux=[(i+1,j),(i+1,j-1),(i+1,j+1)]
            for k,l in aux:
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







