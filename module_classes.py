## IMPORTATIONS                                                         ################################################
import numpy as np


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

    def symb(self):
        return self.couleur

    def adversaire(self):
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
class Piece(object):
    def __init__(self,couleur:str,num:int):
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
        self.num=num

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

    def est_menacee(self, E):
        """
        Permet de déterminer si la pièce est menacée ou pas

        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        False: bool
            Si la pièce n'est pas menacée
        L: list
            La liste des pièces menaçantes dans le cas contraire
        """
        posi=self.position(E)
        L=[]
        Jadv=Joueur(self.couleur).adversaire()
        for p in Jadv.pieces_vivantes(E):
            if posi in p.cases_accesibles(E):
                L.append(p)
        return L.vide()


    def prendre(self,p,E):
        Jadv=Joueur(self.couleur).adversaire()
        Jadv.pieces_vivantes(E).remove(p)
        E.coup(self,p.position(E))



    def vivante(self, E):
        """
        Permet de déterminer si la pièce est sur l'échiquier ou pas

        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        True, False: bool
            Si la pièce est sur l'échiquier ou pas
        """
        return self in Joueur(self.couleur).pieces_vivantes(E)





# Classe Tour
class Tour(Piece):
    def symb(self):
        return "T"+self.couleur
    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                L.append([i+k,j])
                a=E[i + k][j]
            except IndexError:
                pass
            try:
                L.append([i,j+k])
                a=E[i][j + k]
            except IndexError:
                pass
        return L

#CLASSE CAVALIER                                                                    ####################################
class Cavalier(Piece):
    def symb(self):
        return "C"+self.couleur

    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i-2,j-1),(i-2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2),(i+2,j-1),(i+2,j+1)]
        for k,l in aux:
            try:
                if E[k][l]==None:
                    L.append([k,l])
            except IndexError:
                pass
        return L
#CLASSE FOU                                                                        #####################################
class Fou(Piece):
    def symb(self):
        return "F"+self.couleur
    def cases_accesibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                L.append([i+k,j+k])
            except IndexError:
                pass
            try:
                L.append([i-k,j+k])
            except IndexError:
                pass
        return L

#CLASSE DAME                                                                       #####################################
class Dame(Piece):
    def __init__(self,couleur):
        super().__init__(couleur,num=1)

    def symb(self):
        return "D"+self.couleur

    def cases_accesibles(self,E):
        L=[]
        i,j=self.position(E)
        for k in range(-7,8):
            try:
                if E[i+k][j+k]==None:
                    L.append([i+k,j+k])
            except IndexError:
                pass
            try:
                if E[i-k][j+k]==None:
                    L.append([i-k,j+k])
            except IndexError:
                pass
            try:
                if E[i+k][j]==None:
                    L.append([i+k,j])
            except IndexError:
                pass
            try:
                if E[i][j+k]==None:
                    L.append([i,j+k])
            except IndexError:
                pass
        return L


#CLASSE ROI                                                                        #####################################
class Roi(Piece):
    def __init__(self,couleur):
        super().__init__(couleur, num=1)
    def symb(self):
        return "R"+self.couleur
    def cases_accesibles(self, E):
        L=[]
        i,j=self.position(E)
        aux=[(i+1,j),(i-1,j),(i+1,j+1),(i,j+1),(i,j-1),(i-1,j-1),(i+1,j-1),(i-1,j+1)]
        for k,l in aux:
            try:
                if E[k][l]==None:
                    L.append([k,l])
            except IndexError:
                pass
        return L


#CLASSE PION                                                                       #####################################
class Pion(Piece):
    def symb(self):
        return "P",self.num,self.couleur

    def cases_accessibles(self, E):
        L=[]
        i,j=self.position(E)
        if self.couleur=='n':
            try:
                if E[i-1][j]==None:
                    L = [(i - 1, j)]
            except IndexError:
                pass
            if self.position(E)[1]==self.position(E())[1]:
                try:
                    if E[i-2][j]==None:
                        L.append((i-2,j))
                except IndexError:
                    pass
            try:
                if E[i - 1][j - 1]!=None:
                    L.append((i-1,j-1))
            except IndexError:
                pass
            try:
                if E[i - 1][j + 1]!=None:
                    L.append((i-1,j+1))
            except IndexError:
                pass
        else:
            try:
                if E[i+1][j]==None:
                    L = [(i+1,j)]
            except IndexError:
                pass
            if self.position(E)[1]==self.position(E())[1]:
                try:
                    if E[i+2][j]==None:
                        L.append((i+2,j))
                except IndexError:
                    pass
            try:
                if E[i + 1][j - 1]!=None:
                   L.append((i+1,j-1))
            except IndexError:
                pass
            try:
                if E[i + 1][j + 1]!=None:
                    L.append((i+11,j+1))
            except IndexError:
                pass
        return L



def liste_pieces(couleur):
    c=couleur
    return [Tour(c),Cavalier(c),Fou(c),Dame(c),Roi(c),Fou(c),Cavalier(c),Tour(c)]


#CLASSE ECHIQUIER                                                                        #####################################
class Echiquier(list):
    def __init__(self):
        super().__init__()
        for k in range(8):
            self.append([])
        Ln=liste_pieces('n')
        Lb=liste_pieces('b')
        for piece in Ln:
            self[0].append(piece)
        for piece in Lb:
            self[7].append(piece)
        for k in range(1,9):
            self[1].append(Pion('n'))
            self[6].append(Pion('b'))
            self[2].append(None)
            self[3].append(None)
            self[4].append(None)
            self[5].append(None)







    # def contenu(self):
    #     return np.array([[["b", "Tn"], ["n", "Cn"], ["b", "Fn"], ["n", "Dn"], ["b", "Rn"], ["n", "Fn"], ["b", "Cn"], ["n", "Tn"]],
    #                            [["n","P1n"],["b","P2n"],["n","P3n"],["b","P4n"],["n","P5n"],["b","P6n"],["n","P7n"],["b","P8n"],
    #                             [["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""]],
    #                             [["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""]],
    #                             [["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""]],
    #                             [["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""], ["n",""], ["b",""]],
    #                             [["b", "P1b"], ["n", "P2b"], ["b", "P3b"], ["n", "P4b"], ["b", "P5b"], ["n", "P6b"], ["b", "P7b"], ["n", "P8b"]],
    #                             [["n", "Tb"], ["b", "Cb"], ["n", "Fb"], ["b", "Db"], ["n", "Rb"], ["b", "Fb"], ["n", "Cb"], ["b", "Tb"]]
    #                             ])
        # A VOIR SI LA MENTION DES COULEURS DES CASES SERT A QUELQUE CHOSE




#@static method c'est pour les méthodes indépendantes du self et de la classe
#map(fonction, iterable1, iterable2, ...): fonction intégrée qui permet d'appliquer une fonction à chaque élément d'un itérable (liste, tuple, chaîne de caractères, etc.) et de renvoyer un nouvel itérable (un objet map) contenant les résultats.








