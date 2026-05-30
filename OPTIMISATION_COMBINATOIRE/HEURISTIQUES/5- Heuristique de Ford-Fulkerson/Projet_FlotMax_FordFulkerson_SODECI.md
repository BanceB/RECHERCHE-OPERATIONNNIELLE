# 💧 Projet : Optimisation du Réseau de Distribution d'Eau

## Optimisation Combinatoire — Flot Maximal & Algorithme de Ford-Fulkerson

---

## 📖 Contexte Réel : La SODECI — Réseau d'Eau d'Abidjan

M. Ouattara est **ingénieur réseau** à la SODECI (Société de Distribution d'Eau de Côte d'Ivoire). Pendant la saison sèche, la demande en eau potable explose dans les quartiers d'Abidjan. Il doit déterminer le **débit maximal** que le réseau de canalisations peut acheminer depuis la **station de pompage principale** (source) jusqu'au **réservoir terminal** de distribution (puits).

Chaque canalisation a une **capacité maximale** (en m³/heure) qu'elle ne peut pas dépasser. L'eau traverse plusieurs **stations intermédiaires** (nœuds de jonction, stations de surpression) avant d'atteindre le réservoir.

> **Objectif** : Déterminer le **débit maximal** d'eau pouvant transiter de la source au puits sans dépasser la capacité d'aucune canalisation.

C'est exactement un **Problème de Flot Maximal** :
- Les **sommets** = stations (pompage, jonctions, réservoir)
- Les **arcs** = canalisations orientées
- Les **capacités** = débit max de chaque canalisation (m³/h)
- La **source** s = station de pompage
- Le **puits** t = réservoir terminal
- L'**objectif** = maximiser le flot de s à t

---

## 🎯 Cahier des Charges

### Le réseau de distribution

```
8 stations :

  s   = Station de pompage (Songon)           → SOURCE
  A   = Station de jonction (Yopougon Nord)
  B   = Station de surpression (Adjamé)
  C   = Station de jonction (Plateau)
  D   = Station de surpression (Cocody)
  E   = Station de jonction (Treichville)
  F   = Station de jonction (Koumassi)
  t   = Réservoir terminal (Port-Bouët)       → PUITS
```

### Les canalisations et leurs capacités (m³/h)

| Arc | De | Vers | Capacité (m³/h) |
|-----|-----|------|----------------|
| 1 | s | A | 10 |
| 2 | s | B | 8 |
| 3 | s | C | 7 |
| 4 | A | B | 5 |
| 5 | A | D | 7 |
| 6 | B | D | 6 |
| 7 | B | E | 9 |
| 8 | C | E | 8 |
| 9 | C | F | 4 |
| 10 | D | t | 12 |
| 11 | E | D | 3 |
| 12 | E | F | 5 |
| 13 | E | t | 6 |
| 14 | F | t | 9 |

### Schéma du réseau

```
                    ┌───── A ─────┐
                    │    ╱   ╲    │
              10    │  5       7  │
                    ↓╱           ╲↓
   s ──── 8 ────→ B ──── 6 ────→ D ──── 12 ────→ t
   │              │               ↑               ↑
   │         9    │          3    │          6     │
   │              ↓               │               │
   │              E ──────────────┘               │
   │         ╱    │    ╲                          │
   │    8   ╱     │  5  ╲                    9    │
   │       ╱      ↓      ╲                       │
   └── 7 → C ── 4 → F ────────────────────────→──┘
```

### Vérification du réseau

```
✅ Graphe orienté
✅ Capacités positives sur tous les arcs
✅ Source s : aucun arc entrant
✅ Puits t : aucun arc sortant
✅ Tout sommet sur un chemin de s à t
✅ 8 sommets, 14 arcs

Capacité sortante de s : 10 + 8 + 7 = 25 m³/h
Capacité entrante en t : 12 + 6 + 9 = 27 m³/h
→ Borne supérieure du flot max : min(25, 27) = 25 m³/h
```

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Rappel des définitions fondamentales

```
FLOT ADMISSIBLE ϕ :
  Fonction sur les arcs respectant :

  1) CONTRAINTE DE CAPACITÉ :
     0 ≤ ϕ(u) ≤ c(u)        pour tout arc u
     (le débit ne dépasse jamais la capacité)

  2) CONTRAINTE DE CONSERVATION (Kirchhoff) :
     Σ ϕ(entrant en v) = Σ ϕ(sortant de v)    pour tout v ≠ s, t
     (ce qui entre dans un nœud = ce qui en sort)

VALEUR DU FLOT α :
     α = Σ ϕ(sortant de s) = Σ ϕ(entrant en t)

FLOT MAXIMAL :
     Flot admissible de valeur α maximale
```

#### Étape 1.2 : Rappel — Chaîne augmentante

```
Une chaîne augmentante de s à t est un chemin dans le réseau tel que :

  → Pour tout arc DIRECT (sens s→t) :  ϕ(u) < c(u)
    (il reste de la marge, on peut ajouter du flot)

  → Pour tout arc INDIRECT (sens t→s) : ϕ(u) > 0
    (il y a du flot, on peut en retirer)

L'augmentation possible sur la chaîne :

  δ = min( {c(u) - ϕ(u) | u direct} ∪ {ϕ(u) | u indirect} )
```

#### Étape 1.3 : Modèle mathématique

```
DONNÉES :
  G = (V, E)     graphe orienté
  s = source, t = puits
  c(i,j) = capacité de l'arc (i,j)
  ϕ(i,j) = flot sur l'arc (i,j) — variable de décision

MODÈLE :

  Maximiser α = Σ ϕ(s,j)              (flot sortant de la source)
               j∈Γ⁺(s)

  s.c. :
    Σ ϕ(i,v) = Σ ϕ(v,j)              ∀ v ∈ V \ {s,t}  (conservation)
   i∈Γ⁻(v)    j∈Γ⁺(v)

    0 ≤ ϕ(i,j) ≤ c(i,j)              ∀ (i,j) ∈ E       (capacité)
```

#### Étape 1.4 : Rappel — Théorème Flot Max = Coupe Min

```
La valeur du flot maximal = la capacité de la coupe minimale

  max α(ϕ) = min c(S,T)

  Coupe (S,T) : partition de V avec s ∈ S, t ∈ T
  Capacité de la coupe = Σ c(i,j) pour i ∈ S, j ∈ T

Ce théorème PROUVE l'optimalité de Ford-Fulkerson.
```

#### Étape 1.5 : Algorithme de Ford-Fulkerson — Rappel

```
ALGORITHME FORD-FULKERSON :

1. Initialiser : ϕ(u) = 0 pour tout arc u (flot nul)
2. Tant qu'il existe une chaîne augmentante de s à t :
     a. Trouver une chaîne augmentante (BFS ou DFS)
     b. Calculer δ = augmentation max sur cette chaîne
     c. Mettre à jour le flot :
          - arcs directs : ϕ(u) += δ
          - arcs indirects : ϕ(u) -= δ
3. Quand plus de chaîne augmentante → le flot est MAXIMAL
```

#### Étape 1.6 : Résoudre à la main

```
═══ INITIALISATION ═══

Flot nul : ϕ(u) = 0 pour tout arc
α = 0

Arc         │ Cap │ Flot │ Marge
────────────┼─────┼──────┼──────
s → A       │  10 │  0   │  10
s → B       │   8 │  0   │   8
s → C       │   7 │  0   │   7
A → B       │   5 │  0   │   5
A → D       │   7 │  0   │   7
B → D       │   6 │  0   │   6
B → E       │   9 │  0   │   9
C → E       │   8 │  0   │   8
C → F       │   4 │  0   │   4
D → t       │  12 │  0   │  12
E → D       │   3 │  0   │   3
E → F       │   5 │  0   │   5
E → t       │   6 │  0   │   6
F → t       │   9 │  0   │   9


═══ ITÉRATION 1 ═══

Chaîne augmentante : s → A → D → t
  s→A : marge = 10
  A→D : marge = 7
  D→t : marge = 12
  δ = min(10, 7, 12) = 7

Mise à jour :
  s→A : 0 + 7 = 7
  A→D : 0 + 7 = 7
  D→t : 0 + 7 = 7

α = 0 + 7 = 7


═══ ITÉRATION 2 ═══

Chaîne augmentante : s → B → E → t
  s→B : marge = 8
  B→E : marge = 9
  E→t : marge = 6
  δ = min(8, 9, 6) = 6

Mise à jour :
  s→B : 0 + 6 = 6
  B→E : 0 + 6 = 6
  E→t : 0 + 6 = 6

α = 7 + 6 = 13


═══ ITÉRATION 3 ═══

Chaîne augmentante : s → C → E → F → t
  s→C : marge = 7
  C→E : marge = 8
  E→F : marge = 5
  F→t : marge = 9
  δ = min(7, 8, 5, 9) = 5

Mise à jour :
  s→C : 0 + 5 = 5
  C→E : 0 + 5 = 5
  E→F : 0 + 5 = 5
  F→t : 0 + 5 = 5

α = 13 + 5 = 18


═══ ITÉRATION 4 ═══

Chaîne augmentante : s → C → F → t
  s→C : marge = 7-5 = 2
  C→F : marge = 4
  F→t : marge = 9-5 = 4
  δ = min(2, 4, 4) = 2

Mise à jour :
  s→C : 5 + 2 = 7
  C→F : 0 + 2 = 2
  F→t : 5 + 2 = 7

α = 18 + 2 = 20


═══ ITÉRATION 5 ═══

Chaîne augmentante : s → B → D → t
  s→B : marge = 8-6 = 2
  B→D : marge = 6
  D→t : marge = 12-7 = 5
  δ = min(2, 6, 5) = 2

Mise à jour :
  s→B : 6 + 2 = 8
  B→D : 0 + 2 = 2
  D→t : 7 + 2 = 9

α = 20 + 2 = 22


═══ ITÉRATION 6 ═══

Chaîne augmentante : s → A → B → D → t
  s→A : marge = 10-7 = 3
  A→B : marge = 5
  B→D : marge = 6-2 = 4
  D→t : marge = 12-9 = 3
  δ = min(3, 5, 4, 3) = 3

Mise à jour :
  s→A : 7 + 3 = 10
  A→B : 0 + 3 = 3
  B→D : 2 + 3 = 5
  D→t : 9 + 3 = 12

α = 22 + 3 = 25


═══ ITÉRATION 7 ═══

Recherche de chaîne augmentante...

Depuis s :
  s→A : marge = 10-10 = 0 ❌ SATURÉ
  s→B : marge = 8-8 = 0   ❌ SATURÉ
  s→C : marge = 7-7 = 0   ❌ SATURÉ

→ AUCUN arc sortant de s n'a de marge
→ AUCUNE chaîne augmentante possible

═══ TERMINÉ ═══


ÉTAT FINAL :

Arc         │ Cap │ Flot │ Marge │ Saturé ?
────────────┼─────┼──────┼───────┼─────────
s → A       │  10 │  10  │   0   │ ✅
s → B       │   8 │   8  │   0   │ ✅
s → C       │   7 │   7  │   0   │ ✅
A → B       │   5 │   3  │   2   │
A → D       │   7 │   7  │   0   │ ✅
B → D       │   6 │   5  │   1   │
B → E       │   9 │   6  │   3   │
C → E       │   8 │   5  │   3   │
C → F       │   4 │   2  │   2   │
D → t       │  12 │  12  │   0   │ ✅
E → D       │   3 │   0  │   3   │
E → F       │   5 │   5  │   0   │ ✅
E → t       │   6 │   6  │   0   │ ✅
F → t       │   9 │   7  │   2   │


FLOT MAXIMAL : α = 25 m³/h

Vérification :
  Sortant de s : 10 + 8 + 7 = 25 ✅
  Entrant en t : 12 + 6 + 7 = 25 ✅
```

#### Étape 1.7 : Vérification de la conservation et coupe minimale

```
CONSERVATION AUX NŒUDS INTERMÉDIAIRES :

  A : entrant = 10(s)       | sortant = 3(B) + 7(D) = 10     ✅
  B : entrant = 8(s) + 3(A) | sortant = 5(D) + 6(E) = 11    ✅
      = 11                  |
  C : entrant = 7(s)        | sortant = 5(E) + 2(F) = 7      ✅
  D : entrant = 7(A)+5(B)+0(E) | sortant = 12(t)             ✅
      = 12                     |
  E : entrant = 6(B) + 5(C) | sortant = 0(D)+5(F)+6(t) = 11  ✅
      = 11                  |
  F : entrant = 2(C) + 5(E) | sortant = 7(t)                  ✅
      = 7                   |


COUPE MINIMALE :

  Sommets atteignables depuis s dans le graphe résiduel :
  Tous les arcs sortant de s ont marge 0
  → S = {s}
  → T = {A, B, C, D, E, F, t}

  Arcs de la coupe (S → T) :
    s→A : capacité 10
    s→B : capacité 8
    s→C : capacité 7

  Capacité de la coupe = 10 + 8 + 7 = 25

  FLOT MAX (25) = COUPE MIN (25) ✅ → OPTIMAL PROUVÉ
```

> ✅ Vérifie que tu obtiens α = 25 m³/h avant de coder.

---

### PHASE 2 — Conception (pseudo-code)

#### Étape 2.1 : Pseudo-code de Ford-Fulkerson (avec BFS = Edmonds-Karp)

```
ALGORITHME FordFulkerson

ENTRÉES :
    n             : nombre de sommets
    capacite[n][n]: matrice des capacités (0 si pas d'arc)
    s             : indice de la source
    t             : indice du puits

SORTIE :
    flot[n][n]    : matrice des flots sur chaque arc
    flot_max      : valeur du flot maximal

DÉBUT
    ── Initialisation ──
    flot ← matrice n×n de zéros
    flot_max ← 0

    ── Boucle principale ──
    TANT QUE VRAI FAIRE

        ── Chercher une chaîne augmentante par BFS ──
        parent ← BFS_chemin_augmentant(capacite, flot, s, t)

        SI parent = NULL ALORS
            SORTIR  (plus de chaîne → flot maximal atteint)
        FIN SI

        ── Calculer δ (augmentation max sur la chaîne) ──
        δ ← +∞
        v ← t
        TANT QUE v ≠ s FAIRE
            u ← parent[v]
            marge ← capacite[u][v] - flot[u][v]
            δ ← min(δ, marge)
            v ← u
        FIN TANT QUE

        ── Mettre à jour le flot ──
        v ← t
        TANT QUE v ≠ s FAIRE
            u ← parent[v]
            flot[u][v] ← flot[u][v] + δ    (arc direct : +δ)
            flot[v][u] ← flot[v][u] - δ    (arc inverse : -δ)
            v ← u
        FIN TANT QUE

        flot_max ← flot_max + δ

    FIN TANT QUE

    RETOURNER flot, flot_max
FIN
```

#### Étape 2.2 : Pseudo-code de la recherche BFS dans le graphe résiduel

```
FONCTION BFS_chemin_augmentant(capacite, flot, s, t)

ENTRÉES :
    capacite, flot : matrices n×n
    s, t           : source et puits

SORTIE :
    parent[0..n-1] : parent de chaque sommet dans le chemin
                     ou NULL si pas de chemin

DÉBUT
    visite ← [FAUX] * n
    parent ← [-1] * n
    file ← file_vide()

    visite[s] ← VRAI
    file.enfiler(s)

    TANT QUE file non vide FAIRE
        u ← file.défiler()

        POUR chaque sommet v DE 0 À n-1 FAIRE
            ── Capacité résiduelle ──
            residuel ← capacite[u][v] - flot[u][v]

            SI NON visite[v] ET residuel > 0 ALORS
                visite[v] ← VRAI
                parent[v] ← u
                file.enfiler(v)

                SI v = t ALORS
                    RETOURNER parent    (chemin trouvé !)
                FIN SI
            FIN SI
        FIN POUR
    FIN TANT QUE

    RETOURNER NULL    (pas de chemin → flot maximal)
FIN
```

#### Étape 2.3 : Pseudo-code de la coupe minimale

```
FONCTION trouver_coupe_minimale(capacite, flot, s)

DÉBUT
    ── BFS depuis s dans le graphe résiduel ──
    S ← ensemble des sommets atteignables depuis s
        (où capacite[u][v] - flot[u][v] > 0)
    T ← V \ S

    ── Arcs de la coupe ──
    arcs_coupe ← []
    capacite_coupe ← 0

    POUR chaque u ∈ S FAIRE
        POUR chaque v ∈ T FAIRE
            SI capacite[u][v] > 0 ALORS
                arcs_coupe.ajouter((u, v, capacite[u][v]))
                capacite_coupe ← capacite_coupe + capacite[u][v]
            FIN SI
        FIN POUR
    FIN POUR

    RETOURNER S, T, arcs_coupe, capacite_coupe
FIN
```

#### Étape 2.4 : Structures de données

```
1. Matrice des capacités (n×n) :
     capacite[i][j] = capacité de l'arc (i,j), 0 si pas d'arc

2. Matrice des flots (n×n) :
     flot[i][j] = flot actuel sur l'arc (i,j)
     Astuce : flot[i][j] = -flot[j][i] pour gérer les arcs inverses

3. Mapping noms ↔ indices :
     noms = ["s", "A", "B", "C", "D", "E", "F", "t"]
     indices : s=0, A=1, B=2, C=3, D=4, E=5, F=6, t=7

4. Tableau parent pour le BFS :
     parent[v] = sommet précédent dans le chemin augmentant

Complexité (Edmonds-Karp = Ford-Fulkerson avec BFS) :
  Temps : O(V × E²)
  Espace : O(V²) pour les matrices
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_flot_max/
│
├── main.py                         Programme principal
│
├── donnees.py                      Données du réseau
│   ├── noms                        Noms des stations
│   ├── descriptions                Descriptions
│   ├── capacite                    Matrice des capacités
│   ├── source                      Indice de s
│   └── puits                       Indice de t
│
├── ford_fulkerson.py               Algorithme principal
│   ├── bfs_chemin_augmentant()     BFS dans le graphe résiduel
│   ├── ford_fulkerson()            Algorithme complet
│   ├── trouver_coupe_minimale()    Coupe min après résolution
│   └── calculer_valeur_flot()      Valeur du flot courant
│
├── affichage.py                    Module affichage
│   ├── afficher_reseau()           Réseau avec capacités
│   ├── afficher_iteration()        Détail d'une itération
│   ├── afficher_etat_flot()        Tableau arc/cap/flot/marge
│   ├── afficher_coupe()            Coupe minimale
│   └── afficher_conservation()     Vérification aux nœuds
│
├── verification.py                 Vérification
│   ├── verifier_flot()             Flot admissible ?
│   ├── verifier_conservation()     Kirchhoff respecté ?
│   └── verifier_coupe()            Flot max = Coupe min ?
│
└── tests.py                        Tests unitaires
```

#### Étape 3.2 : Squelette des données

```python
# donnees.py

noms = ["s", "A", "B", "C", "D", "E", "F", "t"]

descriptions = {
    "s": "Station de pompage (Songon)",
    "A": "Jonction Yopougon Nord",
    "B": "Surpression Adjamé",
    "C": "Jonction Plateau",
    "D": "Surpression Cocody",
    "E": "Jonction Treichville",
    "F": "Jonction Koumassi",
    "t": "Réservoir terminal (Port-Bouët)",
}

#        s   A   B   C   D   E   F   t
capacite = [
    [  0, 10,  8,  7,  0,  0,  0,  0],  # s
    [  0,  0,  5,  0,  7,  0,  0,  0],  # A
    [  0,  0,  0,  0,  6,  9,  0,  0],  # B
    [  0,  0,  0,  0,  0,  8,  4,  0],  # C
    [  0,  0,  0,  0,  0,  0,  0, 12],  # D
    [  0,  0,  0,  0,  3,  0,  5,  6],  # E
    [  0,  0,  0,  0,  0,  0,  0,  9],  # F
    [  0,  0,  0,  0,  0,  0,  0,  0],  # t
]

source = 0  # s
puits = 7   # t
```

#### Étape 3.3 : Squelette des fonctions principales

```python
# ford_fulkerson.py

from collections import deque


def bfs_chemin_augmentant(capacite, flot, s, t):
    """
    Recherche un chemin augmentant de s à t par BFS
    dans le graphe résiduel.

    Args:
        capacite (list[list[int]]) : matrice des capacités n×n
        flot     (list[list[int]]) : matrice des flots n×n
        s        (int)             : indice source
        t        (int)             : indice puits

    Returns:
        list[int] ou None : tableau parent[] si chemin trouvé,
                            None sinon
    """
    # 1. Initialiser visite[], parent[], file
    # 2. Enfiler s, marquer visité
    # 3. Tant que file non vide :
    #      a. Défiler u
    #      b. Pour chaque v : si residuel(u,v) > 0 et non visité
    #           → marquer, parent[v]=u, enfiler
    #           → si v == t : retourner parent
    # 4. Retourner None (pas de chemin)
    pass


def ford_fulkerson(capacite, s, t):
    """
    Algorithme de Ford-Fulkerson (variante Edmonds-Karp avec BFS).

    Args:
        capacite (list[list[int]]) : matrice des capacités
        s        (int)             : source
        t        (int)             : puits

    Returns:
        list[list[int]] : matrice des flots
        int             : valeur du flot maximal
        list[dict]      : historique des itérations
    """
    # 1. Initialiser flot = matrice de zéros, flot_max = 0
    # 2. Tant qu'un chemin augmentant existe (BFS) :
    #      a. Remonter le chemin via parent[] pour trouver δ
    #      b. Remonter à nouveau pour mettre à jour flot
    #         flot[u][v] += δ  (direct)
    #         flot[v][u] -= δ  (inverse)
    #      c. flot_max += δ
    #      d. Sauvegarder l'itération dans l'historique
    # 3. Retourner flot, flot_max, historique
    pass


def trouver_coupe_minimale(capacite, flot, s):
    """
    Identifie la coupe minimale après résolution.

    Returns:
        set  : ensemble S (sommets côté source)
        set  : ensemble T (sommets côté puits)
        list : arcs de la coupe avec leurs capacités
        int  : capacité totale de la coupe
    """
    # BFS depuis s dans le graphe résiduel
    # S = sommets atteignables, T = les autres
    # Arcs de S vers T = coupe minimale
    pass


def calculer_valeur_flot(flot, s):
    """
    Calcule la valeur du flot = somme des flots sortant de s.
    """
    # Σ flot[s][j] pour tout j
    pass
```

#### Étape 3.4 : Affichage attendu

```
════════════════════════════════════════════════════════════════
   RÉSEAU DE DISTRIBUTION D'EAU — SODECI ABIDJAN
   Algorithme : Ford-Fulkerson (Edmonds-Karp)
════════════════════════════════════════════════════════════════

  ITÉRATION 1 :
    Chaîne : s → A → D → t
    δ = 7 m³/h
    Flot cumulé : 7 m³/h

  ITÉRATION 2 :
    Chaîne : s → B → E → t
    δ = 6 m³/h
    Flot cumulé : 13 m³/h

  ...

  ITÉRATION 6 :
    Chaîne : s → A → B → D → t
    δ = 3 m³/h
    Flot cumulé : 25 m³/h

  ITÉRATION 7 :
    Aucune chaîne augmentante → TERMINÉ

  ÉTAT FINAL :
  ┌─────────────┬─────────┬───────┬───────┬──────────┐
  │ Arc         │ Capacité│ Flot  │ Marge │ Saturé ? │
  ├─────────────┼─────────┼───────┼───────┼──────────┤
  │ s → A       │   10    │  10   │   0   │ ✅       │
  │ s → B       │    8    │   8   │   0   │ ✅       │
  │ s → C       │    7    │   7   │   0   │ ✅       │
  │ ...         │  ...    │ ...   │  ...  │ ...      │
  └─────────────┴─────────┴───────┴───────┴──────────┘

  CONSERVATION AUX NŒUDS :
  ┌────────┬───────────┬───────────┬─────────┐
  │ Nœud   │ Entrant   │ Sortant   │ OK ?    │
  ├────────┼───────────┼───────────┼─────────┤
  │ A      │ 10        │ 10        │ ✅      │
  │ B      │ 11        │ 11        │ ✅      │
  │ ...    │ ...       │ ...       │ ...     │
  └────────┴───────────┴───────────┴─────────┘

  COUPE MINIMALE :
    S = {s}
    T = {A, B, C, D, E, F, t}
    Arcs : s→A(10) + s→B(8) + s→C(7) = 25

  ┌─────────────────────────────────────────────┐
  │  FLOT MAXIMAL    : 25 m³/h                  │
  │  COUPE MINIMALE  : 25 m³/h                  │
  │  FLOT MAX = COUPE MIN ✅ → OPTIMAL PROUVÉ  │
  │  Nombre d'itérations : 6                    │
  └─────────────────────────────────────────────┘
```

#### Étape 3.5 : Règles de codage

```
1. MATRICE DES FLOTS ANTISYMÉTRIQUE
     flot[u][v] = -flot[v][u]
     Cela gère automatiquement les arcs inverses du graphe résiduel
     Capacité résiduelle = capacite[u][v] - flot[u][v]

2. NOMMER clairement
     ✅ capacite_residuelle, chemin_augmentant, delta_augmentation
     ❌ cr, ca, d

3. HISTORIQUE DES ITÉRATIONS
     Sauvegarder chaque itération :
       {"chemin": [...], "delta": 7, "flot_cumule": 7}
     Permet l'affichage de la trace et le debugging

4. SÉPARER les responsabilités
     ford_fulkerson.py  → logique pure (pas de print)
     affichage.py       → toute la présentation
     verification.py    → vérification du flot

5. VÉRIFICATION SYSTÉMATIQUE
     Après résolution, vérifier automatiquement :
       - Contraintes de capacité
       - Conservation aux nœuds
       - Flot max = Coupe min
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Données complètes (8 sommets, 14 arcs)
  Attendu : flot maximal = 25 m³/h

TEST 2 — Réseau simple (s → t direct)
  capacite = [[0,10],[0,0]]
  Attendu : flot = 10

TEST 3 — Deux chemins parallèles
  s → A → t (cap 5) et s → B → t (cap 3)
  Attendu : flot = 8

TEST 4 — Goulot d'étranglement
  s → A (cap 100) → B (cap 1) → t (cap 100)
  Attendu : flot = 1

TEST 5 — Réseau sans chemin s → t
  Attendu : flot = 0

TEST 6 — Conservation de Kirchhoff
  Vérifier sur le résultat du test 1 :
  Σ entrant = Σ sortant pour tout nœud sauf s et t

TEST 7 — Coupe minimale
  Vérifier : capacité coupe = flot max

TEST 8 — Flot nul initial
  Vérifier : tous les flots à 0 au départ
```

#### Étape 4.2 : Vérification automatique

```python
def verifier_flot(capacite, flot, s, t):
    """
    Vérifie qu'un flot est admissible.

    1. Contrainte de capacité : 0 ≤ flot[i][j] ≤ capacite[i][j]
    2. Conservation : Σ entrant = Σ sortant (sauf s et t)
    3. Valeur cohérente : flot sortant de s = flot entrant en t
    """
    pass

def verifier_optimalite(capacite, flot, s, t):
    """
    Vérifie l'optimalité via le théorème flot max = coupe min.

    1. Trouver la coupe minimale
    2. Vérifier : valeur du flot = capacité de la coupe
    """
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Visualisation du graphe résiduel

```
À chaque itération, afficher le graphe résiduel :
  - Arcs directs avec leur marge (capacite - flot)
  - Arcs inverses avec leur flot
  - Chemin augmentant en surbrillance

Avec matplotlib + networkx :
  - Nœuds colorés (source en vert, puits en rouge)
  - Arcs avec étiquettes flot/capacité
  - Animation itération par itération
```

#### Extension 2 : Lecture depuis un fichier

```
Lire le réseau depuis un fichier CSV :
  s,A,10
  s,B,8
  A,D,7
  ...

Permet de tester sur d'autres réseaux sans modifier le code.
```

#### Extension 3 : Comparaison DFS vs BFS

```
Implémenter Ford-Fulkerson avec DFS (version originale)
et avec BFS (Edmonds-Karp).

Comparer :
  - Nombre d'itérations
  - Temps d'exécution
  - Même résultat final ?

Sur des réseaux aléatoires de taille croissante.
```

#### Extension 4 : Flot à coût minimum

```
Ajouter un coût par unité de flot sur chaque arc.
Trouver le flot maximal de coût minimal.

Application : envoyer l'eau au moindre coût énergétique
(pompage, surpression).
```

#### Extension 5 : Instances aléatoires

```
Générer des réseaux aléatoires :
  - n sommets, m arcs, capacités aléatoires
  - Tester Ford-Fulkerson sur n = 10, 50, 100, 500
  - Mesurer : flot max, nb itérations, temps

Tracer les courbes de performance.
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Réseau identifié (8 sommets, 14 arcs)
  □ Définitions maîtrisées (flot, capacité, conservation, coupe)
  □ Ford-Fulkerson résolu à la main → 6 itérations, α = 25
  □ Conservation vérifiée aux 6 nœuds intermédiaires
  □ Coupe minimale identifiée : S={s}, cap=25

PHASE 2 — Conception
  □ Pseudo-code BFS dans le graphe résiduel
  □ Pseudo-code Ford-Fulkerson complet
  □ Pseudo-code coupe minimale
  □ Structures de données choisies (matrices n×n)

PHASE 3 — Implémentation
  □ donnees.py : matrice des capacités + noms
  □ bfs_chemin_augmentant() codé
  □ ford_fulkerson() codé
  □ trouver_coupe_minimale() codé
  □ calculer_valeur_flot() codé
  □ Affichage : trace des itérations + tableau final
  □ Vérification : conservation + coupe min
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 8 tests unitaires validés
  □ verifier_flot() implémenté
  □ verifier_optimalite() implémenté
  □ Flot de 25 m³/h retrouvé par le code

PHASE 5 — Extensions (bonus)
  □ Visualisation networkx + matplotlib
  □ Lecture depuis fichier CSV
  □ Comparaison DFS vs BFS
  □ Flot à coût minimum
  □ Instances aléatoires + courbes
```

---

## 📐 Rappels Théoriques

### Algorithme de Ford-Fulkerson

```
1. Initialiser flot nul
2. Tant qu'une chaîne augmentante existe (BFS) :
     δ = min des marges sur la chaîne
     Mettre à jour : +δ direct, -δ inverse
     flot_max += δ
3. Plus de chaîne → flot maximal

Variante Edmonds-Karp (BFS) : O(V × E²)
Variante DFS : O(E × flot_max) — peut ne pas terminer sur réels
```

### Théorème Flot Max = Coupe Min

```
max α(ϕ) = min c(S,T)

Preuve d'optimalité : si on trouve un flot de valeur α
ET une coupe de capacité α → le flot est maximal.
```

### Graphe résiduel

```
Pour chaque arc (u,v) avec capacité c et flot ϕ :
  → Arc direct (u,v) de capacité résiduelle c - ϕ  (si c - ϕ > 0)
  → Arc inverse (v,u) de capacité résiduelle ϕ      (si ϕ > 0)

Chemin augmentant dans le réseau original
  = Chemin de s à t dans le graphe résiduel
```

### Les deux contraintes fondamentales

```
CAPACITÉ :      0 ≤ ϕ(u,v) ≤ c(u,v)        ∀ arc (u,v)
CONSERVATION :  Σ entrant = Σ sortant        ∀ nœud ≠ s,t
```

---

*Bonne implémentation ! 💪*
