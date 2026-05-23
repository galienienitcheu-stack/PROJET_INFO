from classe_Piece_et_filles_et_joueur import *
def liste_pieces(couleur):
    c=couleur
    return [Tour(c),Cavalier(c),Fou(c),Dame(c),Roi(c),Fou(c),Cavalier(c),Tour(c)]

[T1n,C1n,F1n,Dn,Rn,F2n,C2n,T2n]=liste_pieces('n')
Pieces_noires=[T1n,C1n,F1n,Dn,Rn,F2n,C2n,T2n]
[T1b, C1b, F1b, Db, Rb, F2b, C2b, T2b]=liste_pieces('b')
Pieces_blanches=[T1b,C1b,F1b,Db,Rb,F2b,C2b,T2b]
[P1b,P2b,P3b,P4b,P5b,P6b,P7b,P8b]=[Pion('b') for _ in range(8)]
Pions_blancs=[P1b,P2b,P3b,P4b,P5b,P6b,P7b,P8b]
[P1n,P2n,P3n,P4n,P5n,P6n,P7n,P8n]=[Pion('n') for _ in range(8)]
Pions_noirs=[P1n,P2n,P3n,P4n,P5n,P6n,P7n,P8n]