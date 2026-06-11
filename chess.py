from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel,QDesktopWidget,QMessageBox,QMainWindow,QApplication
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from functools import partial
from classe_Piece_et_filles_et_joueur import *
import sqlite3
from datetime import datetime
import copy, random, numpy as np

# Interface de jeu
class Ui_Jeu_d_echecs(object):
    def setupUi(self, Jeu_d_echecs):
        # Configuration de la fenêtre principale
        Jeu_d_echecs.setObjectName("Jeu_d_echecs")
        Jeu_d_echecs.resize(979, 600)

        # Widget central
        self.centralwidget = QtWidgets.QWidget(Jeu_d_echecs)
        self.centralwidget.setObjectName("centralwidget")
        Jeu_d_echecs.setCentralWidget(self.centralwidget)

        # GroupBox pour l'échiquier
        self.Echiquier = QtWidgets.QGroupBox(self.centralwidget)
        self.Echiquier.setGeometry(QtCore.QRect(30, 30, 400, 400))
        self.Echiquier.setMinimumSize(QtCore.QSize(400, 400))
        self.Echiquier.setMaximumSize(QtCore.QSize(400, 400))
        self.Echiquier.setTitle("")
        self.Echiquier.setObjectName("Echiquier")

        # QGridLayout pour l'échiquier (sans marges)
        self.gridLayout = QtWidgets.QGridLayout(self.Echiquier)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges
        self.gridLayout.setSpacing(0)  # Supprime les espacements entre les cases
        self.gridLayout.setObjectName("gridLayout")

        # Création des 64 cases (boutons) avec leurs couleurs
        for row in range(8):
            for col in range(8):
                button_name = self.position_to_notation(row,col)  # Ex: A1, B1, ..., H8
                button = QtWidgets.QPushButton(self.Echiquier)
                button.setMinimumSize(QtCore.QSize(50, 50))
                button.setMaximumSize(QtCore.QSize(50, 50))
                button.setText("")
                button.setObjectName(button_name)



                # Ajouter le bouton au gridLayout
                self.gridLayout.addWidget(button, row, col)

        # Autres éléments de l'interface (listWidget, boutons, etc.)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(520, 10, 291, 311))
        self.listWidget.setObjectName("listWidget")

        # Boutons en bas à droite
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(520, 340, 295, 52))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.Abandonner = QtWidgets.QPushButton("Abandonner", self.layoutWidget)
        self.Rentrer = QtWidgets.QPushButton("Rentrer", self.layoutWidget)
        self.Rejouer = QtWidgets.QPushButton("Rejouer", self.layoutWidget)

        self.horizontalLayout_3.addWidget(self.Abandonner)
        self.horizontalLayout_3.addWidget(self.Rentrer)
        self.horizontalLayout_3.addWidget(self.Rejouer)

        # Boutons de thème et PNG
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(520, 390, 203, 52))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.theme = QtWidgets.QPushButton("Thème", self.layoutWidget1)
        self.Png = QtWidgets.QPushButton("PNG", self.layoutWidget1)

        self.horizontalLayout_2.addWidget(self.theme)
        self.horizontalLayout_2.addWidget(self.Png)

        # Barre de menu et barre de statut
        self.menubar = QtWidgets.QMenuBar(Jeu_d_echecs)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 979, 26))
        Jeu_d_echecs.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Jeu_d_echecs)
        Jeu_d_echecs.setStatusBar(self.statusbar)

        self.retranslateUi(Jeu_d_echecs)
        QtCore.QMetaObject.connectSlotsByName(Jeu_d_echecs)



    # Pour la traduction en d'autres langues (pas obligatoire)
    def retranslateUi(self, Jeu_d_echecs):
        _translate = QtCore.QCoreApplication.translate
        Jeu_d_echecs.setWindowTitle(_translate("Jeu_d_echecs", "Jeu d\'échecs"))
        buttons_text = {
            self.Abandonner: "Abandonner",
            self.Rentrer: "Rentrer",
            self.Rejouer: "Rejouer",
            self.theme: "Thème Clair",
            self.Png: "PNG de la partie"
        }
        for button, text in buttons_text.items():
            button.setText(_translate("Jeu_d_echecs", text))

    def position_to_notation(self, row, col):
        pass

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Bienvenue")
        self.setModal(True)  # Bloque l'interaction avec la fenêtre principale
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)  # Garde la barre de titre

        # Active la transparence si nécessaire
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Marges internes

        # Message de bienvenue
        label = QLabel("Bienvenue dans le jeu d'échecs !")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        layout.addWidget(label)

        # Bouton "Commencer une partie"
        self.start_button = QPushButton("Commencer une partie")
        self.start_button.setStyleSheet("""
            font-size: 18px;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        """)
        self.start_button.clicked.connect(self.accept)  # Ferme la fenêtre et lance le jeu
        layout.addWidget(self.start_button)

        # Bouton "Fermer" (optionnel)
        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("""
            font-size: 16px;
            padding: 8px;
            background-color: #f44336;
            color: white;
            border-radius: 5px;
        """)
        close_button.clicked.connect(self.reject)  # Ferme la fenêtre sans lancer le jeu
        layout.addWidget(close_button)

        # Style du fond
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 230);
            border-radius: 15px;
            border: 2px solid black;
        """)

        # Ajuste la taille en fonction de l'écran
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width() // 4, screen.height() // 5)

# Implémentation d'une partie de jeu

class CouleurDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choisir votre couleur")
        self.setModal(True)

        layout = QVBoxLayout(self)
        label = QLabel("Avec quelle couleur voulez-vous jouer ?")
        layout.addWidget(label)

        self.blancs_button = QPushButton("Blancs")
        self.noirs_button = QPushButton("Noirs")
        layout.addWidget(self.blancs_button)
        layout.addWidget(self.noirs_button)

        # Stocke le choix dans un attribut
        self.choice = None

        self.blancs_button.clicked.connect(lambda: self._on_choice('b'))
        self.noirs_button.clicked.connect(lambda: self._on_choice('n'))

    def _on_choice(self, couleur):
        print(f"Choix : {couleur}")
        self.choice = couleur
        self.accept()  # Ferme la boîte de dialogue

    def get_couleur(self):
        """Affiche la boîte de dialogue et retourne la couleur choisie."""
        print("Affichage de la boîte de dialogue...")
        if self.exec_() == QDialog.Accepted:
            return self.choice
        return 'b'  # Valeur par défaut si l'utilisateur ferme la fenêtre

class IAThread(QThread):
    move_found = pyqtSignal(int, int, int, int)  # Signal pour envoyer le coup trouvé
    error_occurred = pyqtSignal(str)
    def __init__(self, board, couleur_ia, profondeur_max, joueur_noir, joueur_blanc, parent=None):
        super().__init__(parent)
        self.board = copy.deepcopy(board)
        self.couleur_ia = couleur_ia
        self.profondeur_max = profondeur_max
        self.joueur_noir = joueur_noir  # ✅ Reçu depuis ChessGame
        self.joueur_blanc = joueur_blanc  # ✅ Reçu depuis ChessGame
        self.stop_requested = False
        self.parent=parent

    def run(self):
        try:
            if self.parent is None:
                self.error_occurred.emit("Erreur : parent est None")
                return
            # ✅ Détermine le joueur IA
            ia = self.joueur_noir if self.couleur_ia == 'n' else self.joueur_blanc

            # ✅ Appelle alpha_beta avec ia en premier argument
            best_move, _ = self.parent.alpha_beta(
                ia,  # ✅ Joueur IA
                profondeur_courante=1,
                alpha=-float('inf'),
                beta=float('inf'),
                board=self.board,
                est_maximisant=False
            )

            if self.stop_requested:
                return

            if best_move is not None:
                if len(best_move) != 5:  # ✅ Vérifie que best_move a 5 éléments
                    self.error_occurred.emit(f"Coup invalide : {best_move}")
                    return
                piece, pos, prise_en_passant, promotion, roque = best_move
                from_row, from_col = piece.position(self.board)
                to_row, to_col = pos

                if from_row is not None and from_col is not None:
                    self.move_found.emit(from_row, from_col, to_row, to_col)
                else:
                    self.error_occurred.emit("Position de la pièce introuvable.")
            else:
                self.error_occurred.emit("L'IA n'a pas trouvé de coup valide.")

        except Exception as e:
            self.error_occurred.emit(f"Erreur dans IAThread: {e}")

    def stop(self):
        self.stop_requested = True
        self.quit()

class ChessGame(QMainWindow, Ui_Jeu_d_echecs):   #Héritage multiple: la classe créée hérite de deux classes mères

    current_player: Joueur

    def __init__(self):
        super().__init__()
        self.couleur_utilisateur = None
        self.setupUi(self)
        self.selected_piece = None
        self.ia_thread=None


        # Affiche la fenêtre de bienvenue
        self.welcome_dialog = WelcomeDialog(self)
        self.welcome_dialog.exec_()  # Affiche la fenêtre modale


        #créer les pièces
        [self.T1n, self.C1n, self.F1n, self.Dn, self.Rn, self.F2n, self.C2n, self.T2n] = self.liste_pieces('n')
        self.Pieces_noires = [self.T1n, self.C1n, self.F1n, self.Dn, self.Rn, self.F2n, self.C2n, self.T2n]
        [self.T1b, self.C1b, self.F1b, self.Db, self.Rb, self.F2b, self.C2b, self.T2b] = self.liste_pieces('b')
        self.Pieces_blanches = [self.T1b, self.C1b, self.F1b, self.Db, self.Rb, self.F2b, self.C2b, self.T2b]
        self.Pions_noirs=[]
        self.Pions_blancs=[]

        # Initialise un échiquier 8x8 vide
        self.board = []  #représente l'échiquier et contient toutes les pièces vivantes
        self.joueur_blanc = Joueur('b')
        self.joueur_noir = Joueur('n')
        self.current_player = self.joueur_blanc
        self.couleur_ia=None
        self.profondeur_max = 2
        self.game_over = False
        self.pieces_prises = []
        self.moved_pieces = []  #utile pour la prise en passant
        self.move_history = []
        self.pion_avance_de_2_cases={}
        self.a_roque={'n':False,'b':False}
        self.a_bouge = {self.T1n: False, self.Rn: False, self.T2n: False, self.T1b: False, self.Rb: False, self.T2b: False}
        self.choisir_couleur()  # Message au démarrage

        # Initialise la base de données
        self.conn = sqlite3.connect('echecs_games.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS parties(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, result TEXT, winner TEXT, moves TEXT )''')
        self.conn.commit()


        #connexion des boutons
        self.Abandonner.clicked.connect(self.on_abandon_clicked)
        self.Rejouer.clicked.connect(self.reset_game)
        self.Rentrer.clicked.connect(self.undo_last_move)

    def liste_pieces(self,couleur):
        c = couleur
        return [Tour(c), Cavalier(c), Fou(c), Dame(c), Roi(c), Fou(c), Cavalier(c), Tour(c)]

    def choisir_couleur(self):
        couleur_dialog = CouleurDialog(self)
        self.couleur_utilisateur = couleur_dialog.get_couleur()
        self.couleur_ia = 'n' if self.couleur_utilisateur == 'b' else 'b'
        self.setup_board()
        self.start_game()

    def setup_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        depart_noir=1 if self.couleur_utilisateur=='b' else 6
        depart_blanc=6 if self.couleur_utilisateur=='b' else 1
        [self.P1b, self.P2b, self.P3b, self.P4b, self.P5b, self.P6b, self.P7b, self.P8b] = [Pion('b', i, depart_blanc) for i in range(8)]
        self.Pions_blancs = [self.P1b, self.P2b, self.P3b, self.P4b, self.P5b, self.P6b, self.P7b, self.P8b]
        [self.P1n, self.P2n, self.P3n, self.P4n, self.P5n, self.P6n, self.P7n, self.P8n] = [Pion('n', i, depart_noir) for i in range(8)]
        self.Pions_noirs = [self.P1n, self.P2n, self.P3n, self.P4n, self.P5n, self.P6n, self.P7n, self.P8n]
        self.pion_avance_de_2_cases = {pion: False for pion in self.Pions_noirs + self.Pions_blancs}

        positions_initiales = {
            self.T1n: (0, 0), self.C1n: (0, 1), self.F1n: (0, 2), self.Dn: (0, 3), self.Rn: (0, 4), self.F2n: (0, 5), self.C2n: (0, 6), self.T2n: (0, 7),
            self.P1n: (1, 0), self.P2n: (1, 1), self.P3n: (1, 2), self.P4n: (1, 3), self.P5n: (1, 4), self.P6n: (1, 5), self.P7n: (1, 6), self.P8n: (1, 7),
            self.P1b: (6, 0), self.P2b: (6, 1), self.P3b: (6, 2), self.P4b: (6, 3), self.P5b: (6, 4), self.P6b: (6, 5), self.P7b: (6, 6), self.P8b: (6, 7),
            self.T1b: (7, 0), self.C1b: (7, 1), self.F1b: (7, 2), self.Db: (7, 3), self.Rb: (7, 4), self.F2b: (7, 5), self.C2b: (7, 6), self.T2b: (7, 7)
        }

        Pieces_haut=self.Pieces_noires if self.couleur_utilisateur=='b' else self.Pieces_blanches
        Pions_haut=self.Pions_noirs if self.couleur_utilisateur=='b' else self.Pions_blancs
        Pieces_bas=self.Pieces_blanches if self.couleur_utilisateur=='b' else self.Pieces_noires
        Pions_bas=self.Pions_blancs if self.couleur_utilisateur=='b' else self.Pions_noirs
        col: int
        # Place les pièces noires/blanches (ligne 0 ou 7)
        for col in range(8):  # ✅ col va de 0 à 7
            if col < len(Pieces_haut):  # ✅ Vérifie que col est dans la liste
                self.board[0][col] = Pieces_haut[col]

        # Place les pièces blanches/noires (ligne 7 ou 0)
        for col in range(8):
            if col < len(Pieces_bas):
                self.board[7][col] = Pieces_bas[col]

        # Place les pions noirs/blancs (ligne 1 ou 6)
        for col in range(8):
            if col < len(Pions_haut):
                self.board[1][col] = Pions_haut[col]

        # Place les pions blancs/noirs (ligne 6 ou 1)
        for col in range(8):
            if col < len(Pions_bas):
                self.board[6][col] = Pions_bas[col]

        # Met à jour l'interface
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                button_name = self.position_to_notation(row, col)
                button = self.findChild(QtWidgets.QPushButton, button_name)
                if button:
                    try:
                        button.clicked.disconnect()  # ✅ Déconnecte les anciens signaux
                    except TypeError:
                        pass
                    if (row + col) % 2 == 0:
                        button.setStyleSheet("background-color: white; font-size: 24px;")
                    else:
                        button.setStyleSheet("background-color: blue; font-size: 24px;")

                    if piece is not None:
                        button.setText(str(piece))
                    else:
                        button.setText("")

                    button.clicked.connect(partial(self.on_case_clicked, row, col))

    def start_game(self):
        # Utilise un QTimer pour éviter de bloquer l'interface
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.check_game_state)
        self.game_timer.start(100)  # Vérifie toutes les 100 ms

    def on_case_clicked(self, row, col):
        if self.selected_piece is None:  # Premier clic
            piece = self.board[row][col]
            if piece is not None and self.current_player.couleur == piece.couleur:
                self.selected_piece = (row, col)
                button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(row,col))
                self.reset_highlight()
                button.setStyleSheet("background-color: yellow; font-size: 24px;")


                # Gestion de la prise en passant
                m, n = None, None
                if isinstance(piece, Pion) and len(self.moved_pieces)>0:
                    i, j = piece.position(self.board)
                    last_piece = self.moved_pieces[-1]
                    last_pos = last_piece.position(self.board)
                    if isinstance(last_piece, Pion) and last_piece in self.pion_avance_de_2_cases.keys() and self.pion_avance_de_2_cases[last_piece]==True:
                        if last_pos == (i, j - 1):  # Pion à gauche
                            m, n = (i - 1, j - 1) if piece.couleur == self.couleur_utilisateur else (i + 1, j - 1)
                        elif last_pos == (i, j + 1):  # Pion à droite
                            m, n = (i - 1, j + 1) if piece.couleur == self.couleur_utilisateur else (i + 1, j + 1)

                # Liste des cases accessibles (incluant la prise en passant)
                L = piece.cases_accessibles(self.board)
                if (m, n)!=(None,None):
                    L.append((m, n))

                # Surbrillance des cases accessibles
                for (r, c) in L:
                    case_button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(r,c))
                    if case_button:
                        current_style = case_button.styleSheet()
                        case_button.setStyleSheet(f"{current_style} border: 1px solid black;")

            else:
                self.selected_piece = None
                self.reset_highlight()
        else:  # Deuxième clic

            start_row, start_col = self.selected_piece
            self.reset_highlight()
            self.move_piece(start_row, start_col, row, col)
            self.selected_piece = None


    #code du jeu


    def check_game_state(self):
        if self.echec_et_mat(self.current_player):
            self.game_timer.stop()
            if self.ia_thread is not None and self.ia_thread.isRunning():
                self.ia_thread.stop()
            winner = "Blancs" if self.current_player.couleur == 'n' else "Noirs"
            self.show_end_game_dialog("Échec et mat", winner)
        elif self.match_nul(self.current_player):
            self.game_timer.stop()
            if self.ia_thread is not None and self.ia_thread.isRunning():
                self.ia_thread.stop()
            self.show_end_game_dialog("Match nul", None)
        else:
            if (self.current_player.couleur == self.couleur_ia) and (self.ia_thread is None or not self.ia_thread.isRunning()):  # Tour de l'IA
                QTimer.singleShot(1000, self.ia_move)
            else:
                pass

    def reset_highlight(self):
        # Réinitialise la couleur de toutes les cases
        for row in range(8):
            for col in range(8):
                button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(row,col))
                if button:
                    color = "white" if (row + col) % 2 == 0 else "blue"
                    button.setStyleSheet(f"background-color: {color}; font-size: 24px;")

    def isvalid_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        if piece is None:
            return False

        # Gestion de la prise en passant
        m, n = None, None
        if isinstance(piece, Pion) and len(self.moved_pieces) > 0:
            i, j = piece.position(self.board)
            last_piece = self.moved_pieces[-1]
            last_pos = last_piece.position(self.board)
            if isinstance(last_piece, Pion) and last_piece in self.pion_avance_de_2_cases.keys() and self.pion_avance_de_2_cases[last_piece] == True:
                if last_pos == (i, j - 1):  # Pion à gauche
                    m, n = (i - 1, j - 1) if piece.couleur == self.couleur_utilisateur else (i + 1, j - 1)
                elif last_pos == (i, j + 1):  # Pion à droite
                    m, n = (i - 1, j + 1) if piece.couleur == self.couleur_utilisateur else (i + 1, j + 1)

        # Liste des cases accessibles (incluant la prise en passant)
        L = piece.cases_accessibles(self.board)
        if (m, n) is not None:
            L.append((m, n))

        # Vérifie si le mouvement est dans les cases accessibles
        if (to_row, to_col) not in L:
            return False

        # Vérifie si le joueur n'est pas en échec après le mouvement
        aux_to = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        is_valid = not self.echec(self.current_player)

        # Restaure l'échiquier
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = aux_to

        return is_valid

    def move_piece(self, from_row, from_col, to_row, to_col):


        piece= self.board[from_row][from_col]
        if piece is None:
            return

        roque=None
        promotion=None
        piece_prise_en_passant,sa_position = None,None

        # Roque
        petit_roque_possible,grand_roque_possible=self.roque_possible(self.current_player)
        R = self.Rn if self.current_player.couleur == 'n' else self.Rb
        i, j = R.position(self.board)

        if petit_roque_possible or grand_roque_possible:
            if petit_roque_possible:
                print("petit_roque_possible")
                if piece == R and (to_row, to_col) == (i, j + 2):
                    self.roque(self.current_player, 'petit')
                    roque = 'petit'
                    self.a_roque[self.current_player.couleur] = True
            elif grand_roque_possible:
                if piece == R and (to_row, to_col) == (i, j - 2):
                    self.roque(self.current_player, 'grand')
                    roque = 'grand'
                    self.a_roque[self.current_player.couleur] = True

        if not self.isvalid_move(from_row, from_col, to_row, to_col):
            return

        # Déplacement normal
        self.board[from_row][from_col] = None
        self.board[to_row][to_col] = piece

        # Mise à jour des attributs
        self.moved_pieces.append(piece)
        if isinstance(piece,Pion):
            if self.pion_avance_de_2_cases and piece in self.pion_avance_de_2_cases.keys():
                self.pion_avance_de_2_cases[piece]=(abs(to_row-from_row)==2)
        if piece in self.a_bouge.keys():
            self.a_bouge[piece] = True


        #Prise en passant (domine sur une prise classique)
        piece_prise_en_passant,sa_position = self.prise_en_passant(piece)
        if piece_prise_en_passant is not None:
            self.pieces_prises.append(piece_prise_en_passant)
            self.board[sa_position[0]][sa_position[1]] = None
        else:
            self.pieces_prises.append(self.board[to_row][to_col])


        # Promotion
        promotion= self.promotion(piece)
        self.board[to_row][to_col] = promotion[1]

        # Mise à jour de l'UI
        from_button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(from_row,from_col))
        to_button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(to_row,to_col))
        if from_button:
            from_button.setText("")
        if to_button:
            to_button.setText(str(piece))

        # Notation du coup
        move_notation = self.notation_move(piece, to_row, to_col, promotion, piece_prise_en_passant,roque)
        internal_notation = (self.position_to_notation(from_row,from_col)+f"-{move_notation}",roque,promotion,piece_prise_en_passant,sa_position)
        self.move_history.append(internal_notation)
        print("move enregistré: ",internal_notation)
        self.listWidget.addItem(move_notation)


        self.selected_piece = None
        self.reset_highlight()
        if to_button:
            to_button.setStyleSheet("background-color: yellow; font-size: 24px;")

        adversaire= self.joueur_noir if self.current_player==self.joueur_blanc else self.joueur_blanc

        # Échec
        if self.echec(adversaire):
            R = self.Rn if adversaire.couleur == 'n' else self.Rb
            row, col = R.position(self.board)
            button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(row,col))
            if button:
                button.setStyleSheet("background-color: red; font-size: 24px;")

        # Changement de joueur
        self.current_player = self.joueur_noir if self.current_player == self.joueur_blanc else self.joueur_blanc


        # Test de l'état du jeu
        self.check_game_state()

    def roque_possible(self, J):
        """
        Vérifie si un roque (petit ou grand) est possible pour le joueur J.

        Paramètres
        ----------
        J : Joueur
            Le joueur pour lequel vérifier le roque.

        Retourne
        -------
        str or bool
            'petit' si le petit roque est possible,
            'grand' si le grand roque est possible,
            False si aucun roque n'est possible.
        """
        petit_roque,grand_roque=False,False

        if J.couleur == 'n':
            roi_petit = self.Rn
            tour_petit = self.T2n
            roi_grand = self.Rn
            tour_grand = self.T1n
        else:
            roi_petit = self.Rb
            tour_petit = self.T2b
            roi_grand = self.Rb
            tour_grand = self.T1b

        if self.a_roque[J.couleur] == True:
            return False


        # Vérifie le petit roque
        if (not self.a_bouge[roi_petit] and not self.a_bouge[tour_petit] and
                not self.echec(J) and
                self.board[roi_petit.position(self.board)[0]][roi_petit.position(self.board)[1] + 1] is None and
                self.board[roi_petit.position(self.board)[0]][roi_petit.position(self.board)[1] + 2] is None):

            # Simule le roque pour vérifier que le roi ne passe pas par une case en échec (ici case intermédiaire)
            old_board = copy.deepcopy(self.board)
            i, j = roi_petit.position(self.board)
            self.board[i][j] = None
            self.board[i][j + 1] = roi_petit
            if not self.echec(J):
                self.board = old_board
                self.board[i][j] = None
                self.board[i][j + 2] = roi_petit
                if not self.echec(J):
                    petit_roque = 'petit'
            self.board = old_board

        # Vérifie le grand roque
        if (not self.a_bouge[roi_grand] and not self.a_bouge[tour_grand] and
                not self.echec(J) and
                self.board[roi_grand.position(self.board)[0]][roi_grand.position(self.board)[1] - 1] is None and
                self.board[roi_grand.position(self.board)[0]][roi_grand.position(self.board)[1] - 2] is None and
                self.board[roi_grand.position(self.board)[0]][roi_grand.position(self.board)[1] - 3] is None):

            # Simule le roque pour vérifier que le roi ne passe pas par une case en échec
            old_board = copy.deepcopy(self.board)
            i, j = roi_petit.position(self.board)
            self.board[i][j] = None
            self.board[i][j - 1] = roi_petit
            if not self.echec(J):
                self.board = old_board
                self.board[i][j] = None
                self.board[i][j - 2] = roi_petit
                if not self.echec(J):
                    grand_roque = 'grand'
            self.board = old_board

        return petit_roque,grand_roque

    def roque(self, J, type_roque):
        """
        Effectue un roque (petit ou grand) pour le joueur J si possible.

        Paramètres
        ----------
        J : Joueur
            Le joueur qui tente de roquer.
        type_roque : str
            'petit' ou 'grand' pour spécifier le type de roque.

        Retourne
        -------
        bool
            True si le roque a été effectué, False sinon.
        """
        if type_roque == 'petit':
            roi = Rn if J.couleur == 'n' else Rb
            tour = Tn2 if J.couleur == 'n' else Tb2
            direction = 1  # Déplacement vers la droite
        else:  # grand
            roi = Rn if J.couleur == 'n' else Rb
            tour = Tn1 if J.couleur == 'n' else Tb1
            direction = -1  # Déplacement vers la gauche


        i,j=roi.position(self.board)
        k,l = tour.position(self.board)


        # Déplace la tour
        self.board[k][l] = None
        self.board[i][j + direction] = tour

        # Met à jour de a_bouge pour la tour
        self.a_bouge[tour] = True



        # Mise à jour de l'UI pour le move de la tour (celui du roi géré par move_piece)
        from_button_tour = self.findChild(QtWidgets.QPushButton, self.position_to_notation(k,l))
        to_button_tour = self.findChild(QtWidgets.QPushButton, self.position_to_notation(i,j+direction))
        if from_button_tour:
            from_button_tour.setText("")
        if to_button_tour:
            to_button_tour.setText(str(tour))

    def prise_en_passant(self, piece):   #implémenté après le premier move
        if isinstance(piece, Pion) and len(self.moved_pieces)>1:
            last_piece: Piece = self.moved_pieces[-2]
            if isinstance(last_piece, Pion) and last_piece in self.pion_avance_de_2_cases.keys() and self.pion_avance_de_2_cases[last_piece]:
                k, l = last_piece.position(self.board)
                m, n = (k - 1, l) if piece.couleur == self.couleur_utilisateur else (k + 1, l)
                if piece.position(self.board) == (m, n):
                    self.board[k][l] = None
                    button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(k,l))
                    if button:
                        button.setText("")
                    return last_piece,(k,l)
        return None,None

    def promotion(self, piece):
        """

        :type piece: Piece
        """
        row = piece.position(self.board)[0]
        if piece.couleur == self.couleur_utilisateur and row == 0:
            # Boîte de dialogue pour choisir la pièce
            items = ["Dame", "Tour", "Cavalier", "Fou"]
            item, ok = QInputDialog.getItem(self, "Promotion", "Choisissez une pièce:", items, 0, False)
            if ok:
                if item == "Dame":
                    return True, Dame(self.couleur_utilisateur)
                elif item == "Tour":
                    return True, Tour(self.couleur_utilisateur)
                elif item == "Cavalier":
                    return True, Cavalier(self.couleur_utilisateur)
                elif item == "Fou":
                    return True, Fou(self.couleur_utilisateur)
            return True, Dame(self.couleur_utilisateur)
        return False, piece

    def position_to_notation(self, row, col):
        if self.couleur_utilisateur == 'n':
            row, col = 7 - row, 7 - col  # Inverse lignes ET colonnes
        return f"{chr(97 + col)}{8 - row}"

    def notation_move(self,piece, to_row, to_col,promotion=(False,None),piece_prise_en_passant=None,roque=None):
        nota=['','']            # [prise, suffixe]
        adversaire = self.joueur_noir if self.current_player==self.joueur_blanc else self.joueur_blanc
        if self.echec(adversaire):
            nota[1]='+'
        if len(self.pieces_prises)>0 and self.pieces_prises[-1] is not None:
            nota[0]='x'
        if self.echec_et_mat(adversaire):
            nota[1]='#'
        if promotion[0]:
            nota[1] = '='+f'{promotion[1]}'
        if piece_prise_en_passant is not None:
            nota[0] = 'x e.p.'
        if roque=='petit':
            return '0-0'
        if roque=='grand':
            return '0-0-0'
        if not isinstance(piece, Pion):
            return f'{piece}{nota[0]}'+self.position_to_notation(to_row,to_col)+f'{nota[1]}' #notation pour les pions
        else:
            return f'""+{nota[0]}'+self.position_to_notation(to_row,to_col)+f'{nota[1]}'          #notation pour les autres pièces

    def undo_last_move(self):
        if not self.move_history:
            return

        last_move,roque,promotion,piece_prise_en_passant,sa_position = self.move_history.pop()
        start_pos, notation_move = last_move.split('-')


        # Convertit les positions
        start_col, start_row = ord(start_pos[0]) - ord('a'), 8 - int(start_pos[1])
        end_col, end_row = ord(notation_move[0]) - ord('a'), 8 - int(notation_move[1])
        if self.couleur_utilisateur == 'n':
            start_row = 7 - start_row
            end_row = 7 - end_row

        # Récupère les pièces
        piece = self.board[end_row][end_col]
        caught_piece = self.pieces_prises.pop() if self.pieces_prises else None

        # Annule le déplacement en considérant la prise en passant
        if piece_prise_en_passant is not None:
            (pass_row,pass_col)=sa_position
            self.board[pass_row][pass_col] = piece_prise_en_passant
            self.board[end_row][end_col] = None
        else:
            self.board[end_row][end_col] = caught_piece
        self.board[start_row][start_col] = piece


        # Met à jour les listes
        last_piece = self.moved_pieces.pop() if self.moved_pieces else None
        if isinstance(piece,Pion) and self.pion_avance_de_2_cases[piece] and abs(start_row-end_row)==2:
            self.pion_avance_de_2_cases[piece] = False

        # Gestion du roque
        if roque == 'petit':
            # Annule le petit roque

            from_row_tour, from_col_tour = (0, 5) if self.current_player.couleur != self.couleur_utilisateur else (7, 5)
            to_row_tour, to_col_tour = (0, 7) if self.current_player.couleur != self.couleur_utilisateur else (7, 7)


            tour = self.board[from_row_tour][from_col_tour]


            self.board[from_row_tour][from_col_tour] = None
            self.board[to_row_tour][to_col_tour] = tour

            # Retire les deux pièces de moved_pieces
            self.current_player= self.joueur_noir if self.current_player==self.joueur_blanc else self.joueur_blanc


        elif roque == 'grand':
            # Annule le grand roque
            from_row_tour, from_col_tour = (0, 3) if self.current_player.couleur != self.couleur_utilisateur else (7, 3)
            to_row_tour, to_col_tour = (0, 0) if self.current_player.couleur != self.couleur_utilisateur else (7, 0)


            tour = self.board[from_row_tour][from_col_tour]

            self.board[from_row_tour][from_col_tour] = None
            self.board[to_row_tour][to_col_tour] = tour

            # Retire les deux pièces de moved_pieces
            self.moved_pieces.pop()


        # Gestion de la promotion
        if promotion:
            self.board[end_row][end_col] = promotion[1] # Remplace la Dame par le Pion

        # Met à jour l'UI
        from_button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(start_row, start_col))
        to_button = self.findChild(QtWidgets.QPushButton, self.position_to_notation(end_row, end_col))

        if from_button:
            from_button.setText(str(piece))
        if to_button:
            to_button.setText(caught_piece if caught_piece is not None else "")

        # Réinitialise la sélection
        self.selected_piece = None
        self.reset_highlight()

    def echec(self,J):
        R=self.Rn if J.couleur=='n' else self.Rb
        return R.est_menacee(self.board)   #le roi est en échec s'il est directement menacé

    def echec_et_mat(self, J):
        roi = self.Rn if J.couleur == 'n' else self.Rb
        if not self.echec(J):
            return False  # Pas en échec → pas échec et mat
        # Vérifie que le roi n'a aucun coup légal ou qu'aucune autre piece ne peut le protéger
        L=J.pieces_vivantes(self.board)
        for piece in L:
            from_row,from_col = piece.position(self.board)
            for to_row,to_col in piece.cases_accessibles(self.board):
                if self.isvalid_move(from_row,from_col,to_row,to_col):
                    return False
        return True

    def match_nul(self,J):
        if self.echec(J):
            return False
        for piece in J.pieces_vivantes(self.board):
            from_row, from_col = piece.position(self.board)
            for to_row, to_col in piece.cases_accessibles(self.board):
                if self.isvalid_move(from_row, from_col, to_row, to_col):
                    return False
        return True

    # def ia_move(self):
    #     if self.game_over:
    #             return  # Ne fait rien si la partie est terminée
    #     ia=self.joueur_noir if self.couleur_ia=='n' else self.joueur_blanc
    #
    #     try:
    #         resultat = self.alpha_beta(ia, profondeur_courante=1,alpha=-np.inf, beta=np.inf, est_maximisant=False)
    #     except Exception as e:
    #         print(f"Erreur dans alpha_beta: {e}")
    #         QMessageBox.information(self, "Erreur", "L'IA a rencontré une erreur.")
    #         self.game_over = True
    #         return
    #     if resultat[1]!=-np.inf:
    #         coup=resultat[0]
    #         piece,pos_finale=coup[0],coup[1]
    #         from_row,from_col=piece.position(self.board)
    #         to_row,to_col=pos_finale
    #         self.move_piece(from_row,from_col,to_row,to_col)
    #
    #     else:
    #         self.game_over = True  # Désactive les mouvements suivants
    #         winner = "Noirs" if self.current_player.couleur == 'n' else "Blancs"
    #         self.show_end_game_dialog("Abandon",winner)

    def ia_move(self):
        if self.game_over:
            return
        if self.current_player.couleur==self.couleur_utilisateur:
            return
        self.set_enabled_buttons(False)
        self.statusbar.showMessage("L'IA réfléchit...")
        self.ia_thread = IAThread(
            self.board,
            self.couleur_ia,
            self.profondeur_max,
            self.joueur_noir,  # ✅ Passe joueur_noir
            self.joueur_blanc,  # ✅ Passe joueur_blanc
            parent=self
        )
        self.ia_thread.move_found.connect(self.on_ia_move_found)
        self.ia_thread.error_occurred.connect(self.on_ia_error)
        self.ia_thread.start()

    def on_ia_move_found(self, start_row, start_col, end_row, end_col):
        # ✅ Réactive les boutons
        self.set_enabled_buttons(True)

        # ✅ Joue le coup de l'IA
        self.move_piece(start_row, start_col, end_row, end_col)

    def on_ia_error(self, error_message):
        """
        Méthode appelée quand une erreur survient dans le thread IA.
        Affiche un message d'erreur et réactive les boutons de l'interface.

        Args:
            error_message (str): Message d'erreur émis par IAThread.
        """
        # ✅ Réactive les boutons de l'échiquier
        self.set_enabled_buttons(True)

        # ✅ Affiche un message d'erreur dans une boîte de dialogue
        QMessageBox.critical(
            self,
            "Erreur de l'IA",
            f"Une erreur est survenue dans le calcul de l'IA :\n{error_message}"
        )

        # ✅ Met fin à la partie en cas d'erreur critique
        self.game_over = True

    def set_enabled_buttons(self, enabled):
        for row in range(8):
            for col in range(8):
                button_name = self.position_to_notation(row, col)
                button = self.findChild(QtWidgets.QPushButton, button_name)
                if button:
                    button.setEnabled(enabled)


    def alpha_beta(self, J, profondeur_courante=1, alpha=-float('inf'), beta=float('inf'), board=None,est_maximisant=True):
        """
        Implémentation de l'algorithme Alpha-Bêta pour l'IA.
        Gère les promotions et les roques.
        """
        if board is None:
            board = self.board
            board=deepcopy(board)



        if profondeur_courante >= self.profondeur_max:
            return None, self.heuristique(J, board)

        next_J = self.joueur_noir if J == self.joueur_blanc else self.joueur_blanc
        coups = self.coups_possibles(J, board)

        if not coups:
            if self.echec(J):
                return None, -float('inf')
            else:
                return None, 0

        if est_maximisant:
            recompense_retenue = -float('inf')
            coups_meilleurs = []

            for piece, pos, prise_en_passant, promotion, roque in coups:
                if piece is None:  # ✅ Vérifie que piece n'est pas None
                    continue
                new_board = self.resultat_coup(
                    board, piece, pos,
                    prise_en_passant=prise_en_passant,
                    promotion=promotion,
                    roque=roque
                )
                coup, recompense = self.alpha_beta(
                    next_J, profondeur_courante + 1, alpha, beta, new_board, False
                )
                if recompense > recompense_retenue:
                    recompense_retenue = recompense
                    coups_meilleurs = [(piece, pos, prise_en_passant, promotion, roque)]
                elif recompense == recompense_retenue:
                    coups_meilleurs.append((piece, pos, prise_en_passant, promotion, roque))

                if recompense_retenue >= beta:
                    break
                if recompense > alpha:
                    alpha = recompense

            coup_retenu = random.choice(coups_meilleurs)
            return coup_retenu, recompense_retenue

        else:
            recompense_retenue = float('inf')
            coups_meilleurs = []

            for piece, pos, prise_en_passant, promotion, roque in coups:
                new_board = self.resultat_coup(
                    board, piece, pos,
                    prise_en_passant=prise_en_passant,
                    promotion=promotion,
                    roque=roque
                )
                coup, recompense = self.alpha_beta(
                    next_J, profondeur_courante + 1, alpha, beta, new_board, True
                )
                if recompense < recompense_retenue:
                    recompense_retenue = recompense
                    coups_meilleurs = [(piece, pos, prise_en_passant, promotion, roque)]
                elif recompense == recompense_retenue:
                    coups_meilleurs.append((piece, pos, prise_en_passant, promotion, roque))

                if recompense_retenue <= alpha:
                    break
                if recompense < beta:
                    beta = recompense

            coup_retenu = random.choice(coups_meilleurs)
            return coup_retenu, recompense_retenue

    def heuristique(self, J,E=None):
        """
        Renvoie l'heuristique d'une configuration pour un joueur J.
        Basée sur :
        - Valeur des pièces (matériel)
        - Contrôle du centre
        - Mobilité des pièces
        - Pénalités pour les pions mal placés
        :type J: Joueur
        """
        h = 0
        c = J.couleur
        if E is None:
            E=self.board



        # Valeurs des pièces (en centipions)
        valeurs = {
            'Pion': 1,
            'Cavalier': 3,
            'Fou': 3,
            'Tour': 5,
            'Dame': 9,
            'Roi': 0
        }

        # Bonus pour les paires de fous
        nb_fou = 0

        for i, row in enumerate(E):
            for j, piece in enumerate(row):
                if piece is not None:
                    # Valeur matérielle
                    type_piece = piece.__class__.__name__
                    valeur = valeurs.get(type_piece,0)
                    if piece.couleur == c:
                        h += valeur
                    else:
                        h -= valeur

                    # Bonus pour les pièces du joueur J
                    if piece.couleur == c:
                        # Bonus pour le contrôle du centre (cases d4, d5, e4, e5)
                        if (i, j) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                            h += 10  # Bonus modéré pour le centre

                        # Pénalité pour les pièces menacées
                        if piece.est_menacee(E):
                            h -= 10

                        # Bonus pour la mobilité (nombre de coups légaux)
                        h += len(piece.cases_accessibles(E)) * 10  # 10 centipions par coup légal

                        # Spécifique aux pions
                        if isinstance(piece, Pion):
                            # Pénalité pour les pions sur les bords
                            if j in [0, 7]:
                                h -= 20

                            # Bonus pour les pions avancés (proches de la promotion)
                            if c == self.couleur_utilisateur and i == 1:  # Pion blanc en 7ème ligne (index 1)
                                h += 50
                            elif c == self.couleur_ia and i == 6:  # Pion noir en 2ème ligne (index 6)
                                h += 50

                            # Bonus pour les pions connectés (protégés par un autre pion)
                            for di, dj in [(-1, -1), (-1, 1)]:
                                ni, nj = i + di, j + dj
                                if 0 <= ni < 8 and 0 <= nj < 8:
                                    if isinstance(E[ni][nj], Pion) and E[ni][nj].couleur == c:
                                        h += 20

                        # Spécifique aux fous
                        if isinstance(piece, Fou):
                            nb_fou += 1

                        # Bonus pour le roque (roi en sécurité)
                        if self.a_roque[J.couleur]:
                            h += 50

                    # Bonus pour les paires de fous (contrôle de cases de couleurs opposées)
                if nb_fou >= 2:
                    h += 50
                else:
                    pass



        return h

    def coups_possibles(self, J, board=None):
        """
        Renvoie la liste des coups possibles pour le joueur J, y compris :
        - Les coups normaux.
        - Les promotions (Dame, Tour, Cavalier, Fou).
        - Les roques (petit et grand).
        Chaque coup est un tuple (piece, pos_finale, prise_en_passant, promotion, roque).
        """
        if board is None:
            board = self.board
        L = []

        # Ajoute les coups normaux, la prise en passant et les promotions
        for piece in J.pieces_vivantes(board):
            for pos in piece.cases_accessibles(board):
                i, j = piece.position(board)
                to_i, to_j = pos
                if not self.isvalid_move(i,j,to_i, to_j):
                    continue
                prise_en_passant = False
                promotion = None


                if isinstance(piece, Pion):
                    #Vérifie qu'il y a prise en passant
                    if j != to_j and board[to_i][to_j] is None:
                        prise_en_passant = True
                    # Vérifie si c'est une promotion
                    if (piece.couleur == self.couleur_utilisateur and to_i == 0) or (piece.couleur == self.couleur_ia and to_i == 7):
                        for piece_type in ['Dame', 'Tour', 'Cavalier', 'Fou']:
                            L.append((piece, pos, prise_en_passant, piece_type, roque))
                L.append((piece, pos, prise_en_passant, promotion, roque))

        roque = None  # None = pas un roque
        # Ajoute les roques pour le roi du joueur J
        roi = self.Rn if J.couleur == 'n' else self.Rb

        if self.roque_possible(J)[0]=='petit':
            L.append((roi, (roi.position(board)[0], roi.position(board)[1] + 2), False, None, 'petit'))
            # Grand roque
        if self.roque_possible(J)[1]=='grand':
            L.append((roi, (roi.position(board)[0], roi.position(board)[1] - 2), False, None, 'grand'))

        return L

    def resultat_coup(self, board, piece, pos_finale, roque=None, prise_en_passant=False, promotion=None):
        """
        Simule un coup sur une copie de l'échiquier.
        Gère :
        - Les coups normaux.
        - Les promotions.
        - Les roques (petit et grand).
        """

        if board is None or piece is None:
            return None
        E = copy.deepcopy(board)
        if piece not in [p for row in E for p in row if p is not None]:
            k, l = 0, 0  # ✅ Position par défaut
        else:
            k, l = piece.position(E)
        i, j = pos_finale
        if k is None or l is None:
            k, l = 0, 0
        # Gestion de la prise en passant
        if isinstance(piece, Pion) and prise_en_passant:
            E[k][j] = None

        # Gestion du roque
        if roque is not None:
            roi = piece
            if roque == 'petit':
                tour = self.T2n if roi.couleur == 'n' else self.T2b
                # Déplace le roi
                E[i][j] = roi
                E[k][l] = None
                # Déplace la tour
                E[i][j - 1] = tour
                E[i][7] = None  # Tour était en (i, 7) avant le roque
            elif roque == 'grand':
                tour = self.T1n if roi.couleur == 'n' else self.T1b
                # Déplace le roi
                E[i][j] = roi
                E[k][l] = None
                # Déplace la tour
                E[i][j + 1] = tour
                E[i][0] = None  # Tour était en (i, 0) avant le roque
            return E

        # Gestion des coups normaux
        E[i][j] = piece
        E[k][l] = None

        # Gestion de la promotion
        if isinstance(piece, Pion) and promotion is not None:
            piece_class = globals()[promotion]
            E[i][j] = piece_class(piece.couleur)


        return E


    #fin d'une partie


    def show_end_game_dialog(self, result, winner):
        if hasattr(self, 'ia_thread') and self.ia_thread is not None and self.ia_thread.isRunning():
            self.ia_thread.stop()
            self.ia_thread.wait()
            self.set_enabled_buttons(False)
        msg = QMessageBox(self)
        msg.setWindowTitle("Fin de partie")
        msg.setText(f"{result}\nGagnant :{winner}")


        # Sauvegarde dans la base de données
        try:
            moves_str = ", ".join([move[0] for move in self.move_history])
            self.cursor.execute('''
                INSERT INTO parties (date, result, winner, moves)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result, winner, moves_str))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la partie: {e}")
            QMessageBox.warning(self, "Erreur", "La partie n'a pas pu être sauvegardée.")

        # Ajoute le bouton "Nouvelle partie"
        new_game_button = msg.addButton("Nouvelle partie", QMessageBox.ActionRole)
        msg.setStandardButtons(QMessageBox.Ok) # Bouton "OK" classique

        msg.exec_()  # Affiche la boîte de dialogue
        self.game_over = True

        # Si l'utilisateur clique sur "Nouvelle partie"
        if msg.clickedButton() == new_game_button:
            self.reset_game()  # Méthode pour réinitialiser le jeu

    def on_abandon_clicked(self):
        winner = "Noirs" if self.current_player.couleur == 'b' else "Blancs"
        self.show_end_game_dialog("Abandon", winner)

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def reset_game(self):
        self.board = []
        self.setup_board()
        self.move_history = []
        self.pieces_prises = []
        self.moved_pieces = []
        self.pion_avance_de_2_cases = {pion:False for pion in self.Pions_noirs+self.Pions_blancs}
        self.a_bouge = {self.T1n: False, self.Rn: False, self.T2n: False, self.T1b: False, self.Rb: False, self.T2b: False}
        self.current_player = self.joueur_blanc
        self.selected_piece = None

        # Réinitialise l'UI
        self.listWidget.clear()  # Efface l'historique des coups
        self.reset_highlight()  # Réinitialise la surbrillance des cases

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    jeu = ChessGame()
    jeu.show()
    sys.exit(app.exec_())








