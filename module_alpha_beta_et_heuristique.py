import numpy as np
profondeur_max=100

def heuristique(E,J):
    pass

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
        coups_possibles_J = coups_possibles(J.adv(), E)
        recompense=np.inf
        coup_a_retenir=None
        for piece,pos_finale in coups_possibles_J:
            h = heuristique(resultat_coup(E, piece, pos_finale), J)
            if h<recompense:
                recompense=h
                coup_a_retenir=piece,pos_finale
    enchainement,recompense_prochaine=minimax(E,J,profondeur_courante+1,profondeur_max)

    return [coup_a_retenir]+enchainement,recompense+recompense_prochaine

