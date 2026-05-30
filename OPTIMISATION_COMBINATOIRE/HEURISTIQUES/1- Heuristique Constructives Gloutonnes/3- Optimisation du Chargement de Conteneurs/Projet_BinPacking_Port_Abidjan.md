# 📦 Projet : Optimisation du Chargement de Conteneurs

## Optimisation Combinatoire — Problème de Bin Packing

---

## 📖 Contexte Réel : Le Port Autonome d'Abidjan

Aminata est **responsable logistique** au Port Autonome d'Abidjan. Chaque jour, des dizaines de commandes de marchandises doivent être expédiées vers l'Europe par **conteneurs maritimes**.

Chaque conteneur a une **capacité maximale de 20 tonnes**. Les colis qui arrivent à l'entrepôt ont des **poids variés** et **tous doivent partir** dans le prochain navire.

Le problème : chaque conteneur loué coûte **1 500 000 FCFA**. Aminata doit donc **minimiser le nombre de conteneurs utilisés** pour réduire les coûts d'expédition.

> **Objectif** : Ranger **tous les colis** dans des conteneurs identiques de 20 tonnes en utilisant le **minimum de conteneurs possible**.

C'est exactement un **Problème de Bin Packing** :
- Les **objets** = les colis à expédier
- Les **bins** = les conteneurs maritimes
- La **capacité** = 20 tonnes par conteneur
- L'**objectif** = minimiser le nombre de bins utilisés

---

## 🎯 Cahier des Charges

### Les 15 colis à expédier

| Colis | Contenu | Poids (tonnes) |
|-------|---------|---------------|
| C1 | Cacao en sacs | 8 |
| C2 | Beurre de karité | 5 |
| C3 | Noix de cajou | 12 |
| C4 | Textiles wax | 3 |
| C5 | Café torréfié | 7 |
| C6 | Mangues séchées | 2 |
| C7 | Huile de palme | 9 |
| C8 | Caoutchouc brut | 6 |
| C9 | Bois de teck | 14 |
| C10 | Conserves d'ananas | 4 |
| C11 | Fèves de cacao | 11 |
| C12 | Ignames transformées | 3 |
| C13 | Coton brut | 8 |
| C14 | Attieké déshydraté | 1 |
| C15 | Savon artisanal | 5 |

### Capacité des conteneurs

```
C = 20 tonnes par conteneur
Coût unitaire = 1 500 000 FCFA par conteneur
```

### Borne inférieure théorique

```
Somme totale des poids = 8+5+12+3+7+2+9+6+14+4+11+3+8+1+5 = 98 tonnes

Borne inférieure = ⌈98 / 20⌉ = ⌈4.9⌉ = 5 conteneurs minimum

Coût minimum théorique = 5 × 1 500 000 = 7 500 000 FCFA
```

### Heuristiques à implémenter

| Heuristique | Description |
|-------------|------------|
| **Next Fit (NF)** | Un seul conteneur ouvert à la fois |
| **First Fit (FF)** | Premier conteneur où l'objet rentre |
| **Best Fit (BF)** | Conteneur avec le moins d'espace résiduel |
| **First Fit Decreasing (FFD)** | Trier par poids décroissant + First Fit |
| **Best Fit Decreasing (BFD)** | Trier par poids décroissant + Best Fit |

### Résultat attendu pour chaque heuristique

```
Comparer les 5 heuristiques sur les mêmes données :
  - Nombre de conteneurs utilisés
  - Taux de remplissage moyen
  - Coût total d'expédition
  - Écart par rapport à la borne inférieure
```

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Identifier les données

```
DONNÉES :

n = 15                              (nombre de colis)
C = 20                              (capacité de chaque conteneur, en tonnes)
m = n = 15                          (nombre max de conteneurs, au pire 1 par colis)

Poids des colis :
  s = [8, 5, 12, 3, 7, 2, 9, 6, 14, 4, 11, 3, 8, 1, 5]

Somme totale :
  S = Σ sᵢ = 98 tonnes

Borne inférieure :
  LB = ⌈S / C⌉ = ⌈98/20⌉ = 5 conteneurs
```

#### Étape 1.2 : Définir les variables de décision

```
xᵢⱼ = 1 si le colis i est placé dans le conteneur j, 0 sinon

yⱼ  = 1 si le conteneur j est utilisé, 0 sinon

i = 1, ..., n  (colis)
j = 1, ..., m  (conteneurs)
```

#### Étape 1.3 : Écrire le modèle mathématique complet

```
FONCTION OBJECTIF :

              m
  Minimiser Z = Σ  yⱼ                   (minimiser le nombre de conteneurs)
              j=1


CONTRAINTES :

  (1) Chaque colis dans exactement un conteneur :
       m
       Σ  xᵢⱼ = 1                       ∀ i = 1, ..., n
      j=1

  (2) Capacité de chaque conteneur respectée :
       n
       Σ  sᵢ · xᵢⱼ  ≤  C · yⱼ          ∀ j = 1, ..., m
      i=1

  (3) Variables binaires :
      xᵢⱼ ∈ {0, 1}    ∀ i, j
      yⱼ  ∈ {0, 1}    ∀ j
```

#### Étape 1.4 : Appliquer Next Fit à la main

```
Règle : un seul conteneur ouvert. Si le colis ne rentre pas, fermer et ouvrir un nouveau.
Ordre d'arrivée : C1(8), C2(5), C3(12), C4(3), C5(7), C6(2), C7(9),
                  C8(6), C9(14), C10(4), C11(11), C12(3), C13(8), C14(1), C15(5)

Conteneur 1 : C1(8) → 8/20
              C2(5) → 8+5=13/20
              C3(12) → 13+12=25 > 20 ❌ → FERMER

Conteneur 2 : C3(12) → 12/20
              C4(3) → 12+3=15/20
              C5(7) → 15+7=22 > 20 ❌ → FERMER

Conteneur 3 : C5(7) → 7/20
              C6(2) → 7+2=9/20
              C7(9) → 9+9=18/20
              C8(6) → 18+6=24 > 20 ❌ → FERMER

Conteneur 4 : C8(6) → 6/20
              C9(14) → 6+14=20/20 PLEIN → FERMER

Conteneur 5 : C10(4) → 4/20
              C11(11) → 4+11=15/20
              C12(3) → 15+3=18/20
              C13(8) → 18+8=26 > 20 ❌ → FERMER

Conteneur 6 : C13(8) → 8/20
              C14(1) → 8+1=9/20
              C15(5) → 9+5=14/20 → FIN

RÉSULTAT NF : 6 conteneurs
  Cont.1 : [C1(8), C2(5)]           = 13/20 (65%)
  Cont.2 : [C3(12), C4(3)]          = 15/20 (75%)
  Cont.3 : [C5(7), C6(2), C7(9)]    = 18/20 (90%)
  Cont.4 : [C8(6), C9(14)]          = 20/20 (100%)
  Cont.5 : [C10(4), C11(11), C12(3)]= 18/20 (90%)
  Cont.6 : [C13(8), C14(1), C15(5)] = 14/20 (70%)
  Remplissage moyen : 81.7%
```

#### Étape 1.5 : Appliquer First Fit Decreasing à la main

```
Règle : trier par poids décroissant, puis First Fit.

Tri décroissant :
  C9(14), C3(12), C11(11), C7(9), C1(8), C13(8),
  C5(7), C8(6), C2(5), C15(5), C10(4), C4(3),
  C12(3), C6(2), C14(1)

C9(14) → Cont.1 : [C9(14)] = 14/20

C3(12) → Cont.1 : 14+12=26 > 20 ❌
         Cont.2 : [C3(12)] = 12/20

C11(11)→ Cont.1 : 14+11=25 > 20 ❌
         Cont.2 : 12+11=23 > 20 ❌
         Cont.3 : [C11(11)] = 11/20

C7(9)  → Cont.1 : 14+9=23 > 20 ❌
         Cont.2 : 12+9=21 > 20 ❌
         Cont.3 : 11+9=20 ≤ 20 ✅
         Cont.3 : [C11(11), C7(9)] = 20/20 PLEIN

C1(8)  → Cont.1 : 14+8=22 > 20 ❌
         Cont.2 : 12+8=20 ≤ 20 ✅
         Cont.2 : [C3(12), C1(8)] = 20/20 PLEIN

C13(8) → Cont.1 : 14+8=22 > 20 ❌
         Cont.2 PLEIN
         Cont.3 PLEIN
         Cont.4 : [C13(8)] = 8/20

C5(7)  → Cont.1 : 14+7=21 > 20 ❌
         Cont.4 : 8+7=15 ≤ 20 ✅
         Cont.4 : [C13(8), C5(7)] = 15/20

C8(6)  → Cont.1 : 14+6=20 ≤ 20 ✅
         Cont.1 : [C9(14), C8(6)] = 20/20 PLEIN

C2(5)  → Cont.4 : 15+5=20 ≤ 20 ✅
         Cont.4 : [C13(8), C5(7), C2(5)] = 20/20 PLEIN

C15(5) → Cont.1,2,3,4 tous PLEINS
         Cont.5 : [C15(5)] = 5/20

C10(4) → Cont.5 : 5+4=9 ≤ 20 ✅
         Cont.5 : [C15(5), C10(4)] = 9/20

C4(3)  → Cont.5 : 9+3=12 ≤ 20 ✅
         Cont.5 : [C15(5), C10(4), C4(3)] = 12/20

C12(3) → Cont.5 : 12+3=15 ≤ 20 ✅
         Cont.5 : [C15(5), C10(4), C4(3), C12(3)] = 15/20

C6(2)  → Cont.5 : 15+2=17 ≤ 20 ✅
         Cont.5 : [..., C6(2)] = 17/20

C14(1) → Cont.5 : 17+1=18 ≤ 20 ✅
         Cont.5 : [..., C14(1)] = 18/20 → FIN

RÉSULTAT FFD : 5 conteneurs  ✅ = BORNE INFÉRIEURE !
  Cont.1 : [C9(14), C8(6)]                          = 20/20 (100%)
  Cont.2 : [C3(12), C1(8)]                          = 20/20 (100%)
  Cont.3 : [C11(11), C7(9)]                         = 20/20 (100%)
  Cont.4 : [C13(8), C5(7), C2(5)]                   = 20/20 (100%)
  Cont.5 : [C15(5), C10(4), C4(3), C12(3), C6(2), C14(1)] = 18/20 (90%)
  Remplissage moyen : 98.0%
```

> ✅ FFD atteint la borne inférieure (5 conteneurs) : c'est optimal ici !

---

### PHASE 2 — Conception (pseudo-code)

#### Étape 2.1 : Pseudo-code Next Fit

```
ALGORITHME NextFit

ENTRÉES :
    objets[1..n]  : tableau des poids
    C             : capacité des conteneurs

SORTIE :
    conteneurs    : liste de listes (contenu de chaque bin)

DÉBUT
    conteneurs ← [[]]                    (un conteneur vide)
    remplissage_courant ← 0

    POUR i DE 1 À n FAIRE
        SI remplissage_courant + objets[i] ≤ C ALORS
            Ajouter objets[i] au dernier conteneur
            remplissage_courant ← remplissage_courant + objets[i]
        SINON
            Ouvrir un nouveau conteneur
            conteneurs ← conteneurs + [[objets[i]]]
            remplissage_courant ← objets[i]
        FIN SI
    FIN POUR

    RETOURNER conteneurs
FIN

Complexité : O(n)
```

#### Étape 2.2 : Pseudo-code First Fit

```
ALGORITHME FirstFit

ENTRÉES :
    objets[1..n]  : tableau des poids
    C             : capacité des conteneurs

SORTIE :
    conteneurs    : liste de listes

DÉBUT
    conteneurs ← []
    remplissages ← []                    (poids total de chaque conteneur)

    POUR i DE 1 À n FAIRE
        placé ← FAUX

        POUR j DE 0 À |conteneurs|-1 FAIRE
            SI remplissages[j] + objets[i] ≤ C ALORS
                Ajouter objets[i] dans conteneurs[j]
                remplissages[j] ← remplissages[j] + objets[i]
                placé ← VRAI
                SORTIR DE LA BOUCLE
            FIN SI
        FIN POUR

        SI NON placé ALORS
            conteneurs ← conteneurs + [[objets[i]]]
            remplissages ← remplissages + [objets[i]]
        FIN SI
    FIN POUR

    RETOURNER conteneurs
FIN

Complexité : O(n²)
```

#### Étape 2.3 : Pseudo-code Best Fit

```
ALGORITHME BestFit

ENTRÉES :
    objets[1..n], C

SORTIE :
    conteneurs

DÉBUT
    conteneurs ← []
    remplissages ← []

    POUR i DE 1 À n FAIRE
        meilleur_j ← -1
        meilleur_residu ← +∞

        POUR j DE 0 À |conteneurs|-1 FAIRE
            residu ← C - remplissages[j] - objets[i]
            SI residu ≥ 0 ET residu < meilleur_residu ALORS
                meilleur_j ← j
                meilleur_residu ← residu
            FIN SI
        FIN POUR

        SI meilleur_j ≠ -1 ALORS
            Ajouter objets[i] dans conteneurs[meilleur_j]
            remplissages[meilleur_j] += objets[i]
        SINON
            conteneurs ← conteneurs + [[objets[i]]]
            remplissages ← remplissages + [objets[i]]
        FIN SI
    FIN POUR

    RETOURNER conteneurs
FIN

Complexité : O(n²)
```

#### Étape 2.4 : Pseudo-code des variantes Decreasing

```
ALGORITHME FirstFitDecreasing

ENTRÉES :
    objets[1..n], C

DÉBUT
    objets_triés ← trier objets par poids DÉCROISSANT
    RETOURNER FirstFit(objets_triés, C)
FIN


ALGORITHME BestFitDecreasing

ENTRÉES :
    objets[1..n], C

DÉBUT
    objets_triés ← trier objets par poids DÉCROISSANT
    RETOURNER BestFit(objets_triés, C)
FIN
```

#### Étape 2.5 : Structures de données

```
Structures nécessaires :

1. Liste 1D pour les poids :
     poids = [8, 5, 12, 3, 7, 2, 9, 6, 14, 4, 11, 3, 8, 1, 5]

2. Liste de listes pour les conteneurs :
     conteneurs = [
       [("C9", 14), ("C8", 6)],     # Conteneur 1
       [("C3", 12), ("C1", 8)],     # Conteneur 2
       ...
     ]

3. Liste 1D pour le remplissage courant de chaque conteneur :
     remplissages = [20, 20, 20, 20, 18]

4. Dictionnaire pour chaque colis :
     colis = {"id": "C1", "contenu": "Cacao en sacs", "poids": 8}

Complexité globale :
  Next Fit    : O(n) temps, O(n) espace
  First Fit   : O(n²) temps, O(n) espace
  Best Fit    : O(n²) temps, O(n) espace
  FFD / BFD   : O(n·log(n) + n²) temps
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_binpacking/
│
├── main.py                      Programme principal
│
├── donnees.py                   Données du problème
│   ├── colis                    Liste des colis
│   └── capacite                 Capacité des conteneurs
│
├── heuristiques.py              Les 5 heuristiques
│   ├── next_fit()
│   ├── first_fit()
│   ├── best_fit()
│   ├── first_fit_decreasing()
│   └── best_fit_decreasing()
│
├── affichage.py                 Module affichage
│   ├── afficher_conteneurs()    Détail de chaque conteneur
│   ├── afficher_comparaison()   Tableau comparatif des 5 méthodes
│   └── afficher_trace()         Trace pas à pas
│
├── verification.py              Vérification de cohérence
│   └── verifier_solution()
│
└── tests.py                     Tests unitaires
    ├── test_next_fit()
    ├── test_first_fit()
    ├── test_best_fit()
    ├── test_ffd()
    ├── test_bfd()
    ├── test_cas_limites()
    └── test_verification()
```

#### Étape 3.2 : Squelette des données

```python
# donnees.py — À compléter

colis = [
    {"id": "C1",  "contenu": "Cacao en sacs",       "poids": 8},
    {"id": "C2",  "contenu": "Beurre de karité",    "poids": 5},
    {"id": "C3",  "contenu": "Noix de cajou",       "poids": 12},
    {"id": "C4",  "contenu": "Textiles wax",        "poids": 3},
    {"id": "C5",  "contenu": "Café torréfié",       "poids": 7},
    {"id": "C6",  "contenu": "Mangues séchées",     "poids": 2},
    {"id": "C7",  "contenu": "Huile de palme",      "poids": 9},
    {"id": "C8",  "contenu": "Caoutchouc brut",     "poids": 6},
    {"id": "C9",  "contenu": "Bois de teck",        "poids": 14},
    {"id": "C10", "contenu": "Conserves d'ananas",  "poids": 4},
    {"id": "C11", "contenu": "Fèves de cacao",      "poids": 11},
    {"id": "C12", "contenu": "Ignames transformées", "poids": 3},
    {"id": "C13", "contenu": "Coton brut",          "poids": 8},
    {"id": "C14", "contenu": "Attieké déshydraté",  "poids": 1},
    {"id": "C15", "contenu": "Savon artisanal",     "poids": 5},
]

capacite = 20  # tonnes
cout_conteneur = 1_500_000  # FCFA
```

#### Étape 3.3 : Squelettes des 5 heuristiques

```python
# heuristiques.py — Squelettes à compléter

def next_fit(poids, capacite):
    """
    Heuristique Next Fit.
    Un seul conteneur ouvert à la fois.

    Args:
        poids     (list[int]) : poids de chaque colis
        capacite  (int)       : capacité d'un conteneur

    Returns:
        list[list[int]] : liste de conteneurs, chacun = liste d'indices
    """
    # 1. Ouvrir un premier conteneur
    # 2. Pour chaque colis :
    #      Si il rentre dans le conteneur courant → l'ajouter
    #      Sinon → fermer, ouvrir un nouveau, l'y mettre
    # 3. Retourner la liste des conteneurs
    pass


def first_fit(poids, capacite):
    """
    Heuristique First Fit.
    Placer dans le PREMIER conteneur où l'objet rentre.

    Returns:
        list[list[int]] : conteneurs
    """
    # 1. Pour chaque colis :
    #      Parcourir TOUS les conteneurs ouverts
    #      Placer dans le premier qui a assez de place
    #      Si aucun ne convient → ouvrir un nouveau conteneur
    pass


def best_fit(poids, capacite):
    """
    Heuristique Best Fit.
    Placer dans le conteneur avec le MOINS d'espace résiduel
    (meilleur ajustement).

    Returns:
        list[list[int]] : conteneurs
    """
    # 1. Pour chaque colis :
    #      Parcourir tous les conteneurs ouverts
    #      Trouver celui où l'espace résiduel APRÈS placement est MINIMAL
    #      Si aucun ne convient → ouvrir un nouveau
    pass


def first_fit_decreasing(poids, capacite):
    """
    Trier par poids décroissant puis appliquer First Fit.
    """
    # 1. Créer une copie triée par poids décroissant
    # 2. Appliquer first_fit sur cette copie
    # 3. Retourner le résultat en gardant les identifiants originaux
    pass


def best_fit_decreasing(poids, capacite):
    """
    Trier par poids décroissant puis appliquer Best Fit.
    """
    # 1. Créer une copie triée par poids décroissant
    # 2. Appliquer best_fit sur cette copie
    # 3. Retourner le résultat
    pass
```

#### Étape 3.4 : Affichage attendu

```
═══════════════════════════════════════════════════════════════
   PORT AUTONOME D'ABIDJAN — PLAN DE CHARGEMENT
   Heuristique : First Fit Decreasing (FFD)
═══════════════════════════════════════════════════════════════

  Conteneur 1 : [C9(14t), C8(6t)]                    = 20/20t (100%)
  Conteneur 2 : [C3(12t), C1(8t)]                    = 20/20t (100%)
  Conteneur 3 : [C11(11t), C7(9t)]                   = 20/20t (100%)
  Conteneur 4 : [C13(8t), C5(7t), C2(5t)]            = 20/20t (100%)
  Conteneur 5 : [C15(5t), C10(4t), C4(3t),
                  C12(3t), C6(2t), C14(1t)]           = 18/20t (90%)

  ┌─────────────────────────────────────────┐
  │  Nombre de conteneurs : 5               │
  │  Borne inférieure     : 5               │
  │  Écart (GAP)          : 0%  ← OPTIMAL  │
  │  Remplissage moyen    : 98.0%           │
  │  Coût total           : 7 500 000 FCFA  │
  └─────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════
   COMPARAISON DES 5 HEURISTIQUES
═══════════════════════════════════════════════════════════════

  ┌───────────┬────────────┬────────────┬────────────┬──────────────┐
  │ Méthode   │ Conteneurs │ Remplissage│ GAP        │ Coût (FCFA)  │
  ├───────────┼────────────┼────────────┼────────────┼──────────────┤
  │ NF        │     6      │   81.7%    │  +20.0%    │  9 000 000   │
  │ FF        │     ?      │     ?%     │    ?%      │      ?       │
  │ BF        │     ?      │     ?%     │    ?%      │      ?       │
  │ FFD       │     5      │   98.0%    │   0.0%     │  7 500 000   │
  │ BFD       │     ?      │     ?%     │    ?%      │      ?       │
  └───────────┴────────────┴────────────┴────────────┴──────────────┘

  Borne inférieure : 5 conteneurs
  Meilleure heuristique : ___________
```

#### Étape 3.5 : Règles de codage

```
1. INTERFACE COMMUNE pour les 5 heuristiques
     Même signature : heuristique(poids, capacite) → list[list]
     Permet de les comparer avec une seule boucle

2. SÉPARER les responsabilités
     heuristiques.py  → logique pure (pas de print)
     affichage.py     → affichage formaté
     verification.py  → vérification de cohérence

3. TRAÇABILITÉ
     Chaque colis doit garder son identifiant (C1, C2, ...)
     même après le tri pour FFD/BFD

4. MÉTRIQUES automatiques
     Fonction qui calcule : nb conteneurs, remplissage moyen,
     GAP par rapport à la borne inférieure, coût total

5. MODE VERBOSE optionnel
     Afficher chaque décision : "C9(14t) → Conteneur 1 (nouveau)"
                                "C8(6t) → Conteneur 1 (reste 0t)"
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Données du cahier des charges (15 colis)
  NF  : vérifier 6 conteneurs
  FFD : vérifier 5 conteneurs

TEST 2 — Un seul objet
  Entrée : poids = [15], C = 20
  Attendu : 1 conteneur pour toutes les heuristiques

TEST 3 — Objets identiques
  Entrée : poids = [10, 10, 10, 10], C = 20
  Attendu : 2 conteneurs (2 par bin)

TEST 4 — Objet = capacité
  Entrée : poids = [20, 20, 20], C = 20
  Attendu : 3 conteneurs (1 par bin)

TEST 5 — Tous les objets rentrent dans un seul conteneur
  Entrée : poids = [1, 2, 3, 4], C = 20
  Attendu : 1 conteneur

TEST 6 — Objet trop gros
  Entrée : poids = [25], C = 20
  Attendu : ERREUR (objet > capacité)

TEST 7 — Cas pathologique pour Next Fit
  Entrée : poids = [11, 7, 7, 6, 6], C = 20
  NF : combien de conteneurs ? Comparer avec FFD.

TEST 8 — Grande instance aléatoire
  Entrée : 100 colis, poids aléatoires entre 1 et C
  Vérifier cohérence et comparer les 5 heuristiques
```

#### Étape 4.2 : Vérification automatique de cohérence

```python
def verifier_solution(conteneurs, poids_originaux, capacite):
    """
    Vérifie la cohérence d'une solution de bin packing.

    Vérifications :
      1. Chaque colis apparaît exactement UNE fois
      2. Aucun conteneur ne dépasse la capacité
      3. Nombre de conteneurs ≥ borne inférieure
      4. Tous les colis sont bien placés (aucun oublié)

    Returns:
        bool : True si tout est OK
        list[str] : messages d'erreur éventuels
    """
    # À CODER :
    # 1. Collecter tous les colis de tous les conteneurs → ensemble
    # 2. Vérifier : ensemble == {tous les colis originaux}
    # 3. Pour chaque conteneur : somme des poids ≤ C
    # 4. nb_conteneurs ≥ ⌈somme / C⌉
    pass
```

#### Étape 4.3 : Métriques de performance

```python
def calculer_metriques(conteneurs, poids_originaux, capacite, cout_unitaire):
    """
    Calcule les indicateurs de performance.

    Returns:
        dict avec :
          - nb_conteneurs     : int
          - borne_inferieure  : int
          - gap_pourcent       : float
          - remplissage_moyen : float
          - cout_total        : int
    """
    # nb = len(conteneurs)
    # LB = ceil(sum(poids) / capacite)
    # gap = (nb - LB) / LB * 100
    # remplissage = sum(poids) / (nb * capacite) * 100
    # cout = nb * cout_unitaire
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Génération aléatoire de grandes instances

```
Générer N colis aléatoires (N = 50, 100, 500, 1000)
Poids entre 1 et C
Comparer les 5 heuristiques sur chaque instance
Moyenner les résultats sur 100 instances aléatoires

Tableau attendu :
  ┌──────┬──────┬──────┬──────┬──────┬──────┐
  │  N   │  NF  │  FF  │  BF  │  FFD │  BFD │
  ├──────┼──────┼──────┼──────┼──────┼──────┤
  │  50  │  ?   │  ?   │  ?   │  ?   │  ?   │ (nb moyen conteneurs)
  │  100 │  ?   │  ?   │  ?   │  ?   │  ?   │
  │  500 │  ?   │  ?   │  ?   │  ?   │  ?   │
  │ 1000 │  ?   │  ?   │  ?   │  ?   │  ?   │
  └──────┴──────┴──────┴──────┴──────┴──────┘
```

#### Extension 2 : Résolution exacte (force brute / backtracking)

```
Pour les petites instances (n ≤ 15) :
  Énumérer toutes les affectations possibles
  Trouver la solution avec le minimum de conteneurs
  Calculer le GAP exact de chaque heuristique

Attention : complexité exponentielle, uniquement petites instances !
```

#### Extension 3 : Visualisation graphique

```
Avec matplotlib :
  1. Barplot empilé : chaque barre = un conteneur,
     segments colorés = colis dedans
  2. Graphique comparatif : nb conteneurs par heuristique
  3. Courbe : GAP moyen en fonction de n (taille de l'instance)
  4. Histogramme : distribution du remplissage des conteneurs
```

#### Extension 4 : Bin Packing 2D (bonus avancé)

```
Les colis ont maintenant un poids ET un volume.
Conteneurs limités en poids (20t) ET en volume (30 m³).

C'est un Bin Packing multidimensionnel.
Adapter les heuristiques pour vérifier les 2 contraintes.
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Modèle mathématique complet (objectif + contraintes)
  □ Borne inférieure calculée (5 conteneurs)
  □ Next Fit résolu à la main (6 conteneurs)
  □ FFD résolu à la main (5 conteneurs, optimal)

PHASE 2 — Conception
  □ Pseudo-code Next Fit
  □ Pseudo-code First Fit
  □ Pseudo-code Best Fit
  □ Pseudo-code FFD et BFD
  □ Structures de données identifiées

PHASE 3 — Implémentation
  □ next_fit() codé et fonctionnel
  □ first_fit() codé et fonctionnel
  □ best_fit() codé et fonctionnel
  □ first_fit_decreasing() codé et fonctionnel
  □ best_fit_decreasing() codé et fonctionnel
  □ Affichage formaté des résultats
  □ Tableau comparatif des 5 méthodes
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 8 tests unitaires validés
  □ Vérification automatique de cohérence
  □ Métriques calculées (conteneurs, GAP, remplissage, coût)

PHASE 5 — Extensions (bonus)
  □ Grandes instances aléatoires (50 à 1000 colis)
  □ Force brute (petites instances)
  □ Visualisation graphique
  □ Bin Packing 2D
```

---

## 📐 Rappels Théoriques

### Garanties théoriques des heuristiques

```
Next Fit :            NF(I) ≤ 2 · OPT(I)
                      → Au pire 2× l'optimal

First Fit :           FF(I) ≤ ⌈1.7 · OPT(I)⌉
                      → Au pire 1.7× l'optimal

Best Fit :            BF(I) ≤ ⌈1.7 · OPT(I)⌉
                      → Même garantie que FF

First Fit Decreasing : FFD(I) ≤ (11/9) · OPT(I) + 6/9
                      → Au pire ~1.22× l'optimal

Best Fit Decreasing :  BFD(I) ≤ (11/9) · OPT(I) + 6/9
                      → Même garantie que FFD
```

### Modèle mathématique complet

```
              m
  Min Z =     Σ  yⱼ
             j=1

  s.c. :
    m
    Σ  xᵢⱼ = 1                    ∀ i = 1,...,n   (placement unique)
   j=1

    n
    Σ  sᵢ · xᵢⱼ  ≤  C · yⱼ       ∀ j = 1,...,m   (capacité)
   i=1

    xᵢⱼ ∈ {0,1}    yⱼ ∈ {0,1}
```

### Complexité

```
  Next Fit    : O(n)             → le plus rapide
  First Fit   : O(n²)           → bon compromis
  Best Fit    : O(n²)           → léger surcoût vs FF
  FFD / BFD   : O(n·log n + n²) → meilleure qualité
  Exact       : NP-difficile     → exponentiel
```

---

*Bonne implémentation ! 💪*
