from module_alpha_beta_et_heuristique import resultat_coup
from module_classes import *
import module_alpha_beta_et_heuristique

def echec(J,E):
    return Roi(J.couleur).est_menacee(E)




print("C'est parti pour une partie d'échec!!\n")
boucle=True
while boucle:
    try:
        c= input("Choisis ta couleur. 'n' pour noir et 'b' pour blanc:  ")
        if J not in ["n", "b"]:
            raise ValueError("Erreur")
    except ValueError:
        print("Saisir une entrée correcte")
        boucle = True
    else:
        boucle = False
J=Joueur(c)
ia=J.adv()


def jeu_echec(J,ia):
    E=Echiquier()
    print("C'est parti!")
    J,Jadv= J * (J == 'b') + ia * (J == 'n'), J * (J == 'n') + ia * (J == 'b')
    L_adv=Jadv.pieces_vivantes()
    L=J.pieces_vivantes()

    match_nul = False
    while not echec(J,E) and not match_nul:
        if J==ia:
            enchainement, recompense = minimax(E, J, 1, profondeur_max, heuristique)
            piece_jouee,sa_position_finale = enchainement[0]
            E = resultat_coup(piece_jouee,sa_position_finale)

        if recompense==-module_alpha_beta_et_heuristique.np.inf:
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














