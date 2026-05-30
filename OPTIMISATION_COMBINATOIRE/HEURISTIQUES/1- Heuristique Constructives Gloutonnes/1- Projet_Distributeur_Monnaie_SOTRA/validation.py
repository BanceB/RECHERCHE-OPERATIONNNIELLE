"""
validation.py — Module de validation des entrees utilisateur.

Fournit des fonctions pures (sans input() ni print()) permettant
a l'interface graphique de valider les donnees avant traitement.
Les messages d'erreur retournes sont directement affichables dans l'UI.
"""


def valider_entree(montant_str, prix_ticket, coupures):
    """
    Valide le montant saisi par l'utilisateur (fourni sous forme de chaine).

    Effectue trois controles dans l'ordre :
      1. Champ vide ou non numerique
      2. Montant inferieur au prix du ticket
      3. Montant non multiple de la plus petite coupure

    Retourne None si la saisie est valide, sinon retourne un message
    d'erreur lisible directement affichable dans l'interface.
    """
    # Controle 1 : champ vide
    if not montant_str or not montant_str.strip():
        return "Veuillez entrer un montant"

    # Controle 2 : doit etre un entier
    try:
        montant = int(montant_str.strip())
    except ValueError:
        return "Veuillez entrer un nombre entier valide"

    # Controle 3 : montant suffisant
    if montant < prix_ticket:
        manque = prix_ticket - montant
        return f"Montant insuffisant. Il vous manque : {manque} FCFA"

    # Controle 4 : multiple de la plus petite coupure disponible
    plus_petite_coupure = min(coupures)
    if montant % plus_petite_coupure != 0:
        return f"Le montant doit etre un multiple de {plus_petite_coupure} FCFA"

    # Aucune erreur : saisie valide
    return None


def verifier_rendu(montant_rendu, coupures, resultat):
    """
    Verifie que le resultat de l'algorithme glouton correspond au montant attendu.

    Somme tous les billets/pieces du resultat et compare au montant_rendu.
    Retourne True si coherent, False sinon.
    """
    check = sum(resultat[i] * coupures[i] for i in range(len(coupures)))
    return check == montant_rendu
