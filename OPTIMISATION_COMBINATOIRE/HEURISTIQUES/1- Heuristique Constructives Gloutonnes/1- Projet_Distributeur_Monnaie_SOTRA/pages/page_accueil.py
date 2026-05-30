"""
pages/page_accueil.py — Page principale de l'application SOTRA.

Organise l'interface en grille 5 lignes :
  - Ligne 0      : bandeau titre
  - Lignes 1-2-3 : zone centrale fusionnee (spinner / prix / recu)
  - Ligne 4      : barre d'action (saisie + Payer + Reinitialiser)

Orchestre le flux complet :
  1. Generation animee du prix au demarrage
  2. Validation de la saisie utilisateur via validation.py
  3. Appel du callback traiter_paiement() dans un thread separe
  4. Affichage du recu via la ZoneCentrale
"""

import threading
import tkinter as tk
from tkinter import font as tkfont

from components.zone_centrale import ZoneCentrale
from components.generateur_prix import generer_prix


class PageAccueil(tk.Frame):
    """
    Page principale : coordonne tous les composants et gere les interactions
    utilisateur (validation, paiement, reinitialisation).
    """

    def __init__(self, parent, callback, couleurs: dict):
        super().__init__(parent, bg=couleurs["bg"])

        self.callback = callback
        self.couleurs = couleurs
        self.prix_ticket = None  # Prix courant genere et affiche

        # Construction de l'interface
        self._configurer_grille()
        self._construire_titre()            # Ligne 0
        self._construire_zone_centrale()    # Lignes 1-3
        self._construire_barre_action()     # Ligne 4

        # Demarrer la generation du prix apres un court delai (laisse le temps
        # au gestionnaire de geometrie de calculer les tailles des widgets)
        self.after(300, self._lancer_generation_prix)

    # ------------------------------------------------------------------
    # Configuration de la grille
    # ------------------------------------------------------------------

    def _configurer_grille(self):
        """Poids des lignes/colonnes pour que la zone centrale se dilate."""
        self.rowconfigure(0, weight=0)   # Titre : hauteur fixe
        self.rowconfigure(1, weight=1)   # \
        self.rowconfigure(2, weight=1)   #  >  Zone centrale : extensible
        self.rowconfigure(3, weight=1)   # /
        self.rowconfigure(4, weight=0)   # Barre action : hauteur fixe
        self.columnconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Ligne 0 — Bandeau titre
    # ------------------------------------------------------------------

    def _construire_titre(self):
        """Cree le bandeau de titre orange en haut de la fenetre."""
        bandeau = tk.Frame(self, bg=self.couleurs["primary"], pady=14)
        bandeau.grid(row=0, column=0, sticky="ew")

        tk.Label(
            bandeau,
            text="Distributeur de Tickets de Bus",
            font=tkfont.Font(family="Helvetica", size=20, weight="bold"),
            fg="#ffffff",
            bg=self.couleurs["primary"],
        ).pack()

        tk.Label(
            bandeau,
            text="Societe des Transports Abidjanais  —  SOTRA",
            font=("Helvetica", 10),
            fg="#fff3e0",
            bg=self.couleurs["primary"],
        ).pack()

    # ------------------------------------------------------------------
    # Lignes 1-3 — Zone centrale fusionnee
    # ------------------------------------------------------------------

    def _construire_zone_centrale(self):
        """Instancie la ZoneCentrale qui gere les etats prix / spinner / recu."""
        self.zone = ZoneCentrale(self, couleurs=self.couleurs)
        self.zone.grid(
            row=1, column=0,
            rowspan=3,
            sticky="nsew",
            padx=40, pady=10,
        )

    # ------------------------------------------------------------------
    # Ligne 4 — Barre d'action
    # ------------------------------------------------------------------

    def _construire_barre_action(self):
        """
        Cree la barre inferieure avec :
          - un champ de saisie pour le montant en FCFA
          - le bouton "Payer"
          - le bouton "Reinitialiser"
          - un label d'erreur affiche en cas de saisie invalide
        """
        barre = tk.Frame(self, bg=self.couleurs["card"], pady=14)
        barre.grid(row=4, column=0, sticky="ew", padx=40, pady=(0, 24))

        # --- Cadre saisie (label + entry) ---
        cadre_saisie = tk.Frame(barre, bg=self.couleurs["card"])
        cadre_saisie.pack(side="left", padx=(12, 0))

        tk.Label(
            cadre_saisie,
            text="Montant paye (FCFA) :",
            font=("Helvetica", 11),
            fg=self.couleurs["text"],
            bg=self.couleurs["card"],
        ).pack(side="left", padx=(0, 8))

        # Champ de saisie numerique
        self.champ_montant = tk.Entry(
            cadre_saisie,
            font=("Helvetica", 14, "bold"),
            width=10,
            bg="#21262d",
            fg=self.couleurs["text"],
            insertbackground=self.couleurs["text"],
            relief="flat",
            bd=5,
        )
        self.champ_montant.pack(side="left")

        # Valider avec la touche Entree
        self.champ_montant.bind("<Return>", lambda _e: self._on_payer())

        # --- Bouton Payer ---
        self.btn_payer = tk.Button(
            barre,
            text="   Payer   ",
            font=("Helvetica", 12, "bold"),
            bg=self.couleurs["primary"],
            fg="#ffffff",
            activebackground="#d07600",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=7,
            command=self._on_payer,
        )
        self.btn_payer.pack(side="left", padx=(14, 8))

        # --- Bouton Reinitialiser ---
        self.btn_reset = tk.Button(
            barre,
            text="   Reinitialiser   ",
            font=("Helvetica", 12),
            bg=self.couleurs["border"],
            fg=self.couleurs["text"],
            activebackground="#484f58",
            activeforeground=self.couleurs["text"],
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=7,
            command=self._on_reinitialiser,
        )
        self.btn_reset.pack(side="left")

        # --- Label d'erreur (affiche sous les controles si saisie invalide) ---
        self.label_erreur = tk.Label(
            self,
            text="",
            font=("Helvetica", 10),
            fg=self.couleurs["error"],
            bg=self.couleurs["bg"],
        )
        self.label_erreur.grid(row=4, column=0, sticky="sw", padx=52, pady=(0, 6))

    # ------------------------------------------------------------------
    # Generation du prix
    # ------------------------------------------------------------------

    def _lancer_generation_prix(self):
        """
        Lance le cycle d'animation de generation de prix :
          1. Affiche le spinner pendant 2 secondes
          2. Genere un nouveau prix et l'affiche avec fondu
        """
        self.zone.afficher_spinner()
        self.after(2000, self._afficher_prix_genere)

    def _afficher_prix_genere(self):
        """Genere un nouveau prix aleatoire et demande a la zone de l'afficher."""
        self.prix_ticket = generer_prix()
        self.zone.afficher_prix(self.prix_ticket)

    # ------------------------------------------------------------------
    # Bouton Payer
    # ------------------------------------------------------------------

    def _on_payer(self):
        """
        Gestionnaire du bouton "Payer" :
          1. Valide la saisie via validation.valider_entree()
          2. Si erreur : affiche le message et s'arrete
          3. Si valide : lance le traitement dans un thread separe
        """
        from validation import valider_entree
        COUPURES = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5]

        montant_str = self.champ_montant.get()

        # Validation de la saisie — retourne None si valide, un message sinon
        erreur = valider_entree(montant_str, self.prix_ticket, COUPURES)
        if erreur:
            self.label_erreur.config(text=f"  {erreur}")
            return

        # Saisie valide : effacer le message d'erreur et demarrer le traitement
        self.label_erreur.config(text="")
        montant_paye = int(montant_str.strip())

        # Afficher le spinner et bloquer les controles pendant le traitement
        self.zone.afficher_spinner()
        self._bloquer_controles(True)

        # Lancer le callback metier dans un thread daemon pour ne pas geler l'UI
        threading.Thread(
            target=self._executer_paiement,
            args=(self.prix_ticket, montant_paye),
            daemon=True,
        ).start()

    def _executer_paiement(self, prix_ticket: int, montant_paye: int):
        """
        Execute le callback traiter_paiement() dans le thread worker.
        Renvoie le resultat dans le thread principal via after(0, ...).
        """
        resultat = self.callback(prix_ticket, montant_paye)
        # Toujours modifier Tkinter depuis le thread principal
        self.after(0, lambda: self._on_resultat_recu(resultat))

    def _on_resultat_recu(self, resultat: dict):
        """
        Appele dans le thread principal apres reception du resultat.
        Reactive les controles et affiche le recu dans la zone centrale.
        """
        self._bloquer_controles(False)
        self.zone.afficher_resultat(resultat)

    def _bloquer_controles(self, bloquer: bool):
        """Active ou desactive les boutons et le champ de saisie pendant le traitement."""
        etat = "disabled" if bloquer else "normal"
        self.btn_payer.config(state=etat)
        self.btn_reset.config(state=etat)
        self.champ_montant.config(state=etat)

    # ------------------------------------------------------------------
    # Bouton Reinitialiser
    # ------------------------------------------------------------------

    def _on_reinitialiser(self):
        """
        Reinitialise l'interface :
          - Vide le champ de saisie et le message d'erreur
          - Relance la generation animee d'un nouveau prix
        """
        self.champ_montant.delete(0, tk.END)
        self.label_erreur.config(text="")
        self._lancer_generation_prix()
