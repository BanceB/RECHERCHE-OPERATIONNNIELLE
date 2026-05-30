"""
main.py — Point d'entree de l'application et callback de traitement metier.

Expose traiter_paiement(), fonction pure sans effets de bord qui orchestre
le calcul glouton du rendu de monnaie et retourne un dictionnaire de resultats
structure utilisable par l'interface graphique.

Lorsque ce fichier est execute directement, il instancie la fenetre Tkinter
en lui injectant le callback de traitement.
"""

from calculs import calcul_monnaie
from glouton import rendu_monnaie, afficher_rendu
from validation import verifier_rendu

# Coupures FCFA disponibles, triees par ordre decroissant (obligatoire pour le glouton)
COUPURES = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5]


def traiter_paiement(prix_ticket: int, montant_paye: int) -> dict:
    """
    Callback principal appele par l'interface apres validation de la saisie.

    Calcule le rendu de monnaie via l'algorithme glouton et retourne
    un dictionnaire normalise avec tous les details de la transaction.

    Retourne un dict avec les cles :
        - prix_ticket     : prix du ticket affiche
        - montant_paye    : montant entre par l'utilisateur
        - montant_rendu   : difference a rendre en FCFA
        - nombre_coupures : nombre total de pieces/billets rendus
        - detail_coupures : liste de tuples [(quantite, valeur), ...]
        - statut          : "exact" | "success" | "erreur"
    """
    # Calcul de la monnaie a rendre
    montant_rendu = calcul_monnaie(montant_paye, prix_ticket)

    # Cas paiement exact : aucune monnaie a rendre
    if montant_rendu == 0:
        return {
            "prix_ticket": prix_ticket,
            "montant_paye": montant_paye,
            "montant_rendu": 0,
            "nombre_coupures": 0,
            "detail_coupures": [],
            "statut": "exact",
        }

    # Algorithme glouton pour decomposer le montant en coupures
    resultat_brut = rendu_monnaie(montant_rendu, COUPURES)

    # Cas ou l'algorithme echoue (montant non decomposable avec ces coupures)
    if resultat_brut is None or not verifier_rendu(montant_rendu, COUPURES, resultat_brut):
        return {
            "prix_ticket": prix_ticket,
            "montant_paye": montant_paye,
            "montant_rendu": montant_rendu,
            "nombre_coupures": 0,
            "detail_coupures": [],
            "statut": "erreur",
        }

    # Formatage du resultat glouton en dictionnaire structure
    rendu = afficher_rendu(resultat_brut, COUPURES)

    return {
        "prix_ticket": prix_ticket,
        "montant_paye": montant_paye,
        "montant_rendu": rendu["montant_rendu"],
        "nombre_coupures": rendu["nombre_coupures"],
        "detail_coupures": rendu["detail_coupures"],
        "statut": "success",
    }


if __name__ == "__main__":
    # Injection du callback dans l'interface graphique au lancement
    from app import App
    app = App(callback=traiter_paiement)
    app.mainloop()
