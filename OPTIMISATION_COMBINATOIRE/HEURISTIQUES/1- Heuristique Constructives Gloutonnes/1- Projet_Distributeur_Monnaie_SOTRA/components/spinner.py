"""
components/spinner.py — Widget spinner circulaire reutilisable.

Dessine un arc colore tournant en boucle sur un Canvas Tkinter pour
signaler un traitement en cours. Peut etre demarre et arrete dynamiquement.

Utilisation typique :
    sp = Spinner(parent, size=80, couleur="#f08c00")
    sp.pack()
    sp.demarrer()
    ...
    sp.arreter()
"""

import tkinter as tk


class Spinner(tk.Canvas):
    """
    Widget spinner : arc colore anime sur un Canvas.

    Parametres :
        size      — cote du canvas carre en pixels (defaut : 80)
        couleur   — couleur de l'arc anime (defaut : orange SOTRA)
        epaisseur — epaisseur du trait en pixels (defaut : 8)
        bg        — couleur de fond du canvas
    """

    def __init__(self, parent, size=80, couleur="#f08c00", epaisseur=8,
                 bg="#161b22", **kwargs):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=bg,
            highlightthickness=0,
            **kwargs,
        )
        self._size = size
        self._couleur = couleur
        self._epaisseur = epaisseur
        self._angle = 0        # angle de depart de l'arc en degres
        self._actif = False    # True quand l'animation tourne
        self._apres_id = None  # identifiant du callback after() en cours

        # Dessin initial
        self._dessiner_arc()

    def _dessiner_arc(self):
        """Efface le canvas et redessine l'arc a la position angulaire courante."""
        self.delete("all")
        marge = self._epaisseur + 3

        # Cercle de fond grise pour materialiser le chemin de rotation
        self.create_arc(
            marge, marge,
            self._size - marge, self._size - marge,
            start=0, extent=359,
            outline="#30363d",
            width=self._epaisseur,
            style="arc",
        )

        # Arc colore de 90 degres representant la progression
        self.create_arc(
            marge, marge,
            self._size - marge, self._size - marge,
            start=self._angle,
            extent=90,
            outline=self._couleur,
            width=self._epaisseur,
            style="arc",
        )

    def _animer(self):
        """
        Avance l'arc de 12 degres et reprogramme l'animation si le spinner est actif.
        Capture les TclError pour stopper proprement si le widget est detruit.
        """
        if not self._actif:
            return
        self._angle = (self._angle + 12) % 360
        try:
            self._dessiner_arc()
        except tk.TclError:
            # Le widget a ete detruit avant la fin de l'animation
            self._actif = False
            return
        # Planifier la prochaine frame (~33 fps)
        self._apres_id = self.after(30, self._animer)

    def demarrer(self):
        """Demarre la rotation du spinner (sans effet si deja actif)."""
        if self._actif:
            return
        self._actif = True
        self._animer()

    def arreter(self):
        """Arrete la rotation et annule le callback after() en attente."""
        self._actif = False
        if self._apres_id is not None:
            try:
                self.after_cancel(self._apres_id)
            except Exception:
                pass
            self._apres_id = None
