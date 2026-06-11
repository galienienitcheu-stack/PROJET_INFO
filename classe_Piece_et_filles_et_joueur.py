from abc import ABC, abstractmethod, ABCMeta
from typing import Any

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

    def pieces_vivantes(self, E: list[list[Piece]]) -> list[Piece]:
        """

        :type E: object
        """
        L=[]

        return [piece for row in E for piece in row if piece and piece.couleur == self.couleur]

class Piece(metaclass=ABCMeta):
    def __init__(self, couleur: str) -> None:
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
        board : list
            L'échiquier (liste 2D 8x8) où chercher la pièce.

        Retourne
        -------
        tuple
            Un tuple (row, col) représentant la position de la pièce sur l'échiquier.
            Retourne None si la pièce n'est pas trouvée.
        """
        for i in range(8):
            for j in range(8):
                if E[i][j]==self:
                    return i,j
        return (0,0)
    def est_menacee(self, E):
        i, j = self.position(E)
        for x in range(8):
            for y in range(8):
                piece = E[x][y]
                if piece is not None and piece.couleur != self.couleur:
                    if (i, j) in piece.cases_accessibles(E):
                        return True
        return False
    @abstractmethod
    def cases_accessibles(self, E):
        pass

class Tour(Piece):
    def __repr__(self):
        return "♖" if self.couleur=='b' else "♜"

    def cases_accessibles(self, E):
        L = []
        i, j = self.position(E)

        # Droite (→)
        for k in range(1, 8):
            if j + k < 8:
                if E[i][j + k] is None:
                    L.append((i, j + k))
                else:
                    if E[i][j + k].couleur != self.couleur:
                        L.append((i, j + k))
                    break
            else:
                break

        # Gauche (←)
        for k in range(1, 8):
            if j - k >= 0:
                if E[i][j - k] is None:
                    L.append((i, j - k))
                else:
                    if E[i][j - k].couleur != self.couleur:
                        L.append((i, j - k))
                    break
            else:
                break

        # Bas (↓)
        for k in range(1, 8):
            if i + k < 8:
                if E[i + k][j] is None:
                    L.append((i + k, j))
                else:
                    if E[i + k][j].couleur != self.couleur:
                        L.append((i + k, j))
                    break
            else:
                break

        # Haut (↑)
        for k in range(1, 8):
            if i - k >= 0:
                if E[i - k][j] is None:
                    L.append((i - k, j))
                else:
                    if E[i - k][j].couleur != self.couleur:
                        L.append((i - k, j))
                    break
            else:
                break

        return L

class Cavalier(Piece):
    def __repr__(self):
        return "♘" if self.couleur=='b' else "♞"

    MOVES_CAVALIER = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2), (1, 2), (2, -1), (2, 1)]

    def cases_accessibles(self, E):
        L = []
        i, j = self.position(E)
        for di, dj in self.MOVES_CAVALIER:  # Utilise l'attribut de classe
            k, l = i + di, j + dj
            if 0 <= k < 8 and 0 <= l < 8:
                if E[k][l] is None or E[k][l].couleur != self.couleur:
                    L.append((k, l))
        return L

class Fou(Piece):
    def __repr__(self):
        return "♗" if self.couleur=='b' else "♝"

    MOVES_FOU = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def cases_accessibles(self, E):
        L = []
        i, j = self.position(E)
        for di, dj in self.MOVES_FOU:
            for k in range(1, 8):  # Parcourt chaque case de la diagonale
                ni, nj = i + di * k, j + dj * k
                if 0 <= ni < 8 and 0 <= nj < 8:
                    if E[ni][nj] is None:
                        L.append((ni, nj))
                    else:
                        if E[ni][nj].couleur != self.couleur:
                            L.append((ni, nj))
                        break  # Bloque après une pièce
                else:
                    break
        return L

class Dame(Piece):
    def __repr__(self):
        return  "♕" if self.couleur=='b' else "♛"

    def cases_accessibles(self, E):
        L = []
        i, j = self.position(E)
        # Directions de la Tour (horizontales/verticales)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for k in range(1, 8):
                ni, nj = i + di * k, j + dj * k
                if 0 <= ni < 8 and 0 <= nj < 8:
                    if E[ni][nj] is None:
                        L.append((ni, nj))
                    else:
                        if E[ni][nj].couleur != self.couleur:
                            L.append((ni, nj))
                        break
                else:
                    break
        # Directions du Fou (diagonales)
        for di, dj in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            for k in range(1, 8):
                ni, nj = i + di * k, j + dj * k
                if 0 <= ni < 8 and 0 <= nj < 8:
                    if E[ni][nj] is None:
                        L.append((ni, nj))
                    else:
                        if E[ni][nj].couleur != self.couleur:
                            L.append((ni, nj))
                        break
                else:
                    break
        return L

class Roi(Piece):
    def __repr__(self):
        return "♔" if self.couleur=='b' else "♚"

    def cases_accessibles(self, E):
        L = []
        i, j = self.position(E)
        moves = [(i + 1, j), (i - 1, j), (i + 1, j + 1), (i, j + 1),
                 (i, j - 1), (i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1)]
        for k, l in moves:
            if 0 <= k < 8 and 0 <= l < 8:
                if E[k][l] is None or E[k][l].couleur != self.couleur:
                        L.append((k, l))
        return L

class Pion(Piece):
    def __init__(self, couleur, colonne_depart=None,ligne_depart=None):
        super().__init__(couleur)
        self.couleur = couleur
        self.colonne_depart = colonne_depart
        self.ligne_depart = ligne_depart
    def __repr__(self):
        return "♙" if self.couleur=='b' else "♟"

    def cases_accessibles(self, E):
        """
        Renvoie la liste des cases accessibles pour un pion sur un échiquier donné.

        Paramètres
        ----------
        E : list
            L'échiquier (liste 2D 8x8) sur lequel vérifier les cases accessibles.

        Retourne
        -------
        list
            Une liste de tuples (row, col) représentant les positions accessibles pour le pion.
            Inclut les cases de capture, les déplacements vers l'avant, et les déplacements de 2 cases depuis la position initiale.
        """
        L = []
        i, j = self.position(E)

        if self.ligne_depart == 6:  # Pions bas (se déplacent vers le haut, indices décroissants)
            # Captures diagonales
            aux = [(i-1, j-1), (i-1, j+1)]
            for k, l in aux:
                try:
                    if E[k][l] is not None and E[k][l].couleur != self.couleur:
                        L.append((k, l))
                except IndexError:
                    pass

            # Déplacement vers l'avant d'une case
            if 0 <= i-1 < 8 and E[i-1][j] is None:
                L.append((i-1, j))

            # Déplacement de 2 cases depuis la position initiale (ligne 6 ET colonne de départ)
            if i == 6 and j == self.colonne_depart:  # ✅ Vérifie la colonne de départ
                if (0 <= i-2 < 8 and
                        E[i-1][j] is None and  # Case intermédiaire vide
                        E[i-2][j] is None):    # Case finale vide
                    L.append((i-2, j))

        else:  # Pions noirs (se déplacent vers le bas, indices croissants)
            # Captures diagonales
            aux = [(i+1, j-1), (i+1, j+1)]
            for k, l in aux:
                try:
                    if E[k][l] is not None and E[k][l].couleur != self.couleur:
                        L.append((k, l))
                except IndexError:
                    pass

            # Déplacement vers l'avant d'une case
            if 0 <= i+1 < 8 and E[i+1][j] is None:
                L.append((i+1, j))

            # Déplacement de 2 cases depuis la position initiale (ligne 1 ET colonne de départ)
            if i == 1 and j == self.colonne_depart:  # ✅ Vérifie la colonne de départ
                if (0 <= i+2 < 8 and
                        E[i+1][j] is None and  # Case intermédiaire vide
                        E[i+2][j] is None):    # Case finale vide
                    L.append((i+2, j))

        return L


#@static method c'est pour les méthodes indépendantes du self et de la classe
#map(fonction, iterable1, iterable2, ...): fonction intégrée qui permet d'appliquer une fonction à chaque élément d'un itérable (liste, tuple, chaîne de caractères, etc.) et de renvoyer un nouvel itérable (un objet map) contenant les résultats.
#__new__: constructeur et __init__: initialisateur







