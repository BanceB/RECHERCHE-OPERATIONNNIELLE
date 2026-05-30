# 🏧 Projet : Distributeur Automatique de Monnaie

## Optimisation Combinatoire — Implémentation de l'Heuristique Gloutonne

---

## 📖 Contexte Réel : Le Distributeur de Tickets de Bus

La **SOTRA** (Société des Transports Abidjanais) installe de nouveaux **distributeurs automatiques de tickets** aux arrêts de bus. Chaque distributeur :

- Affiche le prix du ticket
- Accepte les pièces et billets FCFA
- **Doit rendre la monnaie automatiquement** avec le minimum de pièces/billets

Tu es l'**ingénieur logiciel** recruté pour programmer le module de rendu de monnaie embarqué dans chaque distributeur.

---

## 🎯 Cahier des Charges

### Fonctionnalités attendues

Le programme doit :

1. Recevoir le **prix du ticket** et le **montant payé** par le client
2. Calculer le **montant à rendre**
3. Appliquer l'**algorithme glouton** pour déterminer les coupures optimales
4. Afficher le **détail du rendu** (quelles coupures, combien de chaque)
5. Gérer les **cas d'erreur** (montant insuffisant, montant exact, etc.)

### Système monétaire

```
Coupures disponibles (FCFA) :
D = {10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5}
```

### Scénarios de test obligatoires

| Scénario | Prix ticket | Montant payé | Monnaie attendue |
|----------|------------|-------------|-----------------|
| Client 1 | 450 FCFA | 1 000 FCFA | 550 FCFA |
| Client 2 | 350 FCFA | 500 FCFA | 150 FCFA |
| Client 3 | 1 250 FCFA | 5 000 FCFA | 3 750 FCFA |
| Client 4 | 675 FCFA | 10 000 FCFA | 9 325 FCFA |
| Client 5 | 2 800 FCFA | 2 800 FCFA | 0 FCFA (exact) |
| Client 6 | 500 FCFA | 200 FCFA | ERREUR (insuffisant) |
| Client 7 | 15 480 FCFA | 20 000 FCFA | 4 520 FCFA |

---

## 🛠️ Démarche Professionnelle de Résolution

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

Avant de coder, formaliser le problème :

#### Étape 1.1 : Définir les données

```
Entrées :
  - P = prix du ticket
  - V = montant versé par le client
  - D = {d₁, d₂, ..., dₖ} = ensemble des coupures triées par ordre décroissant

Sortie :
  - X = {x₁, x₂, ..., xₖ} où xᵢ = nombre de coupures dᵢ utilisées
```

#### Étape 1.2 : Calculer le montant à rendre

```
M = V - P

Si M < 0 → ERREUR : montant insuffisant
Si M = 0 → Pas de monnaie à rendre
Si M > 0 → Appliquer l'algorithme glouton
```

#### Étape 1.3 : Écrire le modèle mathématique

```
         k
Min Z =  Σ  xᵢ                    (minimiser le nombre total de coupures)
        i=1

s.c. :
  k
  Σ  dᵢ · xᵢ  =  M               (rendre exactement M)
 i=1

  xᵢ ∈ ℕ  (entier ≥ 0)            ∀ i = 1, ..., k
```

#### Étape 1.4 : Résoudre un exemple à la main

```
Exemple : M = 3 750 FCFA
Coupures : {10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5}

Étape 1 : 10000 > 3750 → x₁ = 0, reste = 3750
Étape 2 : 5000 > 3750  → x₂ = 0, reste = 3750
Étape 3 : 2000 ≤ 3750  → x₃ = ⌊3750/2000⌋ = 1, reste = 3750 - 2000 = 1750
Étape 4 : 1000 ≤ 1750  → x₄ = ⌊1750/1000⌋ = 1, reste = 1750 - 1000 = 750
Étape 5 : 500 ≤ 750    → x₅ = ⌊750/500⌋ = 1,   reste = 750 - 500 = 250
Étape 6 : 200 ≤ 250    → x₆ = ⌊250/200⌋ = 1,   reste = 250 - 200 = 50
Étape 7 : 100 > 50     → x₇ = 0, reste = 50
Étape 8 : 50 ≤ 50      → x₈ = ⌊50/50⌋ = 1,     reste = 50 - 50 = 0 → STOP

Solution : 1×2000 + 1×1000 + 1×500 + 1×200 + 1×50 = 3750 ✅
Nombre de coupures : 5
```

> ✅ Ne passe à la Phase 2 que si tu obtiens les bons résultats à la main.

---

### PHASE 2 — Conception de l'Algorithme (pseudo-code)

Avant de choisir un langage, écrire le pseudo-code structuré :

#### Étape 2.1 : Pseudo-code de l'algorithme glouton

```
ALGORITHME RenduMonnaieGlouton

ENTRÉES :
    M        : entier    (montant à rendre)
    D[1..k]  : tableau   (coupures triées décroissant)

SORTIE :
    X[1..k]  : tableau   (nombre de chaque coupure)
    Z        : entier    (nombre total de coupures)

DÉBUT
    reste ← M
    Z ← 0

    POUR i DE 1 À k FAIRE
        X[i] ← reste DIV D[i]         // division entière
        reste ← reste - X[i] × D[i]   // mise à jour du reste
        Z ← Z + X[i]                  // compteur total

        SI reste = 0 ALORS
            SORTIR DE LA BOUCLE        // terminé
        FIN SI
    FIN POUR

    SI reste ≠ 0 ALORS
        AFFICHER "Impossible de rendre exactement"
    SINON
        AFFICHER solution X et total Z
    FIN SI
FIN
```

#### Étape 2.2 : Pseudo-code du programme principal

```
ALGORITHME ProgrammePrincipal

DÉBUT
    D ← [10000, 5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5]

    LIRE prix_ticket
    LIRE montant_paye

    M ← montant_paye - prix_ticket

    SI M < 0 ALORS
        AFFICHER "ERREUR : montant insuffisant"
        AFFICHER "Il manque", |M|, "FCFA"
    SINON SI M = 0 ALORS
        AFFICHER "Montant exact, pas de monnaie à rendre"
    SINON
        resultat ← RenduMonnaieGlouton(M, D)
        AFFICHER resultat
    FIN SI
FIN
```

#### Étape 2.3 : Identifier les structures de données

```
Structures nécessaires :
  - Tableau/Liste pour les coupures D
  - Tableau/Liste pour les quantités X (même taille que D)
  - Variables simples : M (montant), reste, Z (total coupures)

Complexité attendue :
  - Temps  : O(k) où k = nombre de coupures → très rapide
  - Espace : O(k) pour stocker les résultats
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du code

```
Organiser le code en fonctions/modules séparés :

projet/
├── main.py                (ou main.c, Main.java)
│
├── glouton.py             Module cœur
│   ├── rendu_monnaie()    Algorithme glouton
│   └── afficher_rendu()   Affichage formaté
│
├── validation.py          Module validation
│   ├── valider_entree()   Vérification des entrées
│   └── verifier_rendu()   Test de cohérence du résultat
│
└── tests.py               Tests unitaires
    ├── test_cas_normaux()
    ├── test_cas_limites()
    └── test_erreurs()
```

#### Étape 3.2 : Règles de codage

```
1. NOMMER clairement les variables
     ✅ montant_a_rendre, coupures, nb_pieces
     ❌ m, d, n, x

2. COMMENTER chaque étape clé
     # Étape gloutonne : prendre le max de la plus grosse coupure

3. SÉPARER la logique de l'affichage
     La fonction glouton RETOURNE un résultat
     Une autre fonction AFFICHE le résultat

4. VALIDER les entrées
     Montant négatif ? Non entier ? Zéro ?

5. TESTER chaque fonction isolément
```

#### Étape 3.3 : Implémenter la fonction cœur

```
Squelette à compléter (Python) :

def rendu_monnaie_glouton(montant, coupures):
    """
    Applique l'algorithme glouton pour le rendu de monnaie.

    Args:
        montant  (int) : montant à rendre en FCFA
        coupures (list) : liste des coupures triées décroissant

    Returns:
        dict : {coupure: quantité} pour chaque coupure utilisée
        int  : nombre total de coupures
    """
    # À CODER :
    # 1. Initialiser reste = montant
    # 2. Pour chaque coupure :
    #      a. Calculer combien de fois elle rentre (division entière)
    #      b. Mettre à jour le reste
    #      c. Stocker le résultat si quantité > 0
    # 3. Vérifier que reste == 0
    # 4. Retourner le résultat
    pass
```

#### Étape 3.4 : Implémenter l'affichage

```
Squelette à compléter :

def afficher_rendu(prix, paye, resultat, total_coupures):
    """
    Affiche le ticket de rendu de monnaie formaté.

    Sortie attendue :
    ╔══════════════════════════════════════╗
    ║     DISTRIBUTEUR SOTRA              ║
    ╠══════════════════════════════════════╣
    ║  Prix du ticket  :     1 250 FCFA   ║
    ║  Montant payé    :     5 000 FCFA   ║
    ║  Monnaie rendue  :     3 750 FCFA   ║
    ╠══════════════════════════════════════╣
    ║  Détail du rendu :                  ║
    ║    1 × 2 000 FCFA                   ║
    ║    1 × 1 000 FCFA                   ║
    ║    1 ×   500 FCFA                   ║
    ║    1 ×   200 FCFA                   ║
    ║    1 ×    50 FCFA                   ║
    ╠══════════════════════════════════════╣
    ║  Total coupures  :     5 pièces     ║
    ╚══════════════════════════════════════╝
    """
    # À CODER
    pass
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires de la fonction glouton

```
Tests à implémenter :

TEST 1 — Cas normal
  Entrée  : montant = 550, coupures = [10000,...,5]
  Attendu : {500: 1, 50: 1}, total = 2

TEST 2 — Montant exact avec une seule coupure
  Entrée  : montant = 5000
  Attendu : {5000: 1}, total = 1

TEST 3 — Montant nécessitant beaucoup de petites pièces
  Entrée  : montant = 85
  Attendu : {50: 1, 25: 1, 10: 1}, total = 3

TEST 4 — Montant zéro
  Entrée  : montant = 0
  Attendu : {}, total = 0

TEST 5 — Grand montant
  Entrée  : montant = 9325
  Attendu : {5000:1, 2000:2, 200:1, 100:1, 25:1}, total = 6

TEST 6 — Montant non réalisable
  Entrée  : montant = 3, coupures = [10, 5]
  Attendu : ERREUR (reste ≠ 0)

TEST 7 — Tous les 7 scénarios du cahier des charges
```

#### Étape 4.2 : Vérification de cohérence

```
Après chaque exécution, vérifier automatiquement :

  VÉRIFICATION 1 : somme des coupures = montant à rendre
    Σ (quantité_i × coupure_i) == M  ?

  VÉRIFICATION 2 : toutes les quantités sont ≥ 0
    ∀ i, xᵢ ≥ 0  ?

  VÉRIFICATION 3 : reste final = 0
    reste == 0  ?
```

#### Étape 4.3 : Tests de performance (optionnel)

```
Mesurer le temps d'exécution pour :
  - 1 000 rendus de monnaie aléatoires
  - 100 000 rendus de monnaie aléatoires
  - Montants de 5 FCFA à 100 000 FCFA

Complexité théorique : O(k) par appel, k = 11 coupures
→ Le programme doit être quasi-instantané
```

---

### PHASE 5 — Extension (aller plus loin)

#### Extension 1 : Stock limité de coupures

```
Le distributeur a un stock fini de chaque coupure.
Modifier l'algorithme pour respecter les contraintes de stock.

Nouvelle contrainte :  xᵢ ≤ stockᵢ   ∀ i

Pseudo-code modifié :
  X[i] ← min( reste DIV D[i] , stock[i] )
```

#### Extension 2 : Comparer Glouton vs Programmation Dynamique

```
Implémenter aussi la résolution par programmation dynamique.
Comparer les résultats sur un système NON canonique.

Système non canonique à tester :
  D = {500, 375, 200, 100, 50, 25, 10, 5}

Montant test : 750 FCFA
  Glouton → 500 + 200 + 50 = 3 coupures
  Optimal → 375 + 375 = 2 coupures
  → Le glouton échoue !
```

#### Extension 3 : Interface graphique

```
Créer une interface utilisateur simulant l'écran du distributeur.
  - Affichage du prix
  - Saisie du montant payé
  - Animation du rendu de monnaie
  - Historique des transactions
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Modèle mathématique écrit (fonction objectif + contraintes)
  □ Au moins 2 exemples résolus à la main
  □ Résultats à la main vérifiés

PHASE 2 — Conception
  □ Pseudo-code de l'algorithme glouton
  □ Pseudo-code du programme principal
  □ Structures de données identifiées

PHASE 3 — Implémentation
  □ Fonction rendu_monnaie_glouton() codée
  □ Fonction afficher_rendu() codée
  □ Validation des entrées codée
  □ Code commenté et bien nommé

PHASE 4 — Tests
  □ 7 scénarios du cahier des charges validés
  □ Cas limites testés (0, négatif, non réalisable)
  □ Vérification automatique de cohérence

PHASE 5 — Extensions (bonus)
  □ Stock limité implémenté
  □ Comparaison glouton vs programmation dynamique
  □ Interface graphique (optionnel)
```

---

*Bonne implémentation !*
