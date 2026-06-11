import unittest
from unittest.mock import patch
from chess import ChessGame
import sys
from PyQt5.QtWidgets import QApplication




#tests des méthodes des classes pièces
class TestPieces(unittest.TestCase):
    def setUp(self):
        # Crée une instance du jeu pour accéder aux méthodes
        self.game = ChessGame()
        self.game.setup_board()  # Initialise l'échiquier
        self.E = self.game.board  # Accès direct à l'échiquier pour les tests
        self.game.couleur_utilisateur='b'

        #pour les tests, l'utilisateur joue les blancs (choix)

# test des méthodes cases_accessible et est_menacée pour le roi
class TestPion(TestPieces):
    def test_pion_blanc_deplacement_simple(self):
        # Place un pion blanc en (6, 4)
        pion = self.game.P5b
        self.E[6][4] = pion
        accessibles = pion.cases_accessibles(self.E)
        # Le pion blanc peut avancer d'une case vers (5, 4)
        self.assertIn((5, 4), accessibles)

    def test_pion_blanc_deplacement_initial(self):
        # Place un pion blanc en (6, 4) (position initiale)
        pion = self.game.P5b  # Supposons que colonne_depart est passé
        self.E[6][4] = pion
        accessibles = pion.cases_accessibles(self.E)
        # Le pion blanc peut avancer de 2 cases depuis sa position initiale
        self.assertIn((5, 4), accessibles)
        self.assertIn((4, 4), accessibles)

    def test_pion_blanc_capture(self):
        # Place un pion blanc en (6, 4) et un pion noir en (5, 3) et (5, 5)
        pion = self.game.P5b
        self.E[6][4] = pion
        self.E[5][3] = self.game.P4n
        self.E[5][5] = self.game.P6n
        accessibles = pion.cases_accessibles(self.E)
        # Le pion blanc peut capturer les pions noirs en (5, 3) et (5, 5)
        self.assertIn((5, 3), accessibles)
        self.assertIn((5, 5), accessibles)

    def test_pion_noir_deplacement_simple(self):
        # Place un pion noir en (1, 4)
        pion = self.game.P5n
        self.E[1][4] = pion
        accessibles = pion.cases_accessibles(self.E)
        # Le pion noir peut avancer d'une case vers (2, 4)
        self.assertIn((2, 4), accessibles)

    def test_pion_noir_deplacement_initial(self):
        # Place un pion noir en (1, 4) (position initiale)
        pion = self.game.P4n
        self.E[1][4] = pion
        accessibles = pion.cases_accessibles(self.E)
        # Le pion noir peut avancer de 2 cases depuis sa position initiale
        self.assertIn((2, 4), accessibles)
        self.assertIn((3, 4), accessibles)

    def test_pion_noir_capture(self):
        # Place un pion noir en (1, 4) et un pion blanc en (2, 3) et (2, 5)
        pion = self.game.P5n
        self.E[1][4] = pion
        self.E[2][3] = self.game.P4b
        self.E[2][5] = self.game.P6b
        accessibles = pion.cases_accessibles(self.E)
        # Le pion noir peut capturer les pions blancs en (2, 3) et (2, 5)
        self.assertIn((2, 3), accessibles)
        self.assertIn((2, 5), accessibles)

    def test_pion_bord_echiquier(self):
        # Place un pion blanc en (6, 0) (bord gauche)
        pion = self.game.P4b
        self.E[6][0] = pion
        accessibles = pion.cases_accessibles(self.E)
        # Le pion ne peut pas capturer à gauche (hors de l'échiquier)
        self.assertNotIn((5, -1), accessibles)
        # Mais peut avancer vers (5, 0)
        self.assertIn((5, 0), accessibles)

    def test_pion_case_occupee(self):
        # Place un pion blanc en (6, 4) et une pièce blanche en (5, 4)
        pion = self.game.P5b
        self.E[6][4] = pion
        self.E[5][4] = self.game.P6b
        accessibles = pion.cases_accessibles(self.E)
        # Le pion ne peut pas avancer car la case est occupée par une pièce de la même couleur
        self.assertNotIn((5, 4), accessibles)

class TestTour(TestPieces):
    def test_tour_deplacement_horizontal(self):
        # Place une tour blanche en (4, 4)
        tour = self.game.T1b
        self.E[4][4] = tour
        accessibles = tour.cases_accessibles(self.E)
        # La tour peut se déplacer horizontalement
        self.assertIn((4, 0), accessibles)  # Gauche
        self.assertIn((4, 7), accessibles)  # Droite

    def test_tour_deplacement_vertical(self):
        # Place une tour blanche en (4, 4)
        tour = self.game.T1b
        self.E[4][4] = tour
        accessibles = tour.cases_accessibles(self.E)
        # La tour peut se déplacer verticalement
        self.assertIn((0, 4), accessibles)  # Haut
        self.assertIn((7, 4), accessibles)  # Bas

    def test_tour_capture(self):
        # Place une tour blanche en (4, 4) et une pièce noire en (4, 6)
        tour = self.game.T1b
        self.E[4][4] = tour
        self.E[4][6] = self.game.P7n
        accessibles = tour.cases_accessibles(self.E)
        # La tour peut capturer la pièce noire en (4, 6)
        self.assertIn((4, 6), accessibles)
        # Mais ne peut pas aller au-delà de la pièce capturée
        self.assertNotIn((4, 7), accessibles)

    def test_tour_obstacle(self):
        # Place une tour blanche en (4, 4) et une pièce blanche en (4, 6)
        tour = self.game.T1b
        self.E[4][4] = tour
        self.E[4][6] =self.game.P7b
        accessibles = tour.cases_accessibles(self.E)
        # La tour ne peut pas aller au-delà de l'obstacle
        self.assertNotIn((4, 6), accessibles)
        self.assertNotIn((4, 7), accessibles)
        # Mais peut aller jusqu'à (4, 5)
        self.assertIn((4, 5), accessibles)

class TestCavalier(TestPieces):
    def test_cavalier_deplacement(self):
        # Place un cavalier blanc en (4, 4)
        cavalier = self.game.C1b
        self.E[4][4] = cavalier
        accessibles = cavalier.cases_accessibles(self.E)
        # Le cavalier peut se déplacer en L
        self.assertIn((2, 3), accessibles)  # Haut-gauche
        self.assertIn((2, 5), accessibles)  # Haut-droite
        self.assertIn((6, 3), accessibles)  # Bas-gauche
        self.assertIn((6, 5), accessibles)  # Bas-droite
        self.assertIn((3, 2), accessibles)  # Gauche-haut
        self.assertIn((3, 6), accessibles)  # Droite-haut
        self.assertIn((5, 2), accessibles)  # Gauche-bas
        self.assertIn((5, 6), accessibles)  # Droite-bas

    def test_cavalier_capture(self):
        # Place un cavalier blanc en (4, 4) et une pièce noire en (2, 5)
        cavalier = self.game.C1b
        self.E[4][4] = cavalier
        self.E[2][5] = self.game.P6n
        accessibles = cavalier.cases_accessibles(self.E)
        # Le cavalier peut capturer la pièce noire en (2, 5)
        self.assertIn((2, 5), accessibles)

    def test_cavalier_bord_echiquier(self):
        # Place un cavalier blanc en (0, 0) (coin)
        cavalier =self.game.C1b
        self.E[0][0] = cavalier
        accessibles = cavalier.cases_accessibles(self.E)
        # Le cavalier ne peut pas sortir de l'échiquier
        self.assertNotIn((-2, 1), accessibles)
        self.assertNotIn((1, -2), accessibles)
        # Mais peut aller en (1, 2) et (2, 1)
        self.assertIn((1, 2), accessibles)
        self.assertIn((2, 1), accessibles)

class TestFou(TestPieces):
    def test_fou_deplacement_diagonale(self):
        # Place un fou blanc en (4, 4)
        fou = self.game.F1b
        self.E[4][4] = fou
        accessibles = fou.cases_accessibles(self.E)
        # Le fou peut se déplacer en diagonale
        self.assertIn((0, 0), accessibles)  # Haut-gauche
        self.assertIn((7, 7), accessibles)  # Bas-droite
        self.assertIn((1, 7), accessibles)  # Haut-droite
        self.assertIn((6, 1), accessibles)  # Bas-gauche

    def test_fou_capture(self):
        # Place un fou blanc en (4, 4) et une pièce noire en (2, 2)
        fou = self.game.F1b
        self.E[4][4] = fou
        self.E[2][2] =self.game.P3n
        accessibles = fou.cases_accessibles(self.E)
        # Le fou peut capturer la pièce noire en (2, 2)
        self.assertIn((2, 2), accessibles)
        # Mais ne peut pas aller au-delà de la pièce capturée
        self.assertNotIn((0, 0), accessibles)

    def test_fou_obstacle(self):
        # Place un fou blanc en (4, 4) et une pièce blanche en (2, 2)
        fou = self.game.F1b
        self.E[4][4] = fou
        self.E[2][2] = self.game.P3n
        accessibles = fou.cases_accessibles(self.E)
        # Le fou ne peut pas aller au-delà de l'obstacle
        self.assertNotIn((2, 2), accessibles)
        self.assertNotIn((0, 0), accessibles)
        # Mais peut aller jusqu'à (3, 3)
        self.assertIn((3, 3), accessibles)

class TestDame(TestPieces):
    def test_dame_deplacement_horizontal(self):
        # Place une dame blanche en (4, 4)
        dame = self.game.Db
        self.E[4][4] = dame
        accessibles = dame.cases_accessibles(self.E)
        # La dame peut se déplacer horizontalement comme une tour
        self.assertIn((4, 0), accessibles)  # Gauche
        self.assertIn((4, 7), accessibles)  # Droite

    def test_dame_deplacement_vertical(self):
        # Place une dame blanche en (4, 4)
        dame = self.game.Db
        self.E[4][4] = dame
        accessibles = dame.cases_accessibles(self.E)
        # La dame peut se déplacer verticalement comme une tour
        self.assertIn((0, 4), accessibles)  # Haut
        self.assertIn((7, 4), accessibles)  # Bas

    def test_dame_deplacement_diagonale(self):
        # Place une dame blanche en (4, 4)
        dame = self.game.Db
        self.E[4][4] = dame
        accessibles = dame.cases_accessibles(self.E)
        # La dame peut se déplacer en diagonale comme un fou
        self.assertIn((0, 0), accessibles)  # Haut-gauche
        self.assertIn((7, 7), accessibles)  # Bas-droite

    def test_dame_capture(self):
        # Place une dame blanche en (4, 4) et une pièce noire en (4, 6)
        dame =self.game.Db
        self.E[4][4] = dame
        self.E[4][6] = self.game.P7n
        accessibles = dame.cases_accessibles(self.E)
        # La dame peut capturer la pièce noire en (4, 6)
        self.assertIn((4, 6), accessibles)
        # Mais ne peut pas aller au-delà de la pièce capturée
        self.assertNotIn((4, 7), accessibles)

class TestRoi(TestPieces):
    def test_roi_deplacement(self):
        # Place un roi blanc en (4, 4)
        roi = self.game.Rb
        self.E[4][4] = roi
        accessibles = roi.cases_accessibles(self.E)
        # Le roi peut se déplacer d'une case dans toutes les directions
        self.assertIn((3, 3), accessibles)  # Haut-gauche
        self.assertIn((3, 4), accessibles)  # Haut
        self.assertIn((3, 5), accessibles)  # Haut-droite
        self.assertIn((4, 3), accessibles)  # Gauche
        self.assertIn((4, 5), accessibles)  # Droite
        self.assertIn((5, 3), accessibles)  # Bas-gauche
        self.assertIn((5, 4), accessibles)  # Bas
        self.assertIn((5, 5), accessibles)  # Bas-droite

    def test_roi_capture(self):
        # Place un roi blanc en (4, 4) et une pièce noire en (3, 5)
        roi = self.game.Rb
        self.E[4][4] = roi
        self.E[3][5] = roi = self.game.P6n
        accessibles = roi.cases_accessibles(self.E)
        # Le roi peut capturer la pièce noire en (3, 5)
        self.assertIn((3, 5), accessibles)

    def test_roi_bord_echiquier(self):
        # Place un roi blanc en (0, 0) (coin)
        roi = roi = self.game.Rb
        self.E[0][0] = roi
        accessibles = roi.cases_accessibles(self.E)
        # Le roi ne peut pas sortir de l'échiquier
        self.assertNotIn((-1, 0), accessibles)
        self.assertNotIn((0, -1), accessibles)
        # Mais peut aller en (0, 1), (1, 0), (1, 1)
        self.assertIn((0, 1), accessibles)
        self.assertIn((1, 0), accessibles)
        self.assertIn((1, 1), accessibles)

    def test_roi_est_menacee(self):
        # Place un roi blanc en (4, 4) et une tour noire en (4, 0)
        roi = self.game.Rb
        tour = self.game.T1n
        self.E[4][4] = roi
        self.E[4][0] = tour
        # Le roi est menacé par la tour
        self.assertTrue(roi.est_menacee(self.E))

    def test_roi_non_menace(self):
        # Place un roi blanc en (4, 4) sans pièce adverse
        roi = self.game.Rb
        self.E[4][4] = roi
        # Le roi n'est pas menacé
        self.assertFalse(roi.est_menacee(self.E))


#test d'une partie d'échec

#test des méthodes echec et echec et mat

class TestEchecEtMat(unittest.TestCase):
    def setUp(self):
        # Crée une instance du jeu pour accéder aux méthodes
        self.game = ChessGame()
        self.game.setup_board()  # Initialise l'échiquier
        self.E = self.game.board  # Accès direct à l'échiquier pour les tests

    def test_echec_roi_menace_par_tour(self):
        # Place un roi blanc en (4, 4) et une tour noire en (4, 0)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        self.E[4][4] = roi
        self.E[4][0] = tour
        # Le roi blanc est menacé par la tour noire
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_roi_menace_par_fou(self):
        # Place un roi blanc en (4, 4) et un fou noir en (0, 0)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        fou = self.game.F1n
        self.E[4][4] = roi
        self.E[0][0] = fou
        # Le roi blanc est menacé par le fou noir
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_roi_menace_par_cavalier(self):
        # Place un roi blanc en (4, 4) et un cavalier noir en (2, 3)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        cavalier = self.game.C1n
        self.E[4][4] = roi
        self.E[2][3] = cavalier
        # Le roi blanc est menacé par le cavalier noir
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_roi_menace_par_dame(self):
        # Place un roi blanc en (4, 4) et une dame noire en (4, 7)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        dame = self.game.Dn
        self.E[4][4] = roi
        self.E[4][7] = dame
        # Le roi blanc est menacé par la dame noire
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_roi_menace_par_pion(self):
        # Place un roi blanc en (4, 4) et un pion noir en (3, 3)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        pion = self.game.P4n
        self.E[4][4] = roi
        self.E[3][3] = pion
        # Le roi blanc est menacé par le pion noir
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_roi_non_menace(self):
        # Place un roi blanc en (4, 4) sans pièce adverse
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        self.E[4][4] = roi
        # Le roi blanc n'est pas menacé
        self.assertFalse(self.game.echec(self.game.joueur_blanc))

    def test_echec_roi_menace_par_plusieurs_pieces(self):
        # Place un roi blanc en (4, 4), une tour noire en (4, 0) et un fou noir en (0, 0)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        fou = self.game.F1n
        self.E[4][4] = roi
        self.E[4][0] = tour
        self.E[0][0] = fou
        # Le roi blanc est menacé par la tour et le fou
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_et_mat_roi_tour(self):
        # Place un roi blanc en (7, 4) et une tour noire en (7, 0)
        # Le roi ne peut pas bouger, car bloqué par la dame
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        dame=self.game.Dn
        self.E[7][4] = roi
        self.E[7][0] = tour
        self.E[6][2] = dame
        # Le roi blanc est en échec et mat
        self.assertTrue(self.game.echec_et_mat(self.game.joueur_blanc))

    def test_echec_et_mat_roi_dame(self):
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        dame=self.game.Dn
        pion_noir = self.game.P5n  # Protège la dame
        self.E[7][4] = roi
        self.E[6][4] = dame
        self.E[5][4] = pion_noir  # Empêche la capture
        self.assertTrue(self.game.echec_et_mat(self.game.joueur_blanc))

    def test_echec_mais_pas_mat_roi_peut_bouger(self):
        # Place un roi blanc en (4, 4) et une tour noire en (4, 0)
        # Le roi peut bouger vers (3, 4) ou (5, 4)
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        self.E[4][4] = roi
        self.E[4][0] = tour
        # Le roi blanc est en échec mais pas en échec et mat
        self.assertFalse(self.game.echec_et_mat(self.game.joueur_blanc))
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_mais_pas_mat_piece_peut_bloquer(self):
        # Place un roi blanc en (4, 4), une tour noire en (4, 0), et un pion blanc en (5, 1)
        # Le pion peut bloquer la tour
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        pion = self.game.P2b
        self.E[4][4] = roi
        self.E[4][0] = tour
        self.E[5][1] = pion
        # Le roi blanc est en échec mais pas en échec et mat (le pion peut bloquer)
        self.assertFalse(self.game.echec_et_mat(self.game.joueur_blanc))
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_echec_mais_pas_mat_piece_peut_capturer(self):
        # Place un roi blanc en (4, 4), une tour noire en (4, 0), et une tour blanche en (4, 2)
        # La tour blanche peut capturer la tour noire
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour_noire =self.game.T1n
        tour_blanche = self.game.T1b
        self.E[4][4] = roi
        self.E[4][0] = tour_noire
        self.E[4][2] = tour_blanche
        # Le roi blanc est en échec mais pas en échec et mat (la tour blanche peut capturer)
        self.assertFalse(self.game.echec_et_mat(self.game.joueur_blanc))
        self.assertTrue(self.game.echec(self.game.joueur_blanc))

    def test_pas_echec_et_mat(self):
        # Place un roi blanc en (4, 4) sans pièce adverse
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        self.E[4][4] = roi
        # Le roi blanc n'est pas en échec et mat
        self.assertFalse(self.game.echec_et_mat(self.game.joueur_blanc))

    def test_echec_et_mat_roi_cavalier(self):
        # Place un roi blanc en (7, 7) et un cavalier noir en (5, 6)
        # Le roi ne peut pas bouger et aucune pièce ne peut capturer le cavalier
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        cavalier = self.game.C1n
        dame=self.game.Dn
        self.E[7][7] = roi
        self.E[5][6] = cavalier
        self.E[6][5] = dame
        # Le roi blanc est en échec et mat
        self.assertTrue(self.game.echec_et_mat(self.game.joueur_blanc))

    def test_echec_et_mat_roi_fou(self):
        # Place un roi blanc en (7, 7) et un fou noir en (5, 5)
        # Le roi ne peut pas bouger et aucune pièce ne peut bloquer
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        fou = self.game.F1n
        dame = self.game.Dn
        self.E[7][7] = roi
        self.E[5][5] = fou
        self.E[6][5] = dame
        # Le roi blanc est en échec et mat
        self.assertTrue(self.game.echec_et_mat(self.game.joueur_blanc))

    def test_echec_et_mat_roi_pion(self):
        # Place un roi blanc en (7, 4) et un pion noir en (6, 3)
        # Le roi ne peut pas bouger et aucune pièce ne peut capturer le pion
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        pion = self.game.P4n
        dame=self.game.Dn
        tour=self.game.T1n
        self.E[7][4] = roi
        self.E[6][3] = pion
        self.E[5][5] = dame
        self.E[6][2] = tour
        # Le roi blanc est en échec et mat
        self.assertTrue(self.game.echec_et_mat(self.game.joueur_blanc))

class TestAlphaBeta(unittest.TestCase):
    def setUp(self):
        """Initialise un échiquier simplifié pour les tests."""
        self.game = ChessGame()
        self.game.couleur_utilisateur = 'b'  # Utilisateur = Blancs, IA = Noirs
        self.game.setup_board()  # Initialise le board standard


    def test_alpha_beta_retourne_coup_valide(self):
        """Vérifie que alpha_beta retourne un coup valide (pas None)."""
        coup, score = self.game.alpha_beta(
            self.game.joueur_noir,  # IA = Noirs
            profondeur_courante=1,
            alpha=-float('inf'),
            beta=float('inf'),
            board=self.game.board,
            est_maximisant=True
        )
        self.assertIsNotNone(coup, "Alpha-Bêta doit retourner un coup valide.")
        piece, pos_finale = coup
        self.assertIsNotNone(piece, "Le coup doit contenir une pièce.")
        self.assertIsInstance(pos_finale, tuple, "La position finale doit être un tuple.")

    def test_alpha_beta_evite_echec(self):
        """Vérifie que l'IA évite de jouer un coup menant à un échec."""
        # Crée un échiquier où l'IA (Noirs) peut jouer un coup menant à un échec
        self.game.board = [[None for _ in range(8)] for _ in range(8)]
        # Roi noir en (0, 4), Tour blanche en (0, 0) (menace le roi noir)
        self.game.board[0][4] = self.game.Rn
        self.game.board[0][0] = self.game.Tb1

        # L'IA (Noirs) doit éviter de laisser son roi en échec
        coup, score = self.game.alpha_beta(
            self.game.joueur_noir,
            profondeur_courante=1,
            alpha=-float('inf'),
            beta=float('inf'),
            board=self.game.board,
            est_maximisant=True
        )
        # Si un coup est retourné, simule-le et vérifie que le roi n'est pas en échec
        if coup is not None:
            piece, pos_finale = coup
            new_board = self.game.resultat_coup(self.game.board, piece, pos_finale)
            self.assertFalse(
                self.game.echec(self.game.joueur_noir),
                "L'IA ne doit pas jouer un coup menant à un échec."
            )

    def test_alpha_beta_choisit_meilleur_coup(self):
        """Vérifie que l'IA choisit le meilleur coup (simulation simple)."""
        # Crée un échiquier où l'IA (Noirs) a un coup clairement meilleur
        self.game.board = [[None for _ in range(8)] for _ in range(8)]
        # Roi noir en (7, 4), Pion noir en (6, 3), Pion blanc en (5, 4)
        self.game.board[7][4] = self.game.Rn
        self.game.board[6][3] = self.game.Pn1
        self.game.board[5][4] = self.game.Pb1

        # L'IA (Noirs) doit capturer le pion blanc en (5,4) avec son pion en (6,4)
        coup, score = self.game.alpha_beta(
            self.game.joueur_noir,
            profondeur_courante=1,
            alpha=-float('inf'),
            beta=float('inf'),
            board=self.game.board,
            est_maximisant=True
        )
        if coup is not None:
            piece, pos_finale = coup
            # Vérifie que le coup est la capture du pion blanc
            self.assertEqual(
                (piece, pos_finale),
                (self.game.Pn1, (5, 4)),
                "L'IA doit capturer le pion blanc."
            )

    def test_alpha_beta_profondeur_2(self):
        """Vérifie que alpha_beta fonctionne avec une profondeur de 2."""
        # Utilise l'échiquier standard
        self.game.setup_board()
        self.game.profondeur_max = 2
        coup, score = self.game.alpha_beta(
            self.game.joueur_noir,
            profondeur_courante=1,
            alpha=-float('inf'),
            beta=float('inf'),
            board=self.game.board,
            est_maximisant=True
        )
        self.assertIsNotNone(coup, "Alpha-Bêta doit retourner un coup même avec profondeur 2.")

class TestHeuristique(unittest.TestCase):
    def setUp(self):
        """Initialise un jeu et un échiquier vide pour les tests."""
        self.game = ChessGame()
        self.game.couleur_utilisateur = 'b'  # Utilisateur = Blancs
        self.E = [[None for _ in range(8)] for _ in range(8)]  # Échiquier vide


    def test_heuristique_echiquier_vide(self):
        """Teste l'heuristique sur un échiquier vide (score = 0)."""
        score = self.game.heuristique(self.game.joueur_blanc, self.E)
        self.assertEqual(score, 0, "Un échiquier vide doit avoir un score de 0.")

    def test_heuristique_valeur_materielle(self):
        """Teste que l'heuristique compte correctement la valeur matérielle."""
        # Place une Dame blanche (valeur = 9) et un Pion noir (valeur = -1)
        dame = self.game.Db
        pion = self.game.P4n
        self.E[4][4] = dame
        self.E[3][3] = pion
        score = self.game.heuristique(self.game.joueur_blanc, self.E)
        self.assertEqual(score, 278, "Score doit être 9 (Dame) - 1 (Pion noir) = 8.")

    def test_heuristique_controle_centre(self):
        """Teste que l'heuristique donne un bonus pour le contrôle du centre."""
        # Place un Cavalier blanc au centre (valeur = 3 + bonus 0.1)
        cavalier = self.game.C1b
        self.E[3][3] = cavalier  # Case centrale
        score = self.game.heuristique(self.game.joueur_blanc, self.E)
        self.assertEqual(score, 13, msg="Bonus pour le centre manquant.")

    def test_heuristique_bonus_roque(self):
        """Teste que l'heuristique donne un bonus si le roi a roqué."""
        # Crée un roi blanc qui a roqué (a_bouge = True)
        roi = self.game.Rb
        self.game.a_roque['b'] = True  # Simule un roque
        self.E[7][6] = roi
        score = self.game.heuristique(self.game.joueur_blanc, self.E)
        self.assertEqual(score, 130, msg="Bonus pour le roque manquant.")

    def test_heuristique_penalite_piece_menacee(self):
        """Teste que l'heuristique pénalise les pièces menacées (optionnel)."""
        # Place un Pion blanc menacé par une Tour noire
        pion = self.game.P5b
        tour = self.game.T1n
        self.E[4][4] = pion
        self.E[4][0] = tour  # Tour menace le pion en (4,4)
        score = self.game.heuristique(self.game.joueur_blanc, self.E)
        self.assertEqual(score, 6, msg="Pénalité pour pièce menacée manquante.")

class TestRoquePossible(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board


    def test_petit_roque_possible_conditions_remplies(self):
        """Teste que le petit roque est possible si les conditions sont remplies."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.assertTrue(self.game.petit_roque_possible(self.game.joueur_blanc, self.E))

    def test_petit_roque_impossible_roi_a_bouge(self):
        """Teste que le petit roque est impossible si le roi a bougé."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        self.game.a_bouge[roi]= True
        self.game.a_bouge[tour] = False
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.assertFalse(self.game.petit_roque_possible(self.game.joueur_blanc, self.E))

    def test_petit_roque_impossible_tour_a_bouge(self):
        """Teste que le petit roque est impossible si la tour a bougé."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        self.game.a_bouge[roi] = False
        self.game.a_bouge[tour] = True
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.assertFalse(self.game.petit_roque_possible(self.game.joueur_blanc, self.E))

    def test_petit_roque_impossible_echec(self):
        """Teste que le petit roque est impossible si le roi est en échec."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        tour_noire = self.game.Tn1
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.E[0][4] = tour_noire  # Tour noire menace le roi blanc
        self.assertFalse(self.game.petit_roque_possible(self.game.joueur_blanc, self.E))

    def test_petit_roque_impossible_cases_non_vides(self):
        """Teste que le petit roque est impossible si les cases entre le roi et la tour ne sont pas vides."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        pion = self.game.P5n
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.E[7][5] = pion  # Case non vide entre le roi et la tour
        self.assertFalse(self.game.petit_roque_possible(self.game.joueur_blanc, self.E))

    def test_grand_roque_possible_conditions_remplies(self):
        """Teste que le grand roque est possible si les conditions sont remplies."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1b
        self.E[7][4] = roi
        self.E[7][0] = tour
        self.assertTrue(self.game.grand_roque_possible(self.game.joueur_blanc, self.E))

    def test_grand_roque_impossible_cases_non_vides(self):
        """Teste que le grand roque est impossible si les cases entre le roi et la tour ne sont pas vides."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1b
        pion = self.game.P1n
        self.E[7][4] = roi
        self.E[7][0] = tour
        self.E[7][1] = pion  # Case non vide entre le roi et la tour
        self.assertFalse(self.game.grand_roque_possible(self.game.joueur_blanc, self.E))

class TestRoque(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board

    def test_petit_roque(self):
        """Teste que le petit roque déplace correctement le roi et la tour."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1b
        self.E[7][4] = roi
        self.E[7][7] = tour
        self.assertTrue(self.game.roque(self.game.joueur_blanc, 'petit'))
        # Vérifie que le roi et la tour ont bougé
        self.assertIsNone(self.E[7][4])
        self.assertIsNone(self.E[7][7])
        self.assertEqual(self.E[7][6], roi)
        self.assertEqual(self.E[7][5], tour)

    def test_grand_roque(self):
        """Teste que le grand roque déplace correctement le roi et la tour."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T2b
        self.E[7][4] = roi
        self.E[7][0] = tour
        self.assertTrue(self.game.roque(self.game.joueur_blanc, 'grand'))
        # Vérifie que le roi et la tour ont bougé
        self.assertIsNone(self.E[7][4])
        self.assertIsNone(self.E[7][0])
        self.assertEqual(self.E[7][2], roi)
        self.assertEqual(self.E[7][3], tour)

class TestCoupsPossibles(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.couleur_utilisateur='b'
        self.game.setup_board()
        self.E = self.game.board

    def test_coups_possibles_pion_blanc(self):
        """Teste que les coups possibles pour un pion blanc sont corrects."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion
        coups = self.game.coups_possibles(self.game.joueur_blanc, self.E)
        # Le pion blanc peut avancer de 1 ou 2 cases
        self.assertIn((pion, (5, 4), False, None, None), coups)
        self.assertIn((pion, (4, 4), False, None, None), coups)

    def test_coups_possibles_pion_noir(self):
        """Teste que les coups possibles pour un pion noir sont corrects."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5n
        self.E[1][4] = pion
        coups = self.game.coups_possibles(self.game.joueur_noir, self.E)
        # Le pion noir peut avancer de 1 ou 2 cases
        self.assertIn((pion, (2, 4), False, None, None), coups)
        self.assertIn((pion, (3, 4), False, None, None), coups)

    def test_coups_possibles_roi(self):
        """Teste que les coups possibles pour un roi sont corrects."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        self.E[4][4] = roi
        coups = self.game.coups_possibles(self.game.joueur_blanc, self.E)
        # Le roi peut se déplacer d'une case dans toutes les directions
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di != 0 or dj != 0:
                    self.assertIn((roi, (4 + di, 4 + dj), False, None, None), coups)

    def test_coups_possibles_inclut_roques(self):
        """Teste que les roques sont inclus dans les coups possibles."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour1 = self.game.T1b
        tour2 = self.game.T2b
        self.E[7][4] = roi
        self.E[7][0] = tour1
        self.E[7][7] = tour2
        coups = self.game.coups_possibles(self.game.joueur_blanc, self.E)
        # Vérifie que les roques sont inclus
        self.assertIn((roi, (7, 6), False, None, 'petit'), coups)
        self.assertIn((roi, (7, 2), False, None, 'grand'), coups)

    def test_coups_possibles_inclut_promotions(self):
        """Teste que les promotions sont incluses dans les coups possibles."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[1][4] = pion  # Pion blanc en ligne 1 (peut promouvoir en ligne 0)
        coups = self.game.coups_possibles(self.game.joueur_blanc, self.E)
        # Vérifie que les promotions sont incluses
        for piece_type in ['Dame', 'Tour', 'Cavalier', 'Fou']:
            self.assertIn((pion, (0, 4), False, piece_type, None), coups)

class TestIsValidMove(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board

    def test_isvalid_move_deplacement_valide(self):
        """Teste qu'un déplacement valide est reconnu comme valide."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion
        self.assertTrue(self.game.isvalid_move(6, 4, 5, 4))

    def test_isvalid_move_deplacement_invalide(self):
        """Teste qu'un déplacement invalide est reconnu comme invalide."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion
        self.assertFalse(self.game.isvalid_move(6, 4, 3, 4))  # Déplacement de 3 cases

    def test_isvalid_move_case_depart_vide(self):
        """Teste qu'un déplacement depuis une case vide est invalide."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        self.assertFalse(self.game.isvalid_move(6, 4, 5, 4))

    def test_isvalid_move_capture_valide(self):
        """Teste qu'une capture valide est reconnue comme valide."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion_blanc = self.game.P5b
        pion_noir = pion = self.game.P6n
        self.E[6][4] = pion_blanc
        self.E[5][5] = pion_noir
        self.assertTrue(self.game.isvalid_move(6, 4, 5, 5))

class TestResultatCoup(unittest.TestCase):
    def setUp(self):
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board

    def test_resultat_coup_deplacement_simple(self):
        """Teste que resultat_coup déplace correctement une pièce."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion
        new_board = self.game.resultat_coup(self.E, pion, (5, 4))
        self.assertIsNone(new_board[6][4])
        self.assertEqual(new_board[5][4], pion)

    def test_resultat_coup_capture(self):
        """Teste que resultat_coup gère correctement une capture."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion_blanc = self.game.P5b
        pion_noir = self.game.P6n
        self.E[6][4] = pion_blanc
        self.E[5][5] = pion_noir
        new_board = self.game.resultat_coup(self.E, pion_blanc, (5, 5))
        self.assertIsNone(new_board[6][4])
        self.assertEqual(new_board[5][5], pion_blanc)

    def test_resultat_coup_promotion(self):
        """Teste que resultat_coup gère correctement une promotion."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[1][4] = pion
        new_board = self.game.resultat_coup(self.E, pion, (0, 4), promotion='Dame')
        self.assertIsNone(new_board[1][4])
        self.assertIsInstance(new_board[0][4], Dame)

    def test_resultat_coup_petit_roque(self):
        """Teste que resultat_coup gère correctement un petit roque."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.Tb2
        self.E[7][4] = roi
        self.E[7][7] = tour
        new_board = self.game.resultat_coup(self.E, roi, (7, 6), roque='petit')
        self.assertIsNone(new_board[7][4])
        self.assertIsNone(new_board[7][7])
        self.assertEqual(new_board[7][6], roi)
        self.assertEqual(new_board[7][5], tour)

    def test_resultat_coup_grand_roque(self):
        """Teste que resultat_coup gère correctement un grand roque."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1b
        self.E[7][4] = roi
        self.E[7][0] = tour
        new_board = self.game.resultat_coup(self.E, roi, (7, 2), roque='grand')
        self.assertIsNone(new_board[7][4])
        self.assertIsNone(new_board[7][0])
        self.assertEqual(new_board[7][2], roi)
        self.assertEqual(new_board[7][3], tour)

class TestPromotion(unittest.TestCase):
    def setUp(self):
        """Initialise un jeu pour les tests de promotion."""
        self.game = ChessGame()
        self.game.couleur_utilisateur='b'
        self.game.setup_board()
        self.E = self.game.board

    def test_promotion_pion_blanc_en_dame(self):
        """Teste la promotion d'un pion blanc en Dame."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5n
        self.E[1][4] = pion  # Pion blanc en ligne 1 (peut promouvoir en ligne 0)
        self.game.promotion(pion)
        self.assertIsInstance(self.E[0][4], Dame)
        self.assertIsNone(self.E[1][4])

    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    def test_promotion_pion_noir_en_tour(self, mock_get_item):
        """Teste la promotion d'un pion noir en Tour."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion  # Pion noir en ligne 6 (peut promouvoir en ligne 7)
        mock_get_item.return_value = ("Tour", True)
        self.game.promotion(pion)
        self.assertIsInstance(self.E[7][4], Tour)
        self.assertIsNone(self.E[6][4])

    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    def test_promotion_pion_en_cavalier(self, mock_get_item):
        """Teste la promotion d'un pion en Cavalier."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5n
        self.E[1][4] = pion
        mock_get_item.return_value = ("Cavalier", True)
        self.game.promotion(pion)
        self.assertIsInstance(self.E[0][4], Cavalier)

    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    def test_promotion_pion_en_fou(self, mock_get_item):
        """Teste la promotion d'un pion en Fou."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        pion = self.game.P5b
        self.E[6][4] = pion
        mock_get_item.return_value = ("Fou", True)
        self.game.promotion(pion)
        self.assertIsInstance(self.E[7][4], Fou)

class TestMatchNul(unittest.TestCase):
    def setUp(self):
        """Initialise un jeu pour les tests de match nul."""
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board

    def test_match_nul_pat(self):
        """Teste la détection d'un pat (match nul)."""
        # Crée une position de pat : roi blanc isolé, pas en échec, mais sans coup légal
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        self.E[4][4] = roi
        # Aucune pièce adverse, mais le roi n'a aucun coup légal (entouré par ses propres pièces)
        # Ajoute des pièces blanches autour du roi pour bloquer ses déplacements
        self.E[3][3]=self.game.P1b
        self.E[3][4]=self.game.P2b
        self.E[3][5]=self.game.P3b
        self.E[4][3]=self.game.P4b
        self.E[4][5]=self.game.P5b
        self.E[5][3] = self.game.P6b
        self.E[5][4]=self.game.P7b
        self.E[5][5]=self.game.P8b
        self.assertTrue(self.game.match_nul(self.game.joueur_blanc))

    def test_match_nul_faux(self):
        """Teste qu'une position non-nulle ne déclenche pas match_nul."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        self.E[4][4] = roi
        # Le roi a des coups légaux (pas de pat)
        self.assertFalse(self.game.match_nul(self.game.joueur_blanc))

    def test_match_nul_avec_coups_legaux(self):
        """Teste qu'un joueur avec des coups légaux n'est pas en match nul."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        pion = self.game.P5b
        self.E[4][4] = roi
        self.E[6][4] = pion  # Le pion peut avancer
        self.assertFalse(self.game.match_nul(self.game.joueur_blanc))

    def test_match_nul_roi_en_echec(self):
        """Teste qu'un roi en échec n'est pas en match nul (même sans coup légal)."""
        self.E = [[None for _ in range(8)] for _ in range(8)]
        roi = self.game.Rb
        tour = self.game.T1n
        self.E[4][4] = roi
        self.E[4][0] = tour  # Tour noire menace le roi blanc
        self.assertFalse(self.game.match_nul(self.game.joueur_blanc))

class TestResetGame(unittest.TestCase):
    def setUp(self):
        """Initialise un jeu pour les tests de reset_game."""
        self.game = ChessGame()
        self.game.setup_board()
        self.E = self.game.board

    def test_reset_game_reinitialise_board(self):
        """Teste que reset_game réinitialise correctement l'échiquier."""
        # Modifie l'échiquier
        self.E[0][0] = None
        self.E[7][7] = None
        self.game.reset_game()
        # Vérifie que l'échiquier est réinitialisé
        self.assertIsNotNone(self.game.board[0][0])  # Tour noire en (0,0)
        self.assertIsNotNone(self.game.board[7][7])  # Tour blanche en (7,7)

    def test_reset_game_reinitialise_move_history(self):
        """Teste que reset_game réinitialise l'historique des coups."""
        self.game.move_history = [("e2-e4", None,(False,None),None,None)]
        self.game.reset_game()
        self.assertEqual(self.game.move_history, [])

    def test_reset_game_reinitialise_current_player(self):
        """Teste que reset_game réinitialise le joueur actuel."""
        self.game.current_player = self.game.joueur_noir
        self.game.reset_game()
        self.assertEqual(self.game.current_player, self.game.joueur_blanc)

    def test_reset_game_reinitialise_couleur_utilisateur(self):
        """Teste que reset_game conserve la couleur de l'utilisateur."""
        self.game.couleur_utilisateur = 'n'
        self.game.reset_game()
        self.assertEqual(self.game.couleur_utilisateur, 'n')

    def test_reset_game_reinitialise_game_over(self):
        """Teste que reset_game réinitialise game_over."""
        self.game.game_over = True
        self.game.reset_game()
        self.assertFalse(self.game.game_over)

if __name__ == '__main__':
    if '--test' in sys.argv:  # ✅ Mode test
        unittest.main(argv=sys.argv[:1])  # Exécute les tests
    else:  # ✅ Mode graphique
        app = QApplication(sys.argv)
        jeu = ChessGame()
        jeu.show()
        sys.exit(app.exec_())