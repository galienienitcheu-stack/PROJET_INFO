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
        return None
    @abstractmethod
    def cases_accesibles(self, E):
        pass

class Tour(Piece):
    def __repr__(self):
        return "♖" if self.couleur=='b' else "♜"

    def cases_accesibles(self, E):
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

    def cases_accesibles(self, E):
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

    def cases_accesibles(self, E):
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

    def cases_accesibles(self, E):
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

    def est_menacee(self, E):
        i, j = self.position(E)
        for x in range(8):
            for y in range(8):
                piece = E[x][y]
                if piece and piece.couleur != self.couleur:
                    if (i, j) in piece.cases_accesibles(E):
                        return True
        return False

    def cases_accesibles(self, E):
        L = []
        i, j = self.position(E)
        moves = [(i + 1, j), (i - 1, j), (i + 1, j + 1), (i, j + 1),
                 (i, j - 1), (i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1)]
        for k, l in moves:
            if 0 <= k < 8 and 0 <= l < 8:
                if E[k][l] is None or E[k][l].couleur != self.couleur:
                    # Vérifie que le roi ne se met pas en échec
                    temp_board = [row[:] for row in E]  # Copie de l'échiquier
                    temp_board[k][l] = self
                    temp_board[i][j] = None
                    if not self.est_menacee(temp_board):
                        L.append((k, l))
        return L

class Pion(Piece):
    def __init__(self, couleur, colonne_depart=None):
        super().__init__(couleur)
        self.couleur = couleur
        self.colonne_depart = colonne_depart
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

        if self.couleur == 'b':  # Pions blancs (se déplacent vers le haut, indices décroissants)
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

def liste_pieces(couleur):
    c=couleur
    return [Tour(c),Cavalier(c),Fou(c),Dame(c),Roi(c),Fou(c),Cavalier(c),Tour(c)]

[T1n,C1n,F1n,Dn,Rn,F2n,C2n,T2n]=liste_pieces('n')
Pieces_noires=[T1n,C1n,F1n,Dn,Rn,F2n,C2n,T2n]
[T1b, C1b, F1b, Db, Rb, F2b, C2b, T2b]=liste_pieces('b')
Pieces_blanches=[T1b,C1b,F1b,Db,Rb,F2b,C2b,T2b]
[P1b,P2b,P3b,P4b,P5b,P6b,P7b,P8b]=[Pion('b',i) for i in range(8)]
Pions_blancs=[P1b,P2b,P3b,P4b,P5b,P6b,P7b,P8b]
[P1n,P2n,P3n,P4n,P5n,P6n,P7n,P8n]=[Pion('n',i) for i in range(8)]
Pions_noirs=[P1n,P2n,P3n,P4n,P5n,P6n,P7n,P8n]

positions_initiales = {
    T1n: (0, 0), C1n: (0, 1), F1n: (0, 2), Dn: (0, 3), Rn: (0, 4), F2n: (0, 5), C2n: (0, 6), T2n: (0, 7),
    P1n: (1, 0), P2n: (1, 1), P3n: (1, 2), P4n: (1, 3), P5n: (1, 4), P6n: (1, 5), P7n: (1, 6), P8n: (1, 7),
    P1b: (6, 0), P2b: (6, 1), P3b: (6, 2), P4b: (6, 3), P5b: (6, 4), P6b: (6, 5), P7b: (6, 6), P8b: (6, 7),
    T1b: (7, 0), C1b: (7, 1), F1b: (7, 2), Db: (7, 3), Rb: (7, 4), F2b: (7, 5), C2b: (7, 6), T2b: (7, 7)
}



#@static method c'est pour les méthodes indépendantes du self et de la classe
#map(fonction, iterable1, iterable2, ...): fonction intégrée qui permet d'appliquer une fonction à chaque élément d'un itérable (liste, tuple, chaîne de caractères, etc.) et de renvoyer un nouvel itérable (un objet map) contenant les résultats.
#__new__: constructeur et __init__: initialisateur







