"""
components/zone_centrale.py — Gestionnaire de la zone centrale a etats multiples.

La zone centrale transite entre trois etats distincts :
  1. SPINNER  — animation d'attente (generation du prix ou paiement en cours)
  2. PRIX     — affichage du prix du ticket avec effet de fondu progressif
  3. RESULTAT — affichage du recu de paiement avec effet de fondu progressif

Chaque appel a afficher_*() annule l'animation precedente, detruit les widgets
existants, puis construit le nouvel etat avec son animation de fondu.

La robustesse aux transitions rapides (clic "Reinitialiser" en cours d'animation)
est assuree par un compteur de generation : tout callback de fondu planifie
via after() est invalide des qu'une nouvelle transition commence.
"""

import tkinter as tk
from tkinter import font as tkfont

from components.spinner import Spinner

# Nombre d'etapes et delai (ms) de l'effet de fondu
_ETAPES_FONDU = 18
_DELAI_MS = 28

# Largeur du recu en caracteres monospace
_W = 34


def _interpoler_couleur(debut_hex: str, fin_hex: str, t: float) -> str:
    """
    Interpole lineairement entre deux couleurs hexadecimales.
    t=0.0 donne debut_hex, t=1.0 donne fin_hex.
    """
    def to_rgb(h):
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    r1, g1, b1 = to_rgb(debut_hex)
    r2, g2, b2 = to_rgb(fin_hex)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


class ZoneCentrale(tk.Frame):
    """
    Frame principale gerant les trois etats de la zone centrale.

    Tous les widgets fils sont detruits et reconstruits a chaque transition
    d'etat via les methodes publiques afficher_spinner(), afficher_prix()
    et afficher_resultat().
    """

    def __init__(self, parent, couleurs: dict):
        super().__init__(
            parent,
            bg=couleurs["card"],
            relief="flat",
        )
        self.couleurs = couleurs

        # Compteur incremente a chaque transition pour invalider les vieux callbacks
        self._generation = 0

        # Reference au spinner actif pour pouvoir l'arreter proprement
        self._spinner_actif = None

    # ------------------------------------------------------------------
    # API publique : les trois transitions d'etat
    # ------------------------------------------------------------------

    def afficher_spinner(self):
        """Passe a l'etat SPINNER : affiche l'animation d'attente."""
        self._nettoyer()
        self._etat_spinner()

    def afficher_prix(self, prix: int):
        """Passe a l'etat PRIX : affiche le prix avec fondu progressif."""
        self._nettoyer()
        self._etat_prix(prix)

    def afficher_resultat(self, resultat: dict):
        """Passe a l'etat RESULTAT : affiche le recu avec fondu progressif."""
        self._nettoyer()
        self._etat_resultat(resultat)

    # ------------------------------------------------------------------
    # Etat SPINNER
    # ------------------------------------------------------------------

    def _etat_spinner(self):
        """Construit et anime le spinner circulaire centre dans la zone."""
        bg = self.couleurs["card"]

        # Cadre de centrage (pack avec expand=True centre verticalement et horizontalement)
        conteneur = tk.Frame(self, bg=bg)
        conteneur.pack(expand=True)

        spinner = Spinner(
            conteneur,
            size=90,
            couleur=self.couleurs["primary"],
            epaisseur=9,
            bg=bg,
        )
        spinner.pack()
        spinner.demarrer()
        self._spinner_actif = spinner

        tk.Label(
            conteneur,
            text="Veuillez patienter...",
            font=("Helvetica", 11),
            fg=self.couleurs["muted"],
            bg=bg,
        ).pack(pady=(12, 0))

    # ------------------------------------------------------------------
    # Etat PRIX
    # ------------------------------------------------------------------

    def _etat_prix(self, prix: int):
        """
        Construit l'affichage du prix du ticket et lance le fondu
        de la couleur de fond (invisible) vers les couleurs cibles.
        """
        bg = self.couleurs["card"]
        gen = self._generation  # capture la generation courante pour les lambdas

        conteneur = tk.Frame(self, bg=bg)
        conteneur.pack(expand=True)

        # Sous-titre "Prix du ticket" — fondu vers couleur muted
        lbl_sous_titre = tk.Label(
            conteneur,
            text="Prix du ticket",
            font=("Helvetica", 13),
            fg=bg,  # invisible au depart
            bg=bg,
        )
        lbl_sous_titre.pack(pady=(0, 6))

        # Affichage principal du montant — fondu vers couleur primaire (orange)
        lbl_prix = tk.Label(
            conteneur,
            text=f"{prix:,} FCFA".replace(",", " "),
            font=tkfont.Font(family="Helvetica", size=44, weight="bold"),
            fg=bg,
            bg=bg,
        )
        lbl_prix.pack()

        # Instruction pour l'utilisateur — fondu vers couleur muted
        lbl_hint = tk.Label(
            conteneur,
            text="Entrez le montant paye ci-dessous et cliquez sur  Payer",
            font=("Helvetica", 10),
            fg=bg,
            bg=bg,
        )
        lbl_hint.pack(pady=(14, 0))

        # Lancer le fondu pour les trois labels simultanement
        self._fondu(
            labels_cibles=[
                (lbl_sous_titre, self.couleurs["muted"]),
                (lbl_prix,       self.couleurs["primary"]),
                (lbl_hint,       self.couleurs["muted"]),
            ],
            bg=bg,
            etape=0,
            gen=gen,
        )

    # ------------------------------------------------------------------
    # Etat RESULTAT
    # ------------------------------------------------------------------

    def _etat_resultat(self, resultat: dict):
        """
        Construit le recu de paiement formate et lance le fondu
        vers les couleurs cibles (texte + couleur de statut).
        """
        bg = self.couleurs["card"]
        gen = self._generation

        texte_recu, couleur_statut = self._formater_recu(resultat)
        texte_statut = self._texte_statut(resultat["statut"])

        conteneur = tk.Frame(self, bg=bg)
        conteneur.pack(expand=True)

        # Bloc de texte monospace representant le recu
        lbl_recu = tk.Label(
            conteneur,
            text=texte_recu,
            font=("Courier New", 12),
            fg=bg,  # invisible au depart
            bg=bg,
            justify="left",
        )
        lbl_recu.pack()

        # Ligne de statut (v Transaction reussie / Paiement exact / Erreur)
        lbl_statut = tk.Label(
            conteneur,
            text=texte_statut,
            font=("Helvetica", 13, "bold"),
            fg=bg,
            bg=bg,
        )
        lbl_statut.pack(pady=(8, 0))

        # Fondu des deux labels simultanement vers leurs couleurs respectives
        self._fondu(
            labels_cibles=[
                (lbl_recu,    self.couleurs["text"]),
                (lbl_statut,  couleur_statut),
            ],
            bg=bg,
            etape=0,
            gen=gen,
        )

    # ------------------------------------------------------------------
    # Formatage du recu de paiement
    # ------------------------------------------------------------------

    def _formater_recu(self, r: dict) -> tuple:
        """
        Construit le texte complet du recu selon le statut de la transaction.
        Retourne (texte_str, couleur_du_statut).

        Le texte est en police monospace : les nombres sont alignes a droite
        sur 8 caracteres pour garantir l'alignement vertical.
        """
        sep = "-" * _W

        def header(titre):
            """Titre centre dans la largeur du recu avec des tirets."""
            return f" {titre} ".center(_W, "-")

        def ligne_montant(label, valeur):
            """Ligne 'label : valeur FCFA' alignee sur la largeur du recu."""
            return f"  {label:<16}:  {valeur:>8} FCFA"

        # --- En-tete commun a tous les statuts ---
        lignes = [
            sep,
            header("Recu de paiement"),
            sep,
            ligne_montant("Prix du ticket", r["prix_ticket"]),
            ligne_montant("Montant paye", r["montant_paye"]),
            sep,
        ]

        # --- Statut : paiement exact ---
        if r["statut"] == "exact":
            lignes += [
                "  Paiement exact. Merci !",
                "  Aucune monnaie a rendre.",
                sep,
            ]
            return "\n".join(lignes), self.couleurs["success"]

        # --- Statut : erreur de calcul ---
        if r["statut"] == "erreur":
            lignes += [
                "  Montant impossible a rendre",
                "  avec les coupures disponibles.",
                sep,
            ]
            return "\n".join(lignes), self.couleurs["error"]

        # --- Statut : success (rendu de monnaie normal) ---
        lignes += [
            header("Rendu de monnaie"),
            sep,
            ligne_montant("Montant rendu", r["montant_rendu"]),
            f"  {'Nb de coupures':<16}:  {r['nombre_coupures']:>8}",
            sep,
        ]

        # Detail des coupures utilisees
        for qte, val in r["detail_coupures"]:
            lignes.append(f"         {qte:>5}  x  {val:>6}  FCFA")

        lignes.append(sep)
        return "\n".join(lignes), self.couleurs["success"]

    def _texte_statut(self, statut: str) -> str:
        """Retourne la ligne de statut associee au resultat de la transaction."""
        if statut == "exact":
            return "  Paiement exact — Aucune monnaie a rendre."
        if statut == "success":
            return "  Transaction reussie"
        return "  Erreur de traitement"

    # ------------------------------------------------------------------
    # Animation de fondu par interpolation de couleur
    # ------------------------------------------------------------------

    def _fondu(self, labels_cibles: list, bg: str, etape: int, gen: int):
        """
        Interpole recursivement la couleur de texte de chaque label
        du fond (invisible) vers sa couleur cible respective.

        labels_cibles : liste de (widget_label, couleur_cible_hex)
        bg            : couleur de depart (fond = texte invisible)
        etape         : etape courante (0 -> _ETAPES_FONDU)
        gen           : generation au moment du lancement (invalide si differente)
        """
        # Transition obsolete : une nouvelle transition a commence
        if gen != self._generation:
            return

        if etape > _ETAPES_FONDU:
            return

        t = etape / _ETAPES_FONDU  # progression entre 0.0 et 1.0

        for lbl, cible in labels_cibles:
            try:
                lbl.config(fg=_interpoler_couleur(bg, cible, t))
            except tk.TclError:
                # Le widget a ete detruit avant la fin du fondu
                return

        # Planifier la prochaine etape
        self.after(
            _DELAI_MS,
            lambda: self._fondu(labels_cibles, bg, etape + 1, gen),
        )

    # ------------------------------------------------------------------
    # Nettoyage lors d'une transition d'etat
    # ------------------------------------------------------------------

    def _nettoyer(self):
        """
        Invalide toutes les animations en cours (fondu et spinner)
        et detruit tous les widgets fils de cette zone.
        Doit etre appele avant chaque construction d'un nouvel etat.
        """
        # Incrementer la generation invalide tous les callbacks _fondu en attente
        self._generation += 1

        # Arreter le spinner proprement avant de detruire son canvas
        if self._spinner_actif is not None:
            try:
                self._spinner_actif.arreter()
            except Exception:
                pass
            self._spinner_actif = None

        # Detruire tous les widgets fils de cette zone
        for widget in self.winfo_children():
            try:
                widget.destroy()
            except Exception:
                pass
