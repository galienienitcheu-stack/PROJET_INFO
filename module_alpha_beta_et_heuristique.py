import numpy as np
profondeur_max=100

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
    # évaluation du matériel en centipion
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
    
    #Ajustements dynamiques



def coups_possibles(J,E):
    L=[]
    for piece in J.pieces_vivantes(E):
        for pos in piece.cases_accesibles(E):
            L.append((piece,pos))
    return L


def resultat_coup(E, piece, pos_finale):
    k, l = piece.position(E)
    i, j = pos_finale
    E[i][j] = piece
    E[k][l] = None
    return E

def minimax(E,J,profondeur_courante,profondeur_max,heuristique):
    if profondeur_courante%2==1:
        coups_possibles_J = coups_possibles(J, E)
        recompense=-np.inf
        coup_a_retenir=None
        for piece,pos_finale in coups_possibles_J:
            h=heuristique(resultat_coup(E,piece,pos_finale),J)
            if h>recompense:
                recompense=h
                coup_a_retenir=piece,pos_finale
    else:
        if profondeur_courante % 2 == 1:
            recompense_finale = -np.inf
            coup_a_retenir = None, None
            for piece, pos_finale in coups_possibles(J, E):
                enchainement_coups, recompense = minmax(resultat_coup(E, piece, pos_finale), J,
                                                         profondeur_courante + 1, profondeur_max)
                if recompense > recompense_finale:
                    recompense_finale = recompense
                    coup_a_retenir = piece, pos_finale
        else:
            recompense_finale = np.inf
            coup_a_retenir = None, None
            for piece, pos_finale in coups_possibles(J.adv(), E):
                enchainement_coups, recompense = minmax(resultat_coup(E, piece, pos_finale), J,
                                                         profondeur_courante + 1, profondeur_max)
                if recompense < recompense_finale:
                    recompense_finale = recompense
                    coup_a_retenir = piece, pos_finale
        return [coup_a_retenir] + enchainement_coups, recompense_finale

def alpha_beta(E,J,profondeur_courante,profondeur_max,heuristique,alpha=-np.inf,beta=np.inf,est_maximisant=True):
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
        return [],heuristique(E,J)
    else:
        if profondeur_courante % 2 == 1:
            alpha = -np.inf
            config_possibles=[]
            for piece, pos_finale in coups_possibles(J, E):
                config_possibles.append(resultat_coup(E, piece, pos_finale))
            premiere_config=config_possibles[0]
            mini=np.inf
            for piece, pos_finale in coups_possibles(J.adv(), premiere_config):
                configuration = resultat_coup(premiere_config, piece, pos_finale)
                recompense=alpha_beta(configuration,J,profondeur_courante+2,profondeur_max,heuristique)
                if recompense<mini:
                    mini=recompense
            alpha=mini
            for config in config_possibles[1:]:
                i=0
                mini=np.inf
                piece, pos_finale = coups_possibles(J.adv(), config)[i]
                configuration = resultat_coup(config, piece, pos_finale)
                recompense = alpha_beta(configuration, J, profondeur_courante + 2, profondeur_max, heuristique)
                while recompense<mini and recompense>alpha and i<len(coups_possibles(J.adv(), config)):
                    mini=recompense
                    i += 1
                    piece, pos_finale=coups_possibles(J.adv(), config)[i]
                    configuration=resultat_coup(config, piece, pos_finale)
                    recompense=alpha_beta(configuration,J,profondeur_courante+2,profondeur_max,heuristique)
                alpha=max(alpha,recompense)
        if profondeur_courante % 2 == 0:
            beta = np.inf
            config_possibles=[]
            for piece, pos_finale in coups_possibles(J.adv(), E):
                config_possibles.append(resultat_coup(E, piece, pos_finale))
            premiere_config=config_possibles[0]
            maxi=-np.inf
            for piece, pos_finale in coups_possibles(J, premiere_config):
                configuration = resultat_coup(premiere_config, piece, pos_finale)
                recompense=alpha_beta(configuration,J,profondeur_courante+2,profondeur_max,heuristique)
                if recompense>maxi:
                    maxi=recompense
            beta=maxi
            for config in config_possibles[1:]:
                i=0
                maxi=np.inf
                piece, pos_finale = coups_possibles(J, config)[i]
                configuration = resultat_coup(config, piece, pos_finale)
                recompense = alpha_beta(configuration, J, profondeur_courante + 2, profondeur_max, heuristique)
                while recompense>maxi and recompense<beta and i<len(coups_possibles(J.adv(), config)):
                    maxi=recompense
                    i += 1
                    piece, pos_finale=coups_possibles(J.adv(), config)[i]
                    configuration=resultat_coup(config, piece, pos_finale)
                    recompense=alpha_beta(configuration,J,profondeur_courante+2,profondeur_max,heuristique)
                beta=min(beta,recompense)





