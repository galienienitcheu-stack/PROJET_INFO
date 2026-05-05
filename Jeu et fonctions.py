from module_classes import *
from module_alphabeta_et_heristique import *

def echec(J,E):
    return Roi(J.couleur).est_menacee(E)





def jeu_echec(J,Jadv):
    E=Echiquier()
    print("C'est parti!")
    L_adv=Jadv.pieces_vivantes()
    L=J.pieces_vivantes()

    action = False
    while not echec(J,E):
        enchainement,recompense=minimax(E,J,1,profondeur_max,heuristique)
            coup_a_retenir=enchainement[0]
            E=coup_a_retenir
            print("Il y a pat, MATCH  NUL")
    if echec(J.adversaire(),E):
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














