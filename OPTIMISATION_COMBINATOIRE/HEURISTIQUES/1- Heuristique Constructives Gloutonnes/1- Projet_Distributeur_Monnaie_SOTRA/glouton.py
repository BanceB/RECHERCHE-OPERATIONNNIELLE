"""
glouton.py — Module coeur de l'algorithme glouton de rendu de monnaie.

Fournit l'algorithme de rendu (rendu_monnaie) et la fonction de formatage
du resultat (afficher_rendu) qui retourne un dictionnaire structure
directement exploitable par l'interface graphique.
"""


def rendu_monnaie(montant, coupures):
    """
    Applique l'algorithme glouton pour rendre `montant` en FCFA.

    Parcourt les coupures de la plus grande a la plus petite et prend
    autant de billets/pieces que possible a chaque etape.

    Retourne une liste X ou X[i] = nombre de coupures[i] utilisees,
    ou None si le montant ne peut pas etre rendu exactement.
    """
    reste = montant
    X = [0] * len(coupures)

    for i in range(len(coupures)):
        # Nombre de fois que la coupure courante entre dans le reste
        X[i] = reste // coupures[i]
        reste = reste - X[i] * coupures[i]
        if reste == 0:
            break

    if reste != 0:
        return None
    return X


def afficher_rendu(X, coupures):
    """
    Construit et retourne un dictionnaire structure decrivant le rendu de monnaie.

    Ne fait aucun print() : les donnees sont exploitables par l'interface graphique.

    Retourne :
        {
            "montant_rendu"   : int,            total rendu en FCFA
            "nombre_coupures" : int,            nombre total de pieces/billets
            "detail_coupures" : [(qte, valeur)] liste des (quantite, valeur) utilisees
        }
    """
    # Calcul du total rendu et du nombre de pieces/billets utilises
    montant_rendu = sum(X[i] * coupures[i] for i in range(len(coupures)))
    nombre_coupures = sum(X)

    # On ne garde que les coupures effectivement utilisees (quantite > 0)
    detail_coupures = [
        (X[i], coupures[i])
        for i in range(len(coupures))
        if X[i] > 0
    ]

    return {
        "montant_rendu": montant_rendu,
        "nombre_coupures": nombre_coupures,
        "detail_coupures": detail_coupures,
    }
