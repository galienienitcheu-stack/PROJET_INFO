from classe_Piece_et_filles_et_joueur import *
from chess import *

profondeur_max=5

def heuristique(E,J):
    """
    Renvoie l'heuristique d'une configuration pour un joueur J

    Paramètres
    ----------
    E : Echiquier
        L'échiquier
    J: Joueur
        Un joueur.

    Renvoie
    -------
    h : int
        l'heuristique de la configuration E
        """
    h=0
    c=J.couleur
    nb_fou=0
    # déséquilibre du matériel en centipion
    for liste in E:
        for piece in liste:
            if piece!=None:
                if type(piece)==Pion:
                        if piece.couleur==c:
                            h+=100
                        else:
                            h-=100
                if type(piece)==Cavalier:
                    if piece.couleur==c:
                        h+=300
                    else:
                        h-=300
                if type(piece)==Fou:
                    if piece.couleur==c:
                        h+=300
                        nb_fou+=1
                    else:
                        h-=300
                if type(piece)==Tour:
                    if piece.couleur==c:
                        h+=500
                    else:
                        h-=500
                if type(piece)==Dame:
                    if piece.couleur==c:
                        h+=900
                    else:
                        h-=900
                if type(piece)==Roi:
                    h+=0



                if piece.couleur==c:
                    i,j=piece.position(E)
    #Bonus pour le nombre de coups légaux
                    h+=len(piece.cases_accessibles(E))
    # Contrôle du centre
                    if (i,j) in [(4, 3), (4, 4), (3, 3), (3, 4)]:
                        h += 100
    #Pions au bord pénalisés
                    if type(piece)==Pion:
                        if j in [0,8]:
                            h-=100
    #bonus pour les pions connectés ou qui se défendent
                        for k,l in [(i-1,j-1),(i+1,j+1),(i,j-1),(i,j+1),(i-1,j+1),(i+1,j-1)]:
                            try:
                                if type(E[k,l])==piece:
                                h+=100
                            except IndexError:
                                pass
    #malus pour les pions doublés
                        for k,l in [(i-1,j),(i+1,j)]:
                            try:
                                if type(E[k,l])==piece:
                                h-=100
                            except IndexError:
                                pass
    #Bonus pour les pions passés
                        if (c=='n' and i==7 and E[i+1,j]==None) or (c=='b' and i==1 and E[i-1,j]==None):
                            h+=100
    #Malus pour les fous bloqués par les pions de la même couleur
                    if type(piece)==Fou:
                        for k,l in [(i-1,j-1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]:
                            try:
                                if E[k,l].couleur==c:
                                h-=50
                            except IndexError:
                                pass
    #Bonus pour un roi roqué
                    if type(piece)==Roi:
                        if (c=='n' and (i,j) in [(0,6),(0,2)]) or (c=='b' and (i,j) in [(7,6),(7,2)]):
                            h+=100


    #Bonus pour les paires de fous
    if nb_fou==2:
        h+=50
    return h

def coups_possibles(J,E):
    L=[]
    for piece in J.pieces_vivantes(E):
        for pos in piece.cases_accesibles(E):
            L.append((piece,pos))
    return L


def resultat_coup(E, piece, pos_finale):
    k, l = piece.position(E)
    i, j = pos_finale
    E[i,j] = piece
    E[k,l] = None
    return E

def minmax(E,J,profondeur_courante,profondeur_max,heuristique):
    if profondeur_courante>=profondeur_max:
        return None,heuristique(E,J)
    else:
        if profondeur_courante % 2 == 1:
            recompense_finale = -np.inf
            coup_a_retenir = None
            for piece, pos_finale in coups_possibles(J, E):
                coup,recompense = minmax(resultat_coup(E, piece, pos_finale), J,
                                                         profondeur_courante + 1, profondeur_max)
                if recompense_finale < recompense:
                    recompense_finale = recompense
                    coup_a_retenir = piece, pos_finale
        else:
            recompense_finale = np.inf
            coup_a_retenir = None
            for piece, pos_finale in coups_possibles(J.adv(), E):
                recompense = minmax(resultat_coup(E, piece, pos_finale), J,
                                                         profondeur_courante + 1, profondeur_max)
                if recompense < recompense_finale:
                    recompense_finale = recompense
                    coup_a_retenir = piece, pos_finale
        return coup_a_retenir, recompense_finale


def alpha_beta(E,J,profondeur_courante,profondeur_max,heuristique,alpha=-np.inf,beta=np.inf):
    """
    Implémentation de l'algorithme Alpha-Bêta pour les échecs.

    Args:
        E: État du plateau (configuration actuelle).
        J: Joueur actuel (ou objet représentant le joueur).
        profondeur_courante: Profondeur actuelle dans l'arbre.
        profondeur_max: Profondeur maximale de recherche.
        heuristique: Fonction d'évaluation (ex: heuristique(E, J) -> float).
        alpha: Meilleure valeur déjà trouvée pour le joueur maximisant (IA).
        beta: Meilleure valeur déjà trouvée pour le joueur minimisant (adversaire).
        est_maximisant: True si c'est le tour de l'IA (maximiser), False sinon (minimiser).

    Returns:
        tuple: (meilleur_coup, score)
            - meilleur_coup: Tuple (piece, pos_finale) ou None si profondeur_max atteinte.
            - score: Score heuristique associé.
    """
    if profondeur_courante>=profondeur_max:
        return None,heuristique(E,J)
    else:
        if profondeur_courante % 2 == 1:
            recompense_retenue,coup_retenu=-np.inf,None
            for piece, pos_finale in coups_possibles(J, E):
                nouvelle_config=resultat_coup(E, piece, pos_finale)
                coup,recompense=alpha_beta(nouvelle_config,J,profondeur_courante+1,profondeur_max,heuristique,alpha,beta)
                if recompense_retenue<recompense:
                    recompense_retenue=recompense
                    coup_retenu=coup
                    if recompense_retenue>=beta:
                        break
                if recompense>alpha:
                    alpha=recompense
        if profondeur_courante % 2 == 0:
            recompense_retenue,coup_retenu=np.inf,None
            for piece, pos_finale in coups_possibles(J, E):
                nouvelle_config=resultat_coup(E, piece, pos_finale)
                coup,recompense=alpha_beta(nouvelle_config,J,profondeur_courante+1,profondeur_max,heuristique,alpha,beta)
                if recompense_retenue>recompense:
                    recompense_retenue=recompense
                    coup_retenu=coup
                    if recompense_retenue<=alpha:
                        break
                if recompense<beta:
                    beta=recompense
        return coup_retenu,recompense_retenue





