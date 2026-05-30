# 🚀 Projet : Sélection de Projets d'Investissement

## Optimisation Combinatoire — Sac à Dos Multidimensionnel (MKP)

---

## 📖 Contexte Réel : Le Directeur de la Startup Digitale

Moussa est **directeur général** d'une startup technologique à Abidjan spécialisée dans les applications mobiles. Son entreprise connaît une croissance rapide et il a identifié **10 projets potentiels** à lancer cette année.

Le problème : il ne peut pas tous les réaliser. Il est limité par **3 ressources simultanées** :

- **💰 Budget** : enveloppe financière annuelle limitée
- **👨‍💻 Développeurs** : nombre de développeurs disponibles (en mois-homme)
- **⏱️ Temps** : délai maximum avant livraison (en mois)

> **Objectif** : Sélectionner le **sous-ensemble de projets** qui **maximise le profit total**, sans dépasser aucune des 3 contraintes de ressources.

C'est exactement un **Sac à Dos Multidimensionnel** :
- Les **objets** = les projets
- La **valeur** = le profit estimé
- Les **dimensions** = budget, développeurs, temps

---

## 🎯 Cahier des Charges

### Les 10 projets candidats

| Projet | Description | Profit (M FCFA) | Budget (M FCFA) | Dev (mois-homme) | Temps (mois) |
|--------|-------------|-----------------|-----------------|-------------------|-------------|
| P1 | App livraison alimentaire | 45 | 30 | 8 | 5 |
| P2 | Plateforme e-learning | 60 | 40 | 12 | 7 |
| P3 | App de covoiturage | 35 | 20 | 6 | 4 |
| P4 | Système de paiement mobile | 80 | 55 | 15 | 9 |
| P5 | App de gestion de stock | 25 | 15 | 5 | 3 |
| P6 | Réseau social local | 50 | 35 | 10 | 6 |
| P7 | Plateforme de freelance | 40 | 25 | 7 | 5 |
| P8 | App de suivi médical | 55 | 38 | 11 | 8 |
| P9 | Marketplace artisanat | 30 | 18 | 6 | 4 |
| P10 | Chatbot service client | 20 | 10 | 4 | 2 |

### Les ressources disponibles (capacités)

| Ressource | Capacité maximale | Symbole |
|-----------|------------------|---------|
| Budget annuel | 100 millions FCFA | W₁ = 100 |
| Développeurs | 30 mois-homme | W₂ = 30 |
| Temps max | 12 mois | W₃ = 12 |

### Contrainte supplémentaire

- Chaque projet est **indivisible** : on le prend entièrement ou pas du tout (variable binaire 0/1)
- Les projets sélectionnés se réalisent **en parallèle** (le temps = max des temps, mais pour simplifier on considère que la contrainte temps porte sur la somme pondérée)

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Identifier les données du problème

```
DONNÉES :

n = 10                          (nombre de projets)
m = 3                           (nombre de contraintes / dimensions)

Profits :
  v = [45, 60, 35, 80, 25, 50, 40, 55, 30, 20]

Matrice des consommations de ressources :

              Budget(j=1)   Dev(j=2)   Temps(j=3)
  Projet P1 :    30            8           5
  Projet P2 :    40           12           7
  Projet P3 :    20            6           4
  Projet P4 :    55           15           9
  Projet P5 :    15            5           3
  Projet P6 :    35           10           6
  Projet P7 :    25            7           5
  Projet P8 :    38           11           8
  Projet P9 :    18            6           4
  Projet P10:    10            4           2

Capacités :
  W = [100, 30, 12]
```

#### Étape 1.2 : Définir les variables de décision

```
Pour chaque projet i = 1, ..., 10 :

         ⎧ 1   si le projet i est sélectionné
  xᵢ =  ⎨
         ⎩ 0   sinon
```

#### Étape 1.3 : Écrire le modèle mathématique complet

```
FONCTION OBJECTIF :

                 10
  Maximiser Z =  Σ  vᵢ · xᵢ
                i=1

  Z = 45·x₁ + 60·x₂ + 35·x₃ + 80·x₄ + 25·x₅
    + 50·x₆ + 40·x₇ + 55·x₈ + 30·x₉ + 20·x₁₀


CONTRAINTES DE RESSOURCES :

  Contrainte Budget (j=1) :
  30·x₁ + 40·x₂ + 20·x₃ + 55·x₄ + 15·x₅
  + 35·x₆ + 25·x₇ + 38·x₈ + 18·x₉ + 10·x₁₀  ≤  100

  Contrainte Développeurs (j=2) :
  8·x₁ + 12·x₂ + 6·x₃ + 15·x₄ + 5·x₅
  + 10·x₆ + 7·x₇ + 11·x₈ + 6·x₉ + 4·x₁₀  ≤  30

  Contrainte Temps (j=3) :
  5·x₁ + 7·x₂ + 4·x₃ + 9·x₄ + 3·x₅
  + 6·x₆ + 5·x₇ + 8·x₈ + 4·x₉ + 2·x₁₀  ≤  12


CONTRAINTES DE VARIABLES :

  xᵢ ∈ {0, 1}    ∀ i = 1, ..., 10
```

#### Étape 1.4 : Calculer le ratio glouton agrégé

```
Le critère glouton multidimensionnel :

              vᵢ
  rᵢ = ─────────────────
         m
         Σ  (wᵢⱼ / Wⱼ)
        j=1

Chaque terme wᵢⱼ / Wⱼ = fraction de la ressource j consommée par le projet i
On somme ces fractions pour obtenir un coût normalisé global

CALCUL POUR CHAQUE PROJET :

P1 :  coût = 30/100 + 8/30 + 5/12
           = 0.300 + 0.267 + 0.417 = 0.983
      ratio = 45 / 0.983 = 45.78

P2 :  coût = 40/100 + 12/30 + 7/12
           = 0.400 + 0.400 + 0.583 = 1.383
      ratio = 60 / 1.383 = 43.38

P3 :  coût = 20/100 + 6/30 + 4/12
           = 0.200 + 0.200 + 0.333 = 0.733
      ratio = 35 / 0.733 = 47.75

P4 :  coût = 55/100 + 15/30 + 9/12
           = 0.550 + 0.500 + 0.750 = 1.800
      ratio = 80 / 1.800 = 44.44

P5 :  coût = 15/100 + 5/30 + 3/12
           = 0.150 + 0.167 + 0.250 = 0.567
      ratio = 25 / 0.567 = 44.09

P6 :  coût = 35/100 + 10/30 + 6/12
           = 0.350 + 0.333 + 0.500 = 1.183
      ratio = 50 / 1.183 = 42.26

P7 :  coût = 25/100 + 7/30 + 5/12
           = 0.250 + 0.233 + 0.417 = 0.900
      ratio = 40 / 0.900 = 44.44

P8 :  coût = 38/100 + 11/30 + 8/12
           = 0.380 + 0.367 + 0.667 = 1.413
      ratio = 55 / 1.413 = 38.92

P9 :  coût = 18/100 + 6/30 + 4/12
           = 0.180 + 0.200 + 0.333 = 0.713
      ratio = 30 / 0.713 = 42.07

P10 : coût = 10/100 + 4/30 + 2/12
           = 0.100 + 0.133 + 0.167 = 0.400
      ratio = 20 / 0.400 = 50.00
```

#### Étape 1.5 : Classement par ratio décroissant

```
  Rang 1  : P10  ratio = 50.00
  Rang 2  : P3   ratio = 47.75
  Rang 3  : P1   ratio = 45.78
  Rang 4  : P4   ratio = 44.44
  Rang 5  : P7   ratio = 44.44
  Rang 6  : P5   ratio = 44.09
  Rang 7  : P2   ratio = 43.38
  Rang 8  : P6   ratio = 42.26
  Rang 9  : P9   ratio = 42.07
  Rang 10 : P8   ratio = 38.92
```

#### Étape 1.6 : Appliquer le glouton à la main

```
Capacités restantes : Budget=100, Dev=30, Temps=12
Profit total = 0

─── P10 (budget=10, dev=4, temps=2, profit=20) ───
  Budget : 10 ≤ 100 ✅
  Dev    : 4 ≤ 30   ✅
  Temps  : 2 ≤ 12   ✅
  → ON PREND P10
  Restant : Budget=90, Dev=26, Temps=10 | Profit=20

─── P3 (budget=20, dev=6, temps=4, profit=35) ───
  Budget : 20 ≤ 90  ✅
  Dev    : 6 ≤ 26   ✅
  Temps  : 4 ≤ 10   ✅
  → ON PREND P3
  Restant : Budget=70, Dev=20, Temps=6 | Profit=55

─── P1 (budget=30, dev=8, temps=5, profit=45) ───
  Budget : 30 ≤ 70  ✅
  Dev    : 8 ≤ 20   ✅
  Temps  : 5 ≤ 6    ✅
  → ON PREND P1
  Restant : Budget=40, Dev=12, Temps=1 | Profit=100

─── P4 (budget=55, dev=15, temps=9, profit=80) ───
  Budget : 55 > 40  ❌ DÉPASSE
  → ON PASSE

─── P7 (budget=25, dev=7, temps=5, profit=40) ───
  Temps  : 5 > 1    ❌ DÉPASSE
  → ON PASSE

─── P5 (budget=15, dev=5, temps=3, profit=25) ───
  Temps  : 3 > 1    ❌ DÉPASSE
  → ON PASSE

─── P2, P6, P9, P8 ───
  Tous ont temps > 1 ❌
  → ON PASSE TOUS


RÉSULTAT GLOUTON :
  Projets sélectionnés : {P10, P3, P1}
  Budget utilisé  : 10+20+30 = 60/100
  Dev utilisés    : 4+6+8   = 18/30
  Temps utilisé   : 2+4+5   = 11/12
  Profit total    : 20+35+45 = 100 M FCFA
```

> ✅ Vérifie que tu obtiens le même résultat avant de passer au code.

---

### PHASE 2 — Conception de l'Algorithme (pseudo-code)

#### Étape 2.1 : Pseudo-code du calcul du ratio agrégé

```
FONCTION calculer_ratios(profits, conso, capacites)

ENTRÉES :
    profits[1..n]       : tableau des profits
    conso[1..n][1..m]   : matrice des consommations
    capacites[1..m]     : tableau des capacités

SORTIE :
    ratios[1..n]        : tableau des ratios agrégés

DÉBUT
    POUR i DE 1 À n FAIRE
        cout_normalise ← 0
        POUR j DE 1 À m FAIRE
            cout_normalise ← cout_normalise + conso[i][j] / capacites[j]
        FIN POUR

        SI cout_normalise > 0 ALORS
            ratios[i] ← profits[i] / cout_normalise
        SINON
            ratios[i] ← +∞
        FIN SI
    FIN POUR

    RETOURNER ratios
FIN
```

#### Étape 2.2 : Pseudo-code de l'heuristique gloutonne MKP

```
ALGORITHME SacADosMultidimensionnelGlouton

ENTRÉES :
    n                   : nombre d'objets (projets)
    m                   : nombre de contraintes (ressources)
    profits[1..n]       : profits de chaque projet
    conso[1..n][1..m]   : consommation de chaque projet par ressource
    capacites[1..m]     : capacités max de chaque ressource

SORTIE :
    selection[1..n]     : tableau binaire (1=pris, 0=non)
    profit_total        : profit de la solution
    ressources_utilisees[1..m] : consommation totale par ressource

DÉBUT
    ── Étape 1 : Calculer les ratios ──
    ratios ← calculer_ratios(profits, conso, capacites)

    ── Étape 2 : Trier par ratio décroissant ──
    ordre ← indices_tri_decroissant(ratios)

    ── Étape 3 : Construction gloutonne ──
    selection ← [0, 0, ..., 0]         (n zéros)
    reste[1..m] ← copie(capacites)
    profit_total ← 0

    POUR k DE 1 À n FAIRE
        i ← ordre[k]                   (projet courant dans l'ordre trié)

        ── Vérifier TOUTES les contraintes ──
        faisable ← VRAI
        POUR j DE 1 À m FAIRE
            SI conso[i][j] > reste[j] ALORS
                faisable ← FAUX
                SORTIR DE LA BOUCLE
            FIN SI
        FIN POUR

        ── Si faisable, prendre le projet ──
        SI faisable ALORS
            selection[i] ← 1
            profit_total ← profit_total + profits[i]
            POUR j DE 1 À m FAIRE
                reste[j] ← reste[j] - conso[i][j]
            FIN POUR
        FIN SI
    FIN POUR

    RETOURNER selection, profit_total, capacites - reste
FIN
```

#### Étape 2.3 : Structures de données

```
Structures nécessaires :

1. Liste/Tableau 1D :
     profits   = [45, 60, 35, 80, 25, 50, 40, 55, 30, 20]
     capacites = [100, 30, 12]
     ratios    = [45.78, 43.38, ...]
     selection = [0, 0, 1, 0, 0, 0, 0, 0, 0, 1]  (binaire)

2. Matrice 2D (liste de listes) :
     conso = [
       [30, 8, 5],    # P1
       [40, 12, 7],   # P2
       ...
     ]

3. Dictionnaire/Structure pour chaque projet :
     projet = {
       "nom": "App livraison",
       "profit": 45,
       "ressources": [30, 8, 5]
     }

Complexité :
  Temps  : O(n·log(n) + n·m) → tri + parcours glouton
  Espace : O(n·m) pour la matrice
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_mkp/
│
├── main.py                     Programme principal
│
├── donnees.py                  Données du problème
│   ├── projets                 Liste des projets
│   ├── capacites               Capacités des ressources
│   └── noms_ressources         Labels des ressources
│
├── glouton_mkp.py              Module cœur
│   ├── calculer_ratios()       Ratios agrégés
│   ├── glouton_mkp()           Algorithme glouton
│   └── verifier_solution()     Vérification de faisabilité
│
├── affichage.py                Module affichage
│   ├── afficher_projets()      Tableau des projets
│   ├── afficher_ratios()       Classement des ratios
│   ├── afficher_solution()     Résultat formaté
│   └── afficher_trace()        Trace pas à pas du glouton
│
└── tests.py                    Tests unitaires
    ├── test_ratios()
    ├── test_glouton_cas_normal()
    ├── test_glouton_aucun_projet()
    ├── test_glouton_tous_projets()
    └── test_verification()
```

#### Étape 3.2 : Squelette de la structure de données

```python
# Squelette à compléter (Python)

# Chaque projet est un dictionnaire
projets = [
    {
        "id": "P1",
        "nom": "App livraison alimentaire",
        "profit": 45,
        "ressources": [30, 8, 5]   # [budget, dev, temps]
    },
    # ... P2 à P10
]

capacites = [100, 30, 12]
noms_ressources = ["Budget (M FCFA)", "Dev (mois-homme)", "Temps (mois)"]
```

#### Étape 3.3 : Squelette de la fonction des ratios

```python
def calculer_ratios(projets, capacites):
    """
    Calcule le ratio glouton agrégé pour chaque projet.

    ratio_i = profit_i / somme_j(conso_ij / capacite_j)

    Args:
        projets   (list[dict]) : liste des projets
        capacites (list[int])  : capacités des ressources

    Returns:
        list[tuple] : [(indice, ratio), ...] trié décroissant
    """
    # 1. Pour chaque projet :
    #      a. Calculer le coût normalisé = Σ (wij / Wj)
    #      b. Calculer le ratio = profit / coût normalisé
    # 2. Trier par ratio décroissant
    # 3. Retourner la liste triée
    pass
```

#### Étape 3.4 : Squelette de la fonction gloutonne

```python
def glouton_mkp(projets, capacites):
    """
    Résout le MKP par heuristique gloutonne.

    Args:
        projets   (list[dict]) : liste des projets
        capacites (list[int])  : capacités des ressources

    Returns:
        list[dict] : projets sélectionnés
        int        : profit total
        list[int]  : ressources utilisées par dimension
    """
    # 1. Calculer les ratios agrégés
    # 2. Trier les projets par ratio décroissant
    # 3. Pour chaque projet (dans l'ordre trié) :
    #      a. Vérifier si TOUTES les contraintes sont respectées
    #      b. Si oui → sélectionner le projet, mettre à jour les restes
    #      c. Si non → passer au projet suivant
    # 4. Retourner la solution
    pass
```

#### Étape 3.5 : Squelette de l'affichage

```
Affichage attendu du résultat :

══════════════════════════════════════════════════════════
   SÉLECTION DE PROJETS — STARTUP DIGITALE ABIDJAN
══════════════════════════════════════════════════════════

  PROJETS SÉLECTIONNÉS :
  ┌──────┬──────────────────────────┬──────────┐
  │ ID   │ Nom                      │ Profit   │
  ├──────┼──────────────────────────┼──────────┤
  │ P10  │ Chatbot service client   │ 20 M     │
  │ P3   │ App de covoiturage       │ 35 M     │
  │ P1   │ App livraison aliment.   │ 45 M     │
  └──────┴──────────────────────────┴──────────┘

  UTILISATION DES RESSOURCES :
  ┌────────────────────┬──────────┬──────────┬───────────┐
  │ Ressource          │ Utilisé  │ Capacité │ Taux      │
  ├────────────────────┼──────────┼──────────┼───────────┤
  │ Budget (M FCFA)    │ 60       │ 100      │ 60.0%     │
  │ Dev (mois-homme)   │ 18       │ 30       │ 60.0%     │
  │ Temps (mois)       │ 11       │ 12       │ 91.7%     │
  └────────────────────┴──────────┴──────────┴───────────┘

  PROFIT TOTAL : 100 M FCFA
  NOMBRE DE PROJETS : 3 / 10

══════════════════════════════════════════════════════════
```

#### Étape 3.6 : Règles de codage

```
1. NOMMER clairement
     ✅ profit_total, capacites_restantes, cout_normalise
     ❌ p, c, cn, x

2. COMMENTER chaque bloc logique
     # Calcul du ratio agrégé pour le projet i
     # Vérification de faisabilité sur toutes les dimensions

3. SÉPARER les responsabilités
     glouton_mkp()     → calcule la solution
     afficher_solution() → affiche le résultat
     verifier_solution() → vérifie la cohérence

4. GÉRER les cas limites
     Aucun projet faisable ? Tous les projets faisables ?
     Capacité zéro sur une dimension ?

5. TRACER l'exécution (mode verbose)
     Afficher chaque décision : "P3 pris / P4 refusé (budget)"
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Calcul des ratios
  Entrée  : projet P10, profit=20, ressources=[10,4,2], cap=[100,30,12]
  Attendu : coût = 0.100+0.133+0.167 = 0.400, ratio = 50.00

TEST 2 — Cas normal (données du cahier des charges)
  Entrée  : 10 projets, 3 ressources
  Attendu : sélection {P10, P3, P1}, profit = 100

TEST 3 — Un seul projet faisable
  Entrée  : capacités très faibles [10, 4, 2]
  Attendu : seul P10 rentre → profit = 20

TEST 4 — Aucun projet faisable
  Entrée  : capacités [1, 1, 1]
  Attendu : aucun projet → profit = 0

TEST 5 — Tous les projets faisables
  Entrée  : capacités [1000, 1000, 1000]
  Attendu : tous pris → profit = 440

TEST 6 — Projet unique très gros
  Entrée  : P4 seul candidat, capacités [55, 15, 9]
  Attendu : P4 pris → profit = 80
```

#### Étape 4.2 : Vérification automatique de cohérence

```
Après chaque exécution, vérifier :

  VÉRIFICATION 1 : Toutes les contraintes respectées
    Pour chaque dimension j :
      Σ (conso[i][j] × selection[i]) ≤ capacite[j]  ?

  VÉRIFICATION 2 : Profit correctement calculé
    Σ (profit[i] × selection[i]) == profit_total  ?

  VÉRIFICATION 3 : Variables binaires
    Pour tout i : selection[i] ∈ {0, 1}  ?

  VÉRIFICATION 4 : Aucun projet refusé à tort
    Pour chaque projet NON sélectionné :
      Vérifier qu'il ne rentre effectivement pas
      dans les capacités restantes
```

#### Étape 4.3 : Fonction de vérification

```python
def verifier_solution(selection, projets, capacites, profit_annonce):
    """
    Vérifie la cohérence de la solution gloutonne.

    Returns:
        bool : True si toutes les vérifications passent
        list[str] : messages d'erreur éventuels
    """
    # 1. Vérifier les contraintes de capacité
    # 2. Vérifier le calcul du profit
    # 3. Vérifier que les variables sont binaires
    # 4. Afficher OK ou les erreurs trouvées
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Comparer plusieurs critères gloutons

```
Implémenter 3 variantes du critère glouton :

CRITÈRE A — Ratio agrégé (celui vu au-dessus)
  rᵢ = vᵢ / Σⱼ(wᵢⱼ/Wⱼ)

CRITÈRE B — Ratio sur la ressource la plus rare
  Identifier la ressource la plus tendue (taux d'utilisation max)
  rᵢ = vᵢ / wᵢⱼ* où j* = ressource la plus rare

CRITÈRE C — Profit pur (prendre le plus rentable d'abord)
  rᵢ = vᵢ

Comparer les résultats des 3 critères sur les mêmes données.
Lequel donne le meilleur profit ?
```

#### Extension 2 : Résolution exacte par force brute

```
Énumérer toutes les 2ⁿ = 2¹⁰ = 1024 combinaisons possibles.
Pour chaque combinaison :
  - Vérifier la faisabilité
  - Calculer le profit
  - Garder la meilleure

Comparer le résultat exact avec le résultat glouton.
Calculer le GAP :
  GAP = (Optimal - Glouton) / Optimal × 100%
```

#### Extension 3 : Métaheuristique — Algorithme Génétique

```
Implémenter un algorithme génétique pour le MKP :
  - Chromosome = vecteur binaire [x₁, x₂, ..., x₁₀]
  - Fitness = profit si faisable, pénalité sinon
  - Croisement = crossover en un point
  - Mutation = flip d'un bit aléatoire
  - Sélection = tournoi ou roulette

Comparer : Glouton vs Force Brute vs Génétique
  - Qualité de la solution
  - Temps d'exécution
```

#### Extension 4 : Visualisation graphique

```
Créer des graphiques avec matplotlib :
  1. Barplot des profits des projets sélectionnés vs non sélectionnés
  2. Graphique de l'utilisation des ressources (barres empilées)
  3. Radar chart des ratios par projet
  4. Comparaison Glouton vs Optimal (si Extension 2 faite)
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Variables de décision définies
  □ Modèle mathématique complet (objectif + 3 contraintes + binaire)
  □ Ratios agrégés calculés pour les 10 projets
  □ Classement par ratio effectué
  □ Glouton résolu à la main → résultat : {P10, P3, P1}, profit = 100

PHASE 2 — Conception
  □ Pseudo-code du calcul des ratios
  □ Pseudo-code de l'algorithme glouton MKP
  □ Structures de données choisies

PHASE 3 — Implémentation
  □ donnees.py : données du problème
  □ glouton_mkp.py : fonctions calculer_ratios() et glouton_mkp()
  □ affichage.py : affichage formaté
  □ verifier_solution() : vérification de cohérence
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 6 tests unitaires validés
  □ Cas limites testés (aucun, tous, un seul projet)
  □ Vérification automatique de cohérence

PHASE 5 — Extensions (bonus)
  □ 3 critères gloutons comparés
  □ Résolution exacte (force brute)
  □ Algorithme génétique
  □ Visualisation graphique
```

---

## 📐 Rappels Théoriques

### Formule du ratio agrégé

```
              vᵢ
  rᵢ = ─────────────────
         m
         Σ  (wᵢⱼ / Wⱼ)
        j=1

  vᵢ   = profit du projet i
  wᵢⱼ  = consommation du projet i sur la ressource j
  Wⱼ   = capacité de la ressource j
```

### Modèle MKP complet

```
              n
  Max Z =     Σ  vᵢ · xᵢ
             i=1

  s.c. :
    n
    Σ  wᵢⱼ · xᵢ  ≤  Wⱼ      ∀ j = 1, ..., m
   i=1

    xᵢ ∈ {0, 1}               ∀ i = 1, ..., n
```

### Complexité

```
  Algorithme glouton : O(n·log(n) + n·m)   → polynomial, rapide
  Force brute        : O(2ⁿ · m)           → exponentiel, exact
  Algo génétique     : O(G · P · n · m)    → paramétrable
                       G=générations, P=population
```

---

*Bonne implémentation ! 💪*
