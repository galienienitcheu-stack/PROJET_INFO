# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\toumiab\OneDrive\python_workspace\IHM2018\interface.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_principale_ihm(object):
    def setupUi(self, principale_ihm):
        principale_ihm.setObjectName("principale_ihm")
        principale_ihm.resize(855, 535)
        icon = QtGui.QIcon.fromTheme("help")
        principale_ihm.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(principale_ihm)
        self.centralwidget.setObjectName("centralwidget")
        self.conteneur = QtWidgets.QWidget(self.centralwidget)
        self.conteneur.setGeometry(QtCore.QRect(10, 10, 831, 431))
        self.conteneur.setObjectName("conteneur")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 450, 831, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bouton_gen = QtWidgets.QPushButton(self.widget)
        self.bouton_gen.setObjectName("bouton_gen")
        self.horizontalLayout.addWidget(self.bouton_gen)
        self.bouton_pas = QtWidgets.QPushButton(self.widget)
        self.bouton_pas.setObjectName("bouton_pas")
        self.horizontalLayout.addWidget(self.bouton_pas)
        self.bouton_sim = QtWidgets.QPushButton(self.widget)
        self.bouton_sim.setObjectName("bouton_sim")
        self.horizontalLayout.addWidget(self.bouton_sim)
        spacerItem = QtWidgets.QSpacerItem(298, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bouton_qui = QtWidgets.QPushButton(self.widget)
        self.bouton_qui.setObjectName("bouton_qui")
        self.horizontalLayout.addWidget(self.bouton_qui)
        principale_ihm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(principale_ihm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 855, 26))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        principale_ihm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(principale_ihm)
        self.statusbar.setObjectName("statusbar")
        principale_ihm.setStatusBar(self.statusbar)
        self.actionQuitter = QtWidgets.QAction(principale_ihm)
        self.actionQuitter.setObjectName("actionQuitter")
        self.menuFiles.addAction(self.actionQuitter)
        self.menubar.addAction(self.menuFiles.menuAction())

        self.retranslateUi(principale_ihm)
        self.bouton_qui.clicked.connect(principale_ihm.close)
        QtCore.QMetaObject.connectSlotsByName(principale_ihm)

    def retranslateUi(self, principale_ihm):
        _translate = QtCore.QCoreApplication.translate
        principale_ihm.setWindowTitle(_translate("principale_ihm", "Ecosysteme"))
        self.bouton_gen.setText(_translate("principale_ihm", "Générer"))
        self.bouton_pas.setText(_translate("principale_ihm", "Un pas"))
        self.bouton_sim.setText(_translate("principale_ihm", "Simuler"))
        self.bouton_qui.setText(_translate("principale_ihm", "Quitter"))
        self.menuFiles.setTitle(_translate("principale_ihm", "Files"))
        self.actionQuitter.setText(_translate("principale_ihm", "Quitter"))
        self.actionQuitter.setShortcut(_translate("principale_ihm", "Ctrl+Q"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    principale_ihm = QtWidgets.QMainWindow()
    ui = Ui_principale_ihm()
    ui.setupUi(principale_ihm)
    principale_ihm.show()
    sys.exit(app.exec_())

