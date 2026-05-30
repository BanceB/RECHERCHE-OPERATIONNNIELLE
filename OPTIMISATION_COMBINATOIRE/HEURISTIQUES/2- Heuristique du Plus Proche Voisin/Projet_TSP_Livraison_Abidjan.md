# 🚐 Projet : Optimisation de la Tournée de Livraison

## Optimisation Combinatoire — TSP & Heuristique du Plus Proche Voisin

---

## 📖 Contexte Réel : Le Livreur de Jumia Abidjan

Ibrahim est **livreur** pour une plateforme de e-commerce à Abidjan. Chaque matin, il reçoit une liste de **12 clients** à livrer dans la journée. Il part de l'**entrepôt central** de Marcory, livre tous les clients, puis **revient à l'entrepôt**.

Son problème quotidien :

- L'essence coûte cher (prix du carburant en hausse constante)
- Les embouteillages d'Abidjan font perdre un temps énorme
- Son responsable lui demande de **minimiser la distance totale parcourue**

> **Objectif** : Trouver l'**ordre de visite optimal** des 12 clients pour que la tournée complète (départ entrepôt → tous les clients → retour entrepôt) soit la **plus courte possible**.

C'est exactement le **Problème du Voyageur de Commerce (TSP)** :
- Les **villes** = l'entrepôt + les 12 clients
- Les **distances** = kilomètres entre chaque paire de points
- Le **tour** = circuit hamiltonien de distance minimale

---

## 🎯 Cahier des Charges

### Les 13 points de livraison (entrepôt + 12 clients)

| Point | Lieu | Quartier |
|-------|------|----------|
| E | Entrepôt central | Marcory |
| A | Client Kouassi | Cocody Angré |
| B | Client Traoré | Yopougon Maroc |
| C | Client Bamba | Plateau |
| D | Client Koné | Treichville |
| F | Client Diallo | Adjamé |
| G | Client Ouattara | Abobo Gare |
| H | Client Sanogo | Cocody Riviera |
| I | Client Coulibaly | Koumassi |
| J | Client Touré | Marcory Résid. |
| K | Client Fofana | Port-Bouët |
| L | Client Diabaté | Yopougon Sicogi |
| M | Client Sylla | Deux-Plateaux |

### Matrice des distances (en km)

```
     E    A    B    C    D    F    G    H    I    J    K    L    M
E    0    8   14    5    3   10   18    9    4    2    7   16    7
A    8    0   20    9   11    7   15    3   12   10   16   22    2
B   14   20    0   17   15    8    9   22   18   16   20    4   21
C    5    9   17    0    4   11   19   10    7    6    9   18    8
D    3   11   15    4    0    9   17   12    5    3    6   17   10
F   10    7    8   11    9    0    6    9   13   11   15   10    8
G   18   15    9   19   17    6    0   17   20   19   22   11   16
H    9    3   22   10   12    9   17    0   13   11   17   24    4
I    4   12   18    7    5   13   20   13    0    3    5   19   11
J    2   10   16    6    3   11   19   11    3    0    6   17    9
K    7   16   20    9    6   15   22   17    5    6    0   21   15
L   16   22    4   18   17   10   11   24   19   17   21    0   23
M    7    2   21    8   10    8   16    4   11    9   15   23    0
```

> Problème **symétrique** : d(i,j) = d(j,i). Graphe **complet** : chaque point est relié à tous les autres.

### Informations clés

```
Nombre de points : n = 13 (entrepôt + 12 clients)
Nombre de tours possibles : (13-1)! / 2 = 239 500 800 tours
→ Impossible d'énumérer → Heuristique nécessaire

Ville de départ et d'arrivée : E (entrepôt Marcory)

Borne inférieure estimée :
  On peut l'approximer plus tard avec le MST ou la relaxation
```

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Définir les données

```
DONNÉES :

n = 13                              (nombre de points)
V = {E, A, B, C, D, F, G, H, I, J, K, L, M}

Matrice des distances :
  d[i][j] = distance en km entre le point i et le point j
  d[i][j] = d[j][i]                (symétrique)
  d[i][i] = 0                      (diagonale nulle)

Ville de départ : E (entrepôt)
```

#### Étape 1.2 : Variables de décision

```
xᵢⱼ = 1 si le livreur va directement du point i au point j
xᵢⱼ = 0 sinon

Tour = séquence ordonnée visitant chaque point exactement une fois
       puis retour au départ
```

#### Étape 1.3 : Modèle mathématique (rappel)

```
              n    n
Min Z =       Σ    Σ   dᵢⱼ · xᵢⱼ
             i=1  j=1

s.c. :
  Σⱼ xᵢⱼ = 1                    ∀ i   (quitter chaque ville 1 fois)
  Σᵢ xᵢⱼ = 1                    ∀ j   (arriver à chaque ville 1 fois)
  Élimination des sous-tours
  xᵢⱼ ∈ {0, 1}
```

#### Étape 1.4 : Principe du Plus Proche Voisin (PPV)

```
ALGORITHME PPV (Nearest Neighbor) :

1. Commencer à la ville de départ (entrepôt E)
2. Depuis la ville courante :
     → Regarder toutes les villes NON VISITÉES
     → Aller à la PLUS PROCHE
3. Répéter jusqu'à avoir visité toutes les villes
4. Revenir à la ville de départ

Critère glouton : toujours choisir la ville non visitée la plus proche
Complexité : O(n²)
Garantie : aucune (peut donner un mauvais tour)
```

#### Étape 1.5 : Résoudre à la main

```
Départ : E
Villes restantes : {A, B, C, D, F, G, H, I, J, K, L, M}

─── Étape 1 : Depuis E ───
  E→A=8, E→B=14, E→C=5, E→D=3, E→F=10, E→G=18,
  E→H=9, E→I=4, E→J=2, E→K=7, E→L=16, E→M=7

  Minimum : E→J = 2 km ✅
  Tour : [E → J]
  Restantes : {A, B, C, D, F, G, H, I, K, L, M}
  Distance cumulée : 2

─── Étape 2 : Depuis J ───
  J→A=10, J→B=16, J→C=6, J→D=3, J→F=11, J→G=19,
  J→H=11, J→I=3, J→K=6, J→L=17, J→M=9

  Minimum : J→D = 3 km et J→I = 3 km (égalité)
  On choisit D (premier dans l'ordre) ✅
  Tour : [E → J → D]
  Restantes : {A, B, C, F, G, H, I, K, L, M}
  Distance cumulée : 2 + 3 = 5

─── Étape 3 : Depuis D ───
  D→A=11, D→B=15, D→C=4, D→F=9, D→G=17,
  D→H=12, D→I=5, D→K=6, D→L=17, D→M=10

  Minimum : D→C = 4 km ✅
  Tour : [E → J → D → C]
  Distance cumulée : 5 + 4 = 9

─── Étape 4 : Depuis C ───
  C→A=9, C→B=17, C→F=11, C→G=19,
  C→H=10, C→I=7, C→K=9, C→L=18, C→M=8

  Minimum : C→I = 7 km ✅
  Tour : [E → J → D → C → I]
  Distance cumulée : 9 + 7 = 16

─── Étape 5 : Depuis I ───
  I→A=12, I→B=18, I→F=13, I→G=20,
  I→H=13, I→K=5, I→L=19, I→M=11

  Minimum : I→K = 5 km ✅
  Tour : [E → J → D → C → I → K]
  Distance cumulée : 16 + 5 = 21

─── Étape 6 : Depuis K ───
  K→A=16, K→B=20, K→F=15, K→G=22,
  K→H=17, K→L=21, K→M=15

  Minimum : K→M = 15 km et K→F = 15 km (égalité)
  On choisit F ✅
  Tour : [E → J → D → C → I → K → F]
  Distance cumulée : 21 + 15 = 36

─── Étape 7 : Depuis F ───
  F→A=7, F→B=8, F→G=6, F→H=9, F→L=10, F→M=8

  Minimum : F→G = 6 km ✅
  Tour : [E → J → D → C → I → K → F → G]
  Distance cumulée : 36 + 6 = 42

─── Étape 8 : Depuis G ───
  G→A=15, G→B=9, G→H=17, G→L=11, G→M=16

  Minimum : G→B = 9 km ✅
  Tour : [E → J → D → C → I → K → F → G → B]
  Distance cumulée : 42 + 9 = 51

─── Étape 9 : Depuis B ───
  B→A=20, B→H=22, B→L=4, B→M=21

  Minimum : B→L = 4 km ✅
  Tour : [E → J → D → C → I → K → F → G → B → L]
  Distance cumulée : 51 + 4 = 55

─── Étape 10 : Depuis L ───
  L→A=22, L→H=24, L→M=23

  Minimum : L→A = 22 km ✅
  Tour : [E → J → D → C → I → K → F → G → B → L → A]
  Distance cumulée : 55 + 22 = 77

─── Étape 11 : Depuis A ───
  A→H=3, A→M=2

  Minimum : A→M = 2 km ✅
  Tour : [E → J → D → C → I → K → F → G → B → L → A → M]
  Distance cumulée : 77 + 2 = 79

─── Étape 12 : Depuis M (dernière ville) ───
  M→H = 4 km (seule restante)
  Tour : [E → J → D → C → I → K → F → G → B → L → A → M → H]
  Distance cumulée : 79 + 4 = 83

─── Retour à l'entrepôt ───
  H→E = 9 km
  Tour final : [E → J → D → C → I → K → F → G → B → L → A → M → H → E]
  Distance totale : 83 + 9 = 92 km


RÉSULTAT PPV :
  Tour    : E → J → D → C → I → K → F → G → B → L → A → M → H → E
  Distance : 92 km
```

> ✅ Vérifie que tu obtiens exactement 92 km avant de coder.

---

### PHASE 2 — Conception (pseudo-code)

#### Étape 2.1 : Pseudo-code du Plus Proche Voisin

```
ALGORITHME PlusProchVoisin

ENTRÉES :
    n               : nombre de villes
    dist[0..n-1][0..n-1] : matrice des distances
    depart          : indice de la ville de départ

SORTIE :
    tour[0..n]      : séquence de villes (tour[n] = tour[0] = départ)
    distance_totale : longueur du tour

DÉBUT
    visite ← [FAUX, FAUX, ..., FAUX]    (n éléments)
    tour ← [depart]
    visite[depart] ← VRAI
    ville_courante ← depart
    distance_totale ← 0

    POUR étape DE 1 À n-1 FAIRE

        ── Trouver la ville non visitée la plus proche ──
        dist_min ← +∞
        ville_proche ← -1

        POUR j DE 0 À n-1 FAIRE
            SI NON visite[j] ET dist[ville_courante][j] < dist_min ALORS
                dist_min ← dist[ville_courante][j]
                ville_proche ← j
            FIN SI
        FIN POUR

        ── Se déplacer vers cette ville ──
        tour ← tour + [ville_proche]
        visite[ville_proche] ← VRAI
        distance_totale ← distance_totale + dist_min
        ville_courante ← ville_proche

    FIN POUR

    ── Retour au départ ──
    distance_totale ← distance_totale + dist[ville_courante][depart]
    tour ← tour + [depart]

    RETOURNER tour, distance_totale
FIN
```

#### Étape 2.2 : Pseudo-code de la variante multi-départs

```
ALGORITHME PPV_MultiDeparts

ENTRÉES :
    n, dist[0..n-1][0..n-1]

SORTIE :
    meilleur_tour, meilleure_distance

DÉBUT
    meilleure_distance ← +∞

    POUR chaque ville v DE 0 À n-1 FAIRE
        tour, distance ← PlusProchVoisin(n, dist, v)

        SI distance < meilleure_distance ALORS
            meilleur_tour ← tour
            meilleure_distance ← distance
        FIN SI
    FIN POUR

    RETOURNER meilleur_tour, meilleure_distance
FIN

Idée : tester TOUTES les villes de départ et garder le meilleur tour.
Complexité : O(n³) au lieu de O(n²), mais souvent bien meilleur résultat.
```

#### Étape 2.3 : Structures de données

```
1. Matrice des distances (liste de listes) :
     dist = [
       [0, 8, 14, 5, ...],    # depuis E
       [8, 0, 20, 9, ...],    # depuis A
       ...
     ]

2. Mapping noms ↔ indices :
     noms = ["E", "A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M"]
     indices : E=0, A=1, B=2, C=3, D=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12

3. Tour = liste d'indices :
     tour = [0, 9, 4, 3, 8, 10, 5, 6, 2, 11, 1, 12, 7, 0]
     → traduit en noms : E→J→D→C→I→K→F→G→B→L→A→M→H→E

4. Tableau de visite :
     visite = [True, False, True, ...]   (booléens)

Complexité :
  PPV simple       : O(n²) temps, O(n) espace
  PPV multi-départs : O(n³) temps, O(n) espace
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_tsp/
│
├── main.py                      Programme principal
│
├── donnees.py                   Données du problème
│   ├── noms                     Noms des villes
│   ├── distances                Matrice des distances
│   └── ville_depart             Indice de l'entrepôt
│
├── ppv.py                       Heuristique Plus Proche Voisin
│   ├── plus_proche_voisin()     PPV depuis un départ donné
│   ├── ppv_multi_departs()      PPV depuis toutes les villes
│   └── calculer_distance_tour() Distance totale d'un tour
│
├── affichage.py                 Module affichage
│   ├── afficher_matrice()       Matrice des distances formatée
│   ├── afficher_tour()          Tour détaillé avec distances
│   ├── afficher_trace()         Trace pas à pas du glouton
│   └── afficher_comparaison()   Comparaison des départs
│
├── verification.py              Vérification de cohérence
│   └── verifier_tour()          Tour valide ?
│
└── tests.py                     Tests unitaires
    ├── test_ppv_simple()
    ├── test_ppv_multi_departs()
    ├── test_distance_tour()
    ├── test_cas_limites()
    └── test_verification()
```

#### Étape 3.2 : Squelette des données

```python
# donnees.py — À compléter

noms = ["E", "A", "B", "C", "D", "F", "G", "H", "I", "J", "K", "L", "M"]

lieux = {
    "E": "Entrepôt Marcory",
    "A": "Client Kouassi - Cocody Angré",
    "B": "Client Traoré - Yopougon Maroc",
    "C": "Client Bamba - Plateau",
    "D": "Client Koné - Treichville",
    "F": "Client Diallo - Adjamé",
    "G": "Client Ouattara - Abobo Gare",
    "H": "Client Sanogo - Cocody Riviera",
    "I": "Client Coulibaly - Koumassi",
    "J": "Client Touré - Marcory Résid.",
    "K": "Client Fofana - Port-Bouët",
    "L": "Client Diabaté - Yopougon Sicogi",
    "M": "Client Sylla - Deux-Plateaux",
}

distances = [
    #    E   A   B   C   D   F   G   H   I   J   K   L   M
    [  0,  8, 14,  5,  3, 10, 18,  9,  4,  2,  7, 16,  7],  # E
    [  8,  0, 20,  9, 11,  7, 15,  3, 12, 10, 16, 22,  2],  # A
    [ 14, 20,  0, 17, 15,  8,  9, 22, 18, 16, 20,  4, 21],  # B
    [  5,  9, 17,  0,  4, 11, 19, 10,  7,  6,  9, 18,  8],  # C
    [  3, 11, 15,  4,  0,  9, 17, 12,  5,  3,  6, 17, 10],  # D
    [ 10,  7,  8, 11,  9,  0,  6,  9, 13, 11, 15, 10,  8],  # F
    [ 18, 15,  9, 19, 17,  6,  0, 17, 20, 19, 22, 11, 16],  # G
    [  9,  3, 22, 10, 12,  9, 17,  0, 13, 11, 17, 24,  4],  # H
    [  4, 12, 18,  7,  5, 13, 20, 13,  0,  3,  5, 19, 11],  # I
    [  2, 10, 16,  6,  3, 11, 19, 11,  3,  0,  6, 17,  9],  # J
    [  7, 16, 20,  9,  6, 15, 22, 17,  5,  6,  0, 21, 15],  # K
    [ 16, 22,  4, 18, 17, 10, 11, 24, 19, 17, 21,  0, 23],  # L
    [  7,  2, 21,  8, 10,  8, 16,  4, 11,  9, 15, 23,  0],  # M
]

ville_depart = 0  # E = entrepôt
```

#### Étape 3.3 : Squelette de la fonction PPV

```python
# ppv.py — Squelette à compléter

def plus_proche_voisin(distances, depart):
    """
    Heuristique du Plus Proche Voisin pour le TSP.

    Args:
        distances (list[list[int]]) : matrice des distances n×n
        depart    (int)             : indice de la ville de départ

    Returns:
        list[int] : tour (liste d'indices, commence et finit par depart)
        int       : distance totale du tour
    """
    n = len(distances)

    # 1. Initialiser :
    #      visite = [False] * n
    #      tour = [depart]
    #      visite[depart] = True
    #      ville_courante = depart
    #      distance_totale = 0

    # 2. Répéter n-1 fois :
    #      a. Parcourir toutes les villes j non visitées
    #      b. Trouver j* = argmin dist[ville_courante][j]
    #      c. Ajouter j* au tour
    #      d. Marquer j* comme visitée
    #      e. distance_totale += dist[ville_courante][j*]
    #      f. ville_courante = j*

    # 3. Retour au départ :
    #      distance_totale += dist[ville_courante][depart]
    #      tour.append(depart)

    # 4. Retourner tour, distance_totale
    pass


def ppv_multi_departs(distances):
    """
    PPV depuis TOUTES les villes, garde le meilleur tour.

    Returns:
        list[int] : meilleur tour
        int       : meilleure distance
        int       : ville de départ du meilleur tour
    """
    # 1. Pour chaque ville v de 0 à n-1 :
    #      tour, dist = plus_proche_voisin(distances, v)
    #      Si dist < meilleure_dist : mettre à jour
    # 2. Retourner le meilleur
    pass


def calculer_distance_tour(tour, distances):
    """
    Calcule la distance totale d'un tour donné.

    Args:
        tour      (list[int]) : séquence de villes
        distances (list[list]) : matrice

    Returns:
        int : distance totale
    """
    # Somme des dist[tour[i]][tour[i+1]] pour i de 0 à len(tour)-2
    pass
```

#### Étape 3.4 : Affichage attendu

```
══════════════════════════════════════════════════════════════
   TOURNÉE DE LIVRAISON — JUMIA ABIDJAN
   Heuristique : Plus Proche Voisin (PPV)
   Départ : E (Entrepôt Marcory)
══════════════════════════════════════════════════════════════

  Itinéraire détaillé :

  Étape  1 : E (Entrepôt Marcory)
               ↓  2 km
  Étape  2 : J (Marcory Résid.)
               ↓  3 km
  Étape  3 : D (Treichville)
               ↓  4 km
  Étape  4 : C (Plateau)
               ↓  7 km
  Étape  5 : I (Koumassi)
               ↓  5 km
  Étape  6 : K (Port-Bouët)
               ↓  15 km
  Étape  7 : F (Adjamé)
               ↓  6 km
  Étape  8 : G (Abobo Gare)
               ↓  9 km
  Étape  9 : B (Yopougon Maroc)
               ↓  4 km
  Étape 10 : L (Yopougon Sicogi)
               ↓  22 km
  Étape 11 : A (Cocody Angré)
               ↓  2 km
  Étape 12 : M (Deux-Plateaux)
               ↓  4 km
  Étape 13 : H (Cocody Riviera)
               ↓  9 km
  Retour   : E (Entrepôt Marcory)

  ┌──────────────────────────────────┐
  │  Distance totale : 92 km        │
  │  Nombre d'étapes : 13           │
  │  Villes visitées : 13/13 ✅     │
  └──────────────────────────────────┘


══════════════════════════════════════════════════════════════
   COMPARAISON MULTI-DÉPARTS
══════════════════════════════════════════════════════════════

  ┌─────────┬────────────────┬──────────────┐
  │ Départ  │ Lieu           │ Distance (km)│
  ├─────────┼────────────────┼──────────────┤
  │ E       │ Entrepôt       │    92        │
  │ A       │ Cocody Angré   │    ??        │
  │ B       │ Yopougon Maroc │    ??        │
  │ ...     │ ...            │    ??        │
  └─────────┴────────────────┴──────────────┘

  Meilleur départ : ___ avec ___ km
  Gain vs départ E : ___ km économisés
```

#### Étape 3.5 : Règles de codage

```
1. NOMMER CLAIREMENT
     ✅ ville_courante, distance_totale, ville_plus_proche
     ❌ v, d, vpp

2. MATRICE VÉRIFIÉE
     Vérifier que la matrice est symétrique : dist[i][j] == dist[j][i]
     Vérifier que la diagonale est nulle : dist[i][i] == 0

3. SÉPARER LES RESPONSABILITÉS
     ppv.py          → logique pure (pas de print)
     affichage.py    → tout l'affichage formaté
     verification.py → vérification du tour

4. TRAÇABILITÉ
     Chaque ville a un nom ET un indice
     Le tour retourné utilise des indices (efficace)
     L'affichage traduit en noms (lisible)

5. MODE TRACE OPTIONNEL
     Afficher chaque décision :
     "Depuis J : distances vers non-visitées = {D:3, I:3, C:6, ...}"
     "→ Ville choisie : D (3 km)"
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Données du cahier des charges (13 villes, départ E)
  Attendu : tour E→J→D→C→I→K→F→G→B→L→A→M→H→E, distance = 92 km

TEST 2 — Triangle simple
  dist = [[0,1,2],[1,0,3],[2,3,0]], départ = 0
  Attendu : tour [0,1,2,0], distance = 1+3+2 = 6

TEST 3 — Deux villes
  dist = [[0,5],[5,0]], départ = 0
  Attendu : tour [0,1,0], distance = 10

TEST 4 — Quatre villes en carré
  dist = [[0,1,3,2],[1,0,2,3],[3,2,0,1],[2,3,1,0]], départ = 0
  Vérifier que le PPV donne un tour valide

TEST 5 — Multi-départs (13 villes)
  Lancer PPV depuis les 13 villes
  Vérifier que le meilleur est ≤ 92 km

TEST 6 — Distance d'un tour connu
  tour = [0,1,2,...,12,0] (tour dans l'ordre)
  Vérifier : calculer_distance_tour() donne le bon total

TEST 7 — Ville unique
  dist = [[0]], départ = 0
  Attendu : tour [0,0], distance = 0

TEST 8 — Matrice invalide (non symétrique)
  Attendu : ERREUR ou WARNING
```

#### Étape 4.2 : Vérification automatique

```python
def verifier_tour(tour, n, depart):
    """
    Vérifie la validité d'un tour TSP.

    Vérifications :
      1. Le tour commence et finit par la ville de départ
      2. Chaque ville (sauf départ) apparaît exactement 1 fois
      3. Le tour a exactement n+1 éléments
      4. Tous les indices sont dans [0, n-1]

    Returns:
        bool : True si tour valide
        list[str] : erreurs éventuelles
    """
    # À CODER
    pass
```

#### Étape 4.3 : Vérification de la matrice

```python
def verifier_matrice(distances):
    """
    Vérifie que la matrice est valide pour un TSP symétrique.

    Vérifications :
      1. Matrice carrée n×n
      2. Diagonale nulle : dist[i][i] == 0
      3. Symétrique : dist[i][j] == dist[j][i]
      4. Valeurs positives : dist[i][j] >= 0

    Returns:
        bool, list[str]
    """
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Amélioration 2-opt

```
Après le PPV, améliorer le tour avec 2-opt :

Principe :
  1. Prendre le tour PPV
  2. Pour chaque paire d'arêtes (i, i+1) et (j, j+1) :
       Calculer le gain si on les inverse
       Si gain > 0 : effectuer l'échange
  3. Répéter jusqu'à aucune amélioration

Le 2-opt corrige souvent les "croisements" du tour PPV.

Pseudo-code :
  RÉPÉTER
    amélioration ← FAUX
    POUR i DE 0 À n-2 FAIRE
      POUR j DE i+2 À n-1 FAIRE
        gain = dist[tour[i]][tour[i+1]] + dist[tour[j]][tour[j+1]]
             - dist[tour[i]][tour[j]]   - dist[tour[i+1]][tour[j+1]]
        SI gain > 0 ALORS
          Inverser le segment tour[i+1 .. j]
          amélioration ← VRAI
        FIN SI
      FIN POUR
    FIN POUR
  TANT QUE amélioration

Comparer : distance PPV vs distance PPV+2opt
```

#### Extension 2 : Visualisation du tour

```
Avec matplotlib :
  1. Placer les villes comme des points sur un plan 2D
     (utiliser les coordonnées GPS approximatives des quartiers)
  2. Tracer le tour PPV en reliant les points
  3. Numéroter les étapes
  4. Colorier l'entrepôt différemment
  5. Si 2-opt fait : tracer les deux tours superposés
```

#### Extension 3 : Lecture depuis un fichier

```
Lire la matrice des distances depuis un fichier CSV :
  - Permet de changer les données sans modifier le code
  - Tester sur les instances TSPLIB (benchmarks standards)
  - Format : chaque ligne = une rangée de la matrice

Fichier distances.csv :
  0,8,14,5,3,10,18,9,4,2,7,16,7
  8,0,20,9,11,7,15,3,12,10,16,22,2
  ...
```

#### Extension 4 : Calcul de la borne inférieure (MST)

```
Calculer l'Arbre Couvrant Minimum (MST) avec Prim ou Kruskal.
Le poids du MST est une borne inférieure du TSP.

GAP = (distance_PPV - poids_MST) / poids_MST × 100%

Cela permet de mesurer la qualité du tour PPV
sans connaître la solution exacte.
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Données identifiées (13 villes, matrice 13×13)
  □ Modèle mathématique rappelé
  □ Principe du PPV compris
  □ PPV résolu à la main → tour de 92 km

PHASE 2 — Conception
  □ Pseudo-code PPV simple
  □ Pseudo-code PPV multi-départs
  □ Structures de données identifiées

PHASE 3 — Implémentation
  □ donnees.py : matrice + noms + lieux
  □ plus_proche_voisin() codé
  □ ppv_multi_departs() codé
  □ calculer_distance_tour() codé
  □ Affichage formaté de la tournée
  □ Tableau comparatif multi-départs
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 8 tests unitaires validés
  □ verifier_tour() implémenté
  □ verifier_matrice() implémenté
  □ Tour de 92 km retrouvé par le code

PHASE 5 — Extensions (bonus)
  □ Amélioration 2-opt
  □ Visualisation matplotlib
  □ Lecture depuis fichier CSV
  □ Borne inférieure MST + calcul du GAP
```

---

## 📐 Rappels Théoriques

### Algorithme du Plus Proche Voisin

```
1. Partir d'une ville de départ
2. À chaque étape : aller à la ville non visitée la plus proche
3. Quand toutes visitées : revenir au départ

Complexité : O(n²)
Optimalité : NON GARANTIE
Qualité moyenne : ~25% au-dessus de l'optimal
Pire cas : peut donner un tour O(log n) × l'optimal
```

### Modèle TSP

```
Min Σᵢ Σⱼ dᵢⱼ · xᵢⱼ
s.c. Σⱼ xᵢⱼ = 1         ∀ i
     Σᵢ xᵢⱼ = 1         ∀ j
     Élimination sous-tours
     xᵢⱼ ∈ {0, 1}

NP-difficile → (n-1)!/2 tours possibles
```

### Pourquoi le PPV peut échouer

```
Le PPV est MYOPE : il optimise localement sans anticiper.
Le dernier retour au départ coûte souvent très cher
car les villes restantes sont loin.

C'est pourquoi le multi-départs et le 2-opt
améliorent significativement le résultat.
```

---

*Bonne implémentation ! 💪*
