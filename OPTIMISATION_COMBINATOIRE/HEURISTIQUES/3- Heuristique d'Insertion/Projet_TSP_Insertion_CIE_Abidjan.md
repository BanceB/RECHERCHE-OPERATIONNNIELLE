# 🚑 Projet : Optimisation de la Tournée d'un Technicien de Maintenance

## Optimisation Combinatoire — TSP & Heuristiques d'Insertion

---

## 📖 Contexte Réel : Technicien CIE — Maintenance du Réseau Électrique

Dramane est **technicien de maintenance** à la CIE (Compagnie Ivoirienne d'Électricité). Chaque matin, il reçoit la liste des **10 transformateurs** en panne sur le réseau d'Abidjan. Il part du **dépôt technique** de Marcory, intervient sur chaque transformateur, puis **revient au dépôt**.

Les pannes d'électricité impactent des milliers de foyers. Plus la tournée est courte, plus les interventions sont rapides et plus les habitants retrouvent le courant vite.

Son responsable lui demande :

> **« Trouve l'itinéraire le plus court pour visiter les 10 transformateurs et revenir au dépôt. Chaque minute compte. »**

C'est un **Problème du Voyageur de Commerce (TSP)** résolu par **heuristiques d'insertion** :
- On construit un **sous-tour initial** avec 2 ou 3 sites
- On **insère** les sites restants un par un dans le tour
- À chaque insertion, on choisit **quel site** insérer et **où** le placer

---

## 🎯 Cahier des Charges

### Les 11 sites d'intervention (dépôt + 10 transformateurs)

| Site | Localisation | Zone |
|------|-------------|------|
| D | Dépôt technique | Marcory |
| T1 | Transformateur Cocody Angré | Cocody |
| T2 | Transformateur Yopougon Maroc | Yopougon |
| T3 | Transformateur Plateau Centre | Plateau |
| T4 | Transformateur Treichville Gare | Treichville |
| T5 | Transformateur Adjamé Liberté | Adjamé |
| T6 | Transformateur Abobo Baoulé | Abobo |
| T7 | Transformateur Koumassi Remblai | Koumassi |
| T8 | Transformateur Port-Bouët Phare | Port-Bouët |
| T9 | Transformateur Riviera Palmeraie | Cocody |
| T10 | Transformateur Yopougon Sicogi | Yopougon |

### Matrice des distances (en km)

```
       D    T1   T2   T3   T4   T5   T6   T7   T8   T9   T10
D      0     9   15    5    3   11   19    4    8   10   17
T1     9     0   21   10   12    8   16    13   18    3   23
T2    15    21    0   18   16    9   10   19   22   22    5
T3     5    10   18    0    4   12   20    7   10   11   19
T4     3    12   16    4    0   10   18    5    7   13   18
T5    11     8    9   12   10    0    7   14   17    9   11
T6    19    16   10   20   18    7    0   21   24   17   12
T7     4    13   19    7    5   14   21    0    4   14   21
T8     8    18   22   10    7   17   24    4    0   19   24
T9    10     3   22   11   13    9   17   14   19    0   24
T10   17    23    5   19   18   11   12   21   24   24    0
```

> Problème **symétrique** : d(i,j) = d(j,i). Graphe **complet**.

### Informations clés

```
Nombre de sites : n = 11
Tours possibles : (11-1)! / 2 = 1 814 400
Site de départ et d'arrivée : D (dépôt Marcory)
```

### Les 3 heuristiques d'insertion à implémenter

| Heuristique | Critère de SÉLECTION | Critère d'INSERTION |
|-------------|---------------------|---------------------|
| **Insertion la plus proche** | Site le plus PROCHE du tour | Position qui augmente le MOINS la distance |
| **Insertion la plus lointaine** | Site le plus ÉLOIGNÉ du tour | Position qui augmente le MOINS la distance |
| **Insertion la moins coûteuse** | Site dont le COÛT d'insertion est MINIMAL | Position qui augmente le MOINS la distance |

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Comprendre le mécanisme d'insertion

```
PRINCIPE GÉNÉRAL DES HEURISTIQUES D'INSERTION :

1. INITIALISATION : créer un sous-tour avec 2 ou 3 sites
   Tour initial : [D, v₁, D]  (dépôt → un site → retour dépôt)

2. SÉLECTION : choisir quel site insérer ensuite
   → Critère variable selon l'heuristique (proche, lointain, moins coûteux)

3. INSERTION : trouver la MEILLEURE POSITION dans le tour actuel
   Pour chaque arête (i, j) du tour :
     Calculer le coût d'insertion :
     Δ(i, v, j) = d(i,v) + d(v,j) - d(i,j)
   Insérer à la position qui minimise Δ

4. RÉPÉTER les étapes 2-3 jusqu'à ce que tous les sites soient insérés
```

#### Étape 1.2 : Formule du coût d'insertion

```
Quand on insère le site v entre les sites i et j dans le tour :

  AVANT :  ... → i → j → ...        distance = d(i,j)
  APRÈS :  ... → i → v → j → ...    distance = d(i,v) + d(v,j)

  Coût d'insertion = Δ(i, v, j) = d(i,v) + d(v,j) - d(i,j)

  Δ > 0 signifie que la distance augmente (toujours le cas sauf inégalité triangulaire violée)
  On cherche la position (i,j) qui minimise Δ
```

#### Étape 1.3 : Les 3 critères de sélection

```
À chaque itération, il reste des sites non encore dans le tour.
Soit T l'ensemble des sites dans le tour, et R les sites restants.

INSERTION LA PLUS PROCHE :
  Sélectionner v* = argmin { min d(v, u) }  pour v ∈ R, u ∈ T
                     v∈R     u∈T
  → Le site restant dont la distance minimale au tour est la plus petite

INSERTION LA PLUS LOINTAINE :
  Sélectionner v* = argmax { min d(v, u) }  pour v ∈ R, u ∈ T
                     v∈R     u∈T
  → Le site restant dont la distance minimale au tour est la plus grande

INSERTION LA MOINS COÛTEUSE :
  Sélectionner v* = argmin { min Δ(i, v, j) }  pour v ∈ R, (i,j) arêtes de T
                     v∈R    (i,j)∈T
  → Le site dont le meilleur coût d'insertion est le plus faible
```

#### Étape 1.4 : Modèle mathématique (rappel TSP)

```
              n    n
Min Z =       Σ    Σ   dᵢⱼ · xᵢⱼ
             i=1  j=1

s.c. :
  Σⱼ xᵢⱼ = 1       ∀ i   (quitter chaque site 1 fois)
  Σᵢ xᵢⱼ = 1       ∀ j   (arriver à chaque site 1 fois)
  Élimination des sous-tours
  xᵢⱼ ∈ {0, 1}
```

#### Étape 1.5 : Résoudre l'Insertion la Plus Proche à la main

```
═══ INITIALISATION ═══

Départ : D (indice 0)
Site le plus proche de D : T4 (d=3)
Sous-tour initial : [D → T4 → D], distance = 3 + 3 = 6
Sites restants : {T1, T2, T3, T5, T6, T7, T8, T9, T10}


═══ ITÉRATION 1 — SÉLECTION ═══

Distance minimale de chaque site restant au tour {D, T4} :

  T1 : min(d(T1,D), d(T1,T4)) = min(9, 12) = 9
  T2 : min(d(T2,D), d(T2,T4)) = min(15, 16) = 15
  T3 : min(d(T3,D), d(T3,T4)) = min(5, 4) = 4
  T5 : min(d(T5,D), d(T5,T4)) = min(11, 10) = 10
  T6 : min(d(T6,D), d(T6,T4)) = min(19, 18) = 18
  T7 : min(d(T7,D), d(T7,T4)) = min(4, 5) = 4
  T8 : min(d(T8,D), d(T8,T4)) = min(8, 7) = 7
  T9 : min(d(T9,D), d(T9,T4)) = min(10, 13) = 10
  T10: min(d(T10,D), d(T10,T4)) = min(17, 18) = 17

  Minimum global : T3 et T7 ex-aequo à 4. On prend T3.

═══ ITÉRATION 1 — INSERTION ═══

Tour actuel : [D → T4 → D] (2 arêtes)

Position 1 : insérer T3 entre D et T4
  Δ = d(D,T3) + d(T3,T4) - d(D,T4) = 5 + 4 - 3 = 6

Position 2 : insérer T3 entre T4 et D
  Δ = d(T4,T3) + d(T3,D) - d(T4,D) = 4 + 5 - 3 = 6

  Égalité. On prend position 1.

Tour : [D → T3 → T4 → D], distance = 6 + 6 = 12
Restants : {T1, T2, T5, T6, T7, T8, T9, T10}


═══ ITÉRATION 2 — SÉLECTION ═══

Distance minimale au tour {D, T3, T4} :

  T1 : min(9, 10, 12) = 9
  T2 : min(15, 18, 16) = 15
  T5 : min(11, 12, 10) = 10
  T6 : min(19, 20, 18) = 18
  T7 : min(4, 7, 5) = 4     ← MINIMUM
  T8 : min(8, 10, 7) = 7
  T9 : min(10, 11, 13) = 10
  T10: min(17, 19, 18) = 17

  → Sélection : T7 (distance minimale = 4)

═══ ITÉRATION 2 — INSERTION ═══

Tour actuel : [D → T3 → T4 → D] (3 arêtes)

Position 1 : entre D et T3
  Δ = d(D,T7) + d(T7,T3) - d(D,T3) = 4 + 7 - 5 = 6

Position 2 : entre T3 et T4
  Δ = d(T3,T7) + d(T7,T4) - d(T3,T4) = 7 + 5 - 4 = 8

Position 3 : entre T4 et D
  Δ = d(T4,T7) + d(T7,D) - d(T4,D) = 5 + 4 - 3 = 6

  Minimum : positions 1 et 3 ex-aequo (Δ=6). On prend position 3.

Tour : [D → T3 → T4 → T7 → D], distance = 12 + 6 = 18
Restants : {T1, T2, T5, T6, T8, T9, T10}


═══ ITÉRATIONS 3 à 9 — À COMPLÉTER ═══

Continue le même processus :
  1. Calculer la distance minimale de chaque site restant au tour
  2. Sélectionner le plus proche
  3. Tester toutes les positions d'insertion
  4. Insérer à la position de coût minimal
  5. Mettre à jour le tour et la distance

Le résultat final sera ton tour complet et sa distance.
Tu dois trouver le même résultat avec ton code.
```

> ✅ Continue ce calcul à la main pour les itérations 3 à 9 avant de coder.

---

### PHASE 2 — Conception (pseudo-code)

#### Étape 2.1 : Pseudo-code de l'Insertion la Plus Proche

```
ALGORITHME InsertionPlusProche

ENTRÉES :
    n               : nombre de sites
    dist[0..n-1][0..n-1] : matrice des distances
    depart          : indice du dépôt

SORTIE :
    tour            : liste des sites dans l'ordre
    distance_totale : longueur du tour

DÉBUT
    ── Phase 1 : Initialisation ──
    v1 ← site le plus proche de depart
    tour ← [depart, v1, depart]
    dans_tour ← {depart, v1}
    restants ← V \ dans_tour
    distance_totale ← 2 × dist[depart][v1]

    ── Phase 2 : Insertions successives ──
    TANT QUE restants ≠ ∅ FAIRE

        ── SÉLECTION : site le plus proche du tour ──
        dist_min_globale ← +∞
        site_choisi ← -1

        POUR chaque v ∈ restants FAIRE
            dist_au_tour ← +∞
            POUR chaque u ∈ dans_tour FAIRE
                SI dist[v][u] < dist_au_tour ALORS
                    dist_au_tour ← dist[v][u]
                FIN SI
            FIN POUR
            SI dist_au_tour < dist_min_globale ALORS
                dist_min_globale ← dist_au_tour
                site_choisi ← v
            FIN SI
        FIN POUR

        ── INSERTION : meilleure position ──
        meilleur_delta ← +∞
        meilleure_pos ← -1

        POUR k DE 0 À |tour|-2 FAIRE
            i ← tour[k]
            j ← tour[k+1]
            delta ← dist[i][site_choisi] + dist[site_choisi][j] - dist[i][j]
            SI delta < meilleur_delta ALORS
                meilleur_delta ← delta
                meilleure_pos ← k + 1
            FIN SI
        FIN POUR

        ── Insérer le site ──
        tour.inserer(meilleure_pos, site_choisi)
        dans_tour.ajouter(site_choisi)
        restants.retirer(site_choisi)
        distance_totale ← distance_totale + meilleur_delta

    FIN TANT QUE

    RETOURNER tour, distance_totale
FIN
```

#### Étape 2.2 : Pseudo-code de l'Insertion la Plus Lointaine

```
ALGORITHME InsertionPlusLointaine

  ── Seule différence avec InsertionPlusProche : la SÉLECTION ──

  ── SÉLECTION : site le plus LOINTAIN du tour ──
  dist_max_globale ← -∞
  site_choisi ← -1

  POUR chaque v ∈ restants FAIRE
      dist_au_tour ← +∞
      POUR chaque u ∈ dans_tour FAIRE
          SI dist[v][u] < dist_au_tour ALORS
              dist_au_tour ← dist[v][u]
          FIN SI
      FIN POUR
      SI dist_au_tour > dist_max_globale ALORS    ← MAX au lieu de MIN
          dist_max_globale ← dist_au_tour
          site_choisi ← v
      FIN SI
  FIN POUR

  ── INSERTION : identique (meilleure position) ──

  Intuition : insérer d'abord les sites éloignés donne un tour
  "enveloppe" plus stable. Les sites proches se glissent ensuite
  facilement sans trop augmenter la distance.
```

#### Étape 2.3 : Pseudo-code de l'Insertion la Moins Coûteuse

```
ALGORITHME InsertionMoinsCouteuse

  ── SÉLECTION + INSERTION combinées ──

  meilleur_delta_global ← +∞
  site_choisi ← -1
  meilleure_pos ← -1

  POUR chaque v ∈ restants FAIRE
      POUR k DE 0 À |tour|-2 FAIRE
          i ← tour[k]
          j ← tour[k+1]
          delta ← dist[i][v] + dist[v][j] - dist[i][j]
          SI delta < meilleur_delta_global ALORS
              meilleur_delta_global ← delta
              site_choisi ← v
              meilleure_pos ← k + 1
          FIN SI
      FIN POUR
  FIN POUR

  ── On a trouvé simultanément QUEL site et OÙ l'insérer ──
  tour.inserer(meilleure_pos, site_choisi)

  Note : cette heuristique est plus coûteuse en calcul O(n² × |tour|)
  mais donne souvent les meilleurs résultats.
```

#### Étape 2.4 : Factorisation du code

```
Les 3 heuristiques partagent la même structure :

  INITIALISER le sous-tour
  TANT QUE restants ≠ ∅ :
      SÉLECTIONNER un site        ← SEULE DIFFÉRENCE
      TROUVER la meilleure position d'insertion
      INSÉRER

On peut factoriser avec une fonction générique :

  def insertion_generique(distances, depart, critere_selection):
      ...
      site = critere_selection(restants, tour, distances)
      ...

  Où critere_selection est :
    - selection_plus_proche()
    - selection_plus_lointaine()
    - selection_moins_couteuse()
```

#### Étape 2.5 : Structures de données

```
1. Tour = liste ordonnée d'indices
     tour = [0, 3, 4, 7, 0]  (D→T3→T4→T7→D)

2. Ensemble des sites dans le tour
     dans_tour = {0, 3, 4, 7}

3. Ensemble des sites restants
     restants = {1, 2, 5, 6, 8, 9, 10}

4. Matrice des distances
     dist[i][j] = distance entre site i et site j

Complexité :
  Insertion proche/lointaine : O(n² × n) = O(n³)
  Insertion moins coûteuse   : O(n² × n) = O(n³)
  Toutes les variantes sont en O(n³)
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_tsp_insertion/
│
├── main.py                         Programme principal
│
├── donnees.py                      Données du problème
│   ├── noms                        Noms des sites
│   ├── lieux                       Descriptions des sites
│   ├── distances                   Matrice 11×11
│   └── site_depart                 Indice du dépôt
│
├── insertion.py                    Les 3 heuristiques
│   ├── insertion_plus_proche()
│   ├── insertion_plus_lointaine()
│   ├── insertion_moins_couteuse()
│   ├── _trouver_meilleure_position()   (utilitaire interne)
│   └── calculer_distance_tour()
│
├── affichage.py                    Module affichage
│   ├── afficher_tour_detaille()    Itinéraire pas à pas
│   ├── afficher_trace_insertion()  Trace de chaque insertion
│   └── afficher_comparaison()      Tableau des 3 méthodes
│
├── verification.py                 Vérification
│   ├── verifier_tour()
│   └── verifier_matrice()
│
└── tests.py                        Tests unitaires
```

#### Étape 3.2 : Squelette des données

```python
# donnees.py

noms = ["D", "T1", "T2", "T3", "T4", "T5",
        "T6", "T7", "T8", "T9", "T10"]

lieux = {
    "D":   "Dépôt technique Marcory",
    "T1":  "Transfo Cocody Angré",
    "T2":  "Transfo Yopougon Maroc",
    "T3":  "Transfo Plateau Centre",
    "T4":  "Transfo Treichville Gare",
    "T5":  "Transfo Adjamé Liberté",
    "T6":  "Transfo Abobo Baoulé",
    "T7":  "Transfo Koumassi Remblai",
    "T8":  "Transfo Port-Bouët Phare",
    "T9":  "Transfo Riviera Palmeraie",
    "T10": "Transfo Yopougon Sicogi",
}

distances = [
    #    D   T1   T2   T3   T4   T5   T6   T7   T8   T9  T10
    [  0,  9,  15,  5,  3,  11,  19,  4,   8,  10,  17],  # D
    [  9,  0,  21, 10, 12,   8,  16, 13,  18,   3,  23],  # T1
    [ 15, 21,   0, 18, 16,   9,  10, 19,  22,  22,   5],  # T2
    [  5, 10,  18,  0,  4,  12,  20,  7,  10,  11,  19],  # T3
    [  3, 12,  16,  4,  0,  10,  18,  5,   7,  13,  18],  # T4
    [ 11,  8,   9, 12, 10,   0,   7, 14,  17,   9,  11],  # T5
    [ 19, 16,  10, 20, 18,   7,   0, 21,  24,  17,  12],  # T6
    [  4, 13,  19,  7,  5,  14,  21,  0,   4,  14,  21],  # T7
    [  8, 18,  22, 10,  7,  17,  24,  4,   0,  19,  24],  # T8
    [ 10,  3,  22, 11, 13,   9,  17, 14,  19,   0,  24],  # T9
    [ 17, 23,   5, 19, 18,  11,  12, 21,  24,  24,   0],  # T10
]

site_depart = 0  # D = dépôt
```

#### Étape 3.3 : Squelette de la fonction utilitaire d'insertion

```python
def _trouver_meilleure_position(tour, site, distances):
    """
    Trouve la position dans le tour qui minimise le coût d'insertion.

    Args:
        tour      (list[int]) : tour actuel [d, ..., d]
        site      (int)       : indice du site à insérer
        distances (list[list]) : matrice des distances

    Returns:
        int   : indice de la position d'insertion dans le tour
        float : coût delta de l'insertion
    """
    # Pour chaque arête (tour[k], tour[k+1]) du tour :
    #   delta = dist[tour[k]][site] + dist[site][tour[k+1]] - dist[tour[k]][tour[k+1]]
    #   Garder la position avec le delta minimal
    # Retourner (position, delta)
    pass
```

#### Étape 3.4 : Squelettes des 3 heuristiques

```python
def insertion_plus_proche(distances, depart):
    """
    Heuristique d'insertion la plus proche.
    Sélection : site restant le plus PROCHE du tour.
    Insertion : position qui minimise le coût delta.

    Args:
        distances (list[list[int]]) : matrice n×n
        depart    (int)             : indice du site de départ

    Returns:
        list[int] : tour complet
        int       : distance totale
    """
    # 1. Initialiser : tour = [depart, plus_proche_de_depart, depart]
    # 2. Tant que restants non vide :
    #      a. Pour chaque site restant : calculer dist min au tour
    #      b. Sélectionner celui avec la dist min la plus petite
    #      c. Trouver la meilleure position d'insertion
    #      d. Insérer, mettre à jour tour et distance
    # 3. Retourner tour, distance_totale
    pass


def insertion_plus_lointaine(distances, depart):
    """
    Heuristique d'insertion la plus lointaine.
    Sélection : site restant le plus ÉLOIGNÉ du tour.
    Insertion : position qui minimise le coût delta.

    Même structure que insertion_plus_proche,
    seul le critère de sélection change (MAX au lieu de MIN).
    """
    # Même logique, mais sélectionner le site avec
    # la distance minimale au tour la plus GRANDE
    pass


def insertion_moins_couteuse(distances, depart):
    """
    Heuristique d'insertion la moins coûteuse.
    Sélection + Insertion combinées :
    Choisir le couple (site, position) qui minimise le delta global.

    Pour chaque site restant ET chaque position possible :
      calculer delta
    Prendre le (site, position) avec le plus petit delta.
    """
    # Double boucle : pour chaque site restant × chaque arête du tour
    # Garder le triplet (site, position, delta) minimal
    pass


def calculer_distance_tour(tour, distances):
    """
    Calcule la distance totale d'un tour.
    """
    # Somme de dist[tour[i]][tour[i+1]] pour i de 0 à len(tour)-2
    pass
```

#### Étape 3.5 : Affichage attendu

```
══════════════════════════════════════════════════════════════════
   TOURNÉE DE MAINTENANCE CIE — RÉSEAU ÉLECTRIQUE ABIDJAN
   Heuristique : Insertion la Plus Proche
   Départ : D (Dépôt Marcory)
══════════════════════════════════════════════════════════════════

  Trace des insertions :

  Init   : [D → T4 → D]                              dist = 6
  Ins. 1 : + T3 entre D et T4          Δ = 6         dist = 12
  Ins. 2 : + T7 entre T4 et D          Δ = 6         dist = 18
  Ins. 3 : + T8 entre T7 et D          Δ = 4         dist = 22
  ...
  Ins. 9 : + T6 entre ...              Δ = ?         dist = ??

  Itinéraire final :

  D → ... → ... → ... → D

  ┌──────────────────────────────────────────────┐
  │  Distance totale : ?? km                     │
  │  Sites visités   : 11/11 ✅                  │
  └──────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════
   COMPARAISON DES 3 HEURISTIQUES D'INSERTION
══════════════════════════════════════════════════════════════════

  ┌────────────────────────┬──────────────┬──────────────┐
  │ Heuristique            │ Distance (km)│ Nb insertions│
  ├────────────────────────┼──────────────┼──────────────┤
  │ Insertion plus proche  │     ??       │      9       │
  │ Insertion plus lointaine│    ??       │      9       │
  │ Insertion moins coûteuse│    ??       │      9       │
  └────────────────────────┴──────────────┴──────────────┘

  Meilleure heuristique : _______________
```

#### Étape 3.6 : Règles de codage

```
1. FACTORISER le code
     Les 3 heuristiques partagent : initialisation + insertion
     Seule la sélection change
     → Utiliser une fonction utilitaire _trouver_meilleure_position()

2. NOMMER clairement
     ✅ site_selectionne, cout_insertion, meilleure_position
     ❌ s, c, p

3. TRACER chaque insertion
     Afficher : "Insertion de T3 entre D et T4, Δ=6, tour=[D,T3,T4,D]"

4. SÉPARER les responsabilités
     insertion.py    → logique pure (pas de print)
     affichage.py    → affichage et trace
     verification.py → vérification du tour

5. INTERFACE COMMUNE
     Même signature pour les 3 fonctions :
     heuristique(distances, depart) → (tour, distance)
     → Permet la comparaison dans une boucle
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Insertion plus proche, données complètes
  Entrée : 11 sites, départ D
  Vérifier : tour valide, 2 premières insertions = T3 puis T7

TEST 2 — Triangle simple
  dist = [[0,1,2],[1,0,3],[2,3,0]], départ = 0
  Attendu : tour [0,1,2,0], distance = 6

TEST 3 — Deux sites
  dist = [[0,5],[5,0]], départ = 0
  Attendu : tour [0,1,0], distance = 10

TEST 4 — Carré parfait
  dist = [[0,1,2,1],[1,0,1,2],[2,1,0,1],[1,2,1,0]]
  Vérifier : les 3 heuristiques donnent distance = 4

TEST 5 — Cohérence des 3 heuristiques
  Les 3 tours sont valides (vérification automatique)
  Les 3 distances sont ≥ 0

TEST 6 — Coût d'insertion (fonction utilitaire)
  Tour = [0,3,4,0], insérer site 7
  Vérifier : delta calculé correctement pour chaque position

TEST 7 — Meilleure position d'insertion
  Tour = [0,1,2,0], insérer site 3
  Vérifier que la position retournée minimise bien le delta

TEST 8 — Comparaison avec PPV
  Lancer PPV et les 3 insertions sur les mêmes données
  L'insertion donne-t-elle un meilleur tour ?
```

#### Étape 4.2 : Vérification automatique

```python
def verifier_tour(tour, n, depart):
    """
    Vérifie :
      1. Tour commence et finit par depart
      2. Chaque site apparaît exactement 1 fois (sauf depart : 2 fois)
      3. Tour a n+1 éléments
      4. Tous les indices dans [0, n-1]
    """
    pass

def verifier_matrice(distances):
    """
    Vérifie :
      1. Carrée n×n
      2. Diagonale nulle
      3. Symétrique
      4. Valeurs ≥ 0
    """
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Comparaison avec le PPV

```
Implémenter aussi le Plus Proche Voisin (PPV) sur les mêmes données.
Comparer les 4 heuristiques :
  - PPV (départ D)
  - Insertion plus proche
  - Insertion plus lointaine
  - Insertion moins coûteuse

Tableau comparatif + analyse : laquelle est la meilleure ?
```

#### Extension 2 : Amélioration 2-opt

```
Appliquer le 2-opt sur chacun des tours obtenus.
Comparer : distance AVANT et APRÈS 2-opt pour chaque heuristique.

Quel tour initial profite le plus du 2-opt ?
```

#### Extension 3 : Visualisation graphique

```
Avec matplotlib :
  1. Placer les sites sur un plan 2D
  2. Tracer les 3 tours d'insertion en couleurs différentes
  3. Animation : montrer les insertions successives
  4. Légende avec les distances de chaque tour
```

#### Extension 4 : Initialisation alternative

```
Tester différentes initialisations :
  a) Tour initial [D, plus_proche, D]  (standard)
  b) Tour initial [D, plus_lointain, D]
  c) Tour initial avec 3 sites (triangle le plus grand)

Comparer l'impact de l'initialisation sur le résultat final.
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Mécanisme d'insertion compris (sélection + position)
  □ Formule du coût Δ(i,v,j) = d(i,v) + d(v,j) - d(i,j) maîtrisée
  □ Différence entre les 3 critères de sélection claire
  □ Insertion plus proche résolue à la main (2 premières itérations)
  □ Itérations 3 à 9 complétées à la main

PHASE 2 — Conception
  □ Pseudo-code insertion plus proche
  □ Pseudo-code insertion plus lointaine
  □ Pseudo-code insertion moins coûteuse
  □ Factorisation identifiée (utilitaire commun)
  □ Structures de données choisies

PHASE 3 — Implémentation
  □ donnees.py : matrice + noms + lieux
  □ _trouver_meilleure_position() codé
  □ insertion_plus_proche() codé
  □ insertion_plus_lointaine() codé
  □ insertion_moins_couteuse() codé
  □ calculer_distance_tour() codé
  □ Affichage : trace des insertions + itinéraire final
  □ Tableau comparatif des 3 méthodes
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 8 tests unitaires validés
  □ verifier_tour() implémenté
  □ verifier_matrice() implémenté
  □ Les 3 heuristiques donnent des tours valides

PHASE 5 — Extensions (bonus)
  □ Comparaison avec PPV (4 heuristiques)
  □ Amélioration 2-opt sur chaque tour
  □ Visualisation matplotlib
  □ Initialisations alternatives testées
```

---

## 📐 Rappels Théoriques

### Formule du coût d'insertion

```
Δ(i, v, j) = d(i,v) + d(v,j) - d(i,j)

Insérer v entre i et j :
  AVANT :  i ────────→ j           coût = d(i,j)
  APRÈS :  i ───→ v ───→ j         coût = d(i,v) + d(v,j)
  DELTA :  Δ = d(i,v) + d(v,j) - d(i,j)
```

### Comparaison des 3 insertions

```
INSERTION PLUS PROCHE :
  + Simple, intuitive
  + Bonne pour les instances denses
  - Peut négliger les sites éloignés → mauvais retour final
  Qualité : ~15% au-dessus de l'optimal en moyenne

INSERTION PLUS LOINTAINE :
  + Crée un "squelette" large du tour dès le début
  + Souvent meilleure que l'insertion proche
  - Contre-intuitive
  Qualité : ~10-12% au-dessus de l'optimal en moyenne

INSERTION MOINS COÛTEUSE :
  + Minimise directement l'augmentation de distance
  + Souvent la meilleure des 3
  - Plus coûteuse en calcul
  Qualité : ~8-10% au-dessus de l'optimal en moyenne
```

### Complexité

```
  Insertion proche      : O(n³)
  Insertion lointaine   : O(n³)
  Insertion moins coûteuse : O(n³)
  Toutes meilleures que le PPV (~25% au-dessus) en qualité moyenne
```

---

*Bonne implémentation ! 💪*
