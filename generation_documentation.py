import os
import subprocess

# Liste des modules à documenter
modules = ["module_classes", "module_alpha_beta_et_heuristique", "Jeu_et_fonctions","module_tests"]

# Générer un fichier HTML pour chaque module
for module in modules:
    subprocess.run(["python", "-m", "pydoc", "-w", module])

print("Documentation générée avec succès !")