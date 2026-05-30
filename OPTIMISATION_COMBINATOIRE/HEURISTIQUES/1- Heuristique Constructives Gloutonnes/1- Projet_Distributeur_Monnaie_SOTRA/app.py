"""
app.py — Fenetre principale Tkinter de l'application SOTRA.

Initialise la fenetre racine, configure les dimensions et la palette
de couleurs globale, puis charge la page d'accueil. Le callback de
traitement est injecte depuis main.py (inversion de dependance).
"""

import tkinter as tk
from pages.page_accueil import PageAccueil


# Palette de couleurs partagee par tous les composants
COULEURS = {
    "bg":       "#0d1117",   # fond general (noir profond)
    "card":     "#161b22",   # fond des panneaux (gris tres fonce)
    "primary":  "#f08c00",   # orange SOTRA (accent principal)
    "text":     "#e6edf3",   # texte principal (blanc casse)
    "muted":    "#8b949e",   # texte secondaire (gris clair)
    "success":  "#3fb950",   # vert succes
    "error":    "#f85149",   # rouge erreur
    "border":   "#30363d",   # bordures et separateurs
}


class App(tk.Tk):
    """
    Fenetre principale de l'application.

    Reçoit le callback `traiter_paiement` de main.py et le transmet
    a la PageAccueil. La palette COULEURS est propagee a tous les composants
    pour garantir la coherence visuelle.
    """

    def __init__(self, callback):
        super().__init__()

        self.callback = callback

        # --- Configuration de la fenetre ---
        self.title("Distributeur de Tickets — SOTRA")
        self.geometry("820x560")
        self.resizable(False, False)
        self.configure(bg=COULEURS["bg"])

        # Centrer la fenetre sur l'ecran au lancement
        self._centrer_fenetre(820, 560)

        # --- Chargement de la page principale ---
        self.page = PageAccueil(self, callback=callback, couleurs=COULEURS)
        self.page.pack(fill="both", expand=True)

    def _centrer_fenetre(self, largeur: int, hauteur: int):
        """Positionne la fenetre au centre de l'ecran."""
        self.update_idletasks()
        x = (self.winfo_screenwidth()  // 2) - (largeur  // 2)
        y = (self.winfo_screenheight() // 2) - (hauteur // 2)
        self.geometry(f"{largeur}x{hauteur}+{x}+{y}")
