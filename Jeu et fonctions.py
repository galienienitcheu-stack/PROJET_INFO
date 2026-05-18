from module_alpha_beta_et_heuristique import *
from module_classes import *
import numpy as np
import module_alpha_beta_et_heuristique

def echec(J,E):
    return Roi(J.couleur).est_menacee(E)


def notation(couleur, piece, case, nb_coups, capture=False, echec=False, mat=False,
             concurrents=None):
    """
    Permet d'archiver la partie en cours sous forme manuscrite

    Paramètres
    """

    # concurrents = liste des AUTRES pièces du même type pouvant aller à la destination
    concurrents = concurrents or []

    # Préfixe du coup (numéro uniquement pour les Blancs)
    coup = f"{nb_coups}." if couleur == "b" else ""

    symbole = str(piece)  # "" pour un pion

    # ----- Désambiguïsation -----
    ambig = ""

    if concurrents:
        # a) Différentes colonnes → désambiguïsation par colonne
        if any(p.colonne != piece.colonne for p in concurrents):
            ambig = piece.colonne

        # b) Même colonne mais lignes différentes → désambiguïsation par ligne
        elif any(p.ligne != piece.ligne for p in concurrents):
            ambig = piece.ligne

        # c) Cas extrême : même colonne et même ligne (promotions multiples)
        else:
            ambig = piece.position

    # ----- Capture -----
    cap = "x" if capture else ""

    # ----- Suffixes (+ / #) -----
    suffix = "#" if mat else "+" if echec else ""

    # ----- Construction finale -----
    coup += f"{symbole}{ambig}{cap}{case}{suffix}"

    return coup

print("C'est parti pour une partie d'échec!!\n")
boucle=True
while boucle:
    try:
        c= input("Choisis ta couleur. 'n' pour noir et 'b' pour blanc:  ")
        if c not in ["n", "b"]:
            raise ValueError("Erreur")
    except ValueError:
        print("Saisir une entrée correcte")
        boucle = True
    else:
        boucle = False
Joueur=Joueur(c)
ia=Joueur.adv()


def jeu_echec(J,ia):
    E=Echiquier()
    print("C'est parti!")
    J,Jadv= J * (J == 'b') + ia * (J == 'n'), J * (J == 'n') + ia * (J == 'b')
    L_adv=Jadv.pieces_vivantes()
    L=J.pieces_vivantes()

    match_nul = False
    nb_coups = 1
    while not echec(J,E) and not match_nul:

        if J==ia:
            enchainement, recompense = minmax(E, J, 1, profondeur_max, heuristique)
            piece_jouee,sa_position_finale = enchainement[0]
            E = resultat_coup(piece_jouee,sa_position_finale)

        if recompense==-np.inf:
            print("Il y a pat, MATCH  NUL")
        if echec(J.adv(),E):
            print("Echec et mat! Fin de la partie")















































    #     #sécuriser au max les pièces en commençant par le Roi
    #     for p in L:
    #         if est_menacee(p):
    #             if peut_se_defendre(p):
    #                 se_defendre(p)
    #                 action=True
    #             elif est_defendable(p): #renvoie la pièce qui peut le défendre
    #                  defend(p,est_defendable(p))
    #                  action = True
    #     #attaquer stratégiquement si toutes les pièces sont en sécurité
    #     if action==False:
    #         for p in L:
    #             if peut_prendre(p):
    #                 l=peut_prendre(p) # liste des pièces prenables
    #                 for pi in l:
    #                     if est_defendu(p, pi): #si p est défendue lorsqu'il veut prendre pi
    #                         prendre(p,pi)
    #
    #     #attaquer en risquant
    #     if action==False: #si tous les pièces sont
    #
    #     #Si pas de défense ni d'attaque particulière à effectuer
    #     #Occuper le centre
    #
    #     #Développer ses pièces
    #
    #
    #     #Mettre le roi en sécurité
    #
    #
    #     #Roque
    #
    #     #Promotion
    #     if
    #     #Prise en passant
    #
    #
    # #Détecter le pat














