# 📅 Projet : Planification des Examens Universitaires

## Optimisation Combinatoire — Coloration de Graphe & Algorithme de Welsh et Powell

---

## 📖 Contexte Réel : Le Service de Scolarité de l'Université d'Abidjan

Mme Konaté est **responsable de la planification des examens** à l'Université Félix Houphouët-Boigny d'Abidjan. La session d'examens approche et elle doit organiser **12 épreuves** sur un minimum de créneaux horaires.

Le problème : certains étudiants sont inscrits dans **plusieurs matières à la fois** (double licence, options croisées, UE libres). Deux examens qui partagent au moins un étudiant **ne peuvent pas avoir lieu en même temps**, sinon cet étudiant ne pourra pas passer les deux.

Chaque créneau supplémentaire coûte cher : location de salles, surveillance, logistique. Mme Konaté doit donc utiliser le **minimum de créneaux** possible.

> **Objectif** : Affecter un **créneau horaire** à chaque examen de sorte que **deux examens ayant des étudiants communs** ne soient jamais au même créneau, en utilisant le **minimum de créneaux**.

C'est exactement un **Problème de Coloration de Graphe** :
- Les **sommets** = les examens
- Les **arêtes** = les conflits (étudiants en commun)
- Les **couleurs** = les créneaux horaires
- L'**objectif** = minimiser le nombre de couleurs = χ(G)

---

## 🎯 Cahier des Charges

### Les 12 examens à planifier

| Examen | Matière | Filière |
|--------|---------|---------|
| E1 | Mathématiques I | Maths-Info |
| E2 | Algorithmique | Informatique |
| E3 | Physique Générale | Physique |
| E4 | Anglais Scientifique | Toutes filières |
| E5 | Statistiques | Maths-Éco |
| E6 | Bases de Données | Informatique |
| E7 | Mécanique | Physique-Méca |
| E8 | Économie Générale | Éco-Gestion |
| E9 | Programmation C | Informatique |
| E10 | Algèbre Linéaire | Maths |
| E11 | Électronique | Physique-Élec |
| E12 | Droit Commercial | Éco-Droit |

### Les conflits entre examens (étudiants en commun)

```
E1  — E2    (étudiants Maths-Info inscrits aux deux)
E1  — E4    (Anglais obligatoire pour les Maths)
E1  — E5    (étudiants Maths-Éco en commun)
E1  — E10   (Maths I et Algèbre : même filière)
E2  — E4    (Anglais obligatoire pour les Info)
E2  — E6    (étudiants Informatique en commun)
E2  — E9    (Algo et Prog C : même filière)
E3  — E4    (Anglais obligatoire pour les Physique)
E3  — E7    (étudiants Physique en commun)
E3  — E11   (Physique et Électronique : options croisées)
E4  — E5    (Anglais et Stats : étudiants Éco)
E4  — E8    (Anglais obligatoire pour Éco)
E5  — E8    (étudiants Éco en commun)
E5  — E10   (étudiants Maths en commun)
E6  — E9    (BDD et Prog C : même filière)
E7  — E11   (Méca et Électronique : options croisées)
E8  — E12   (étudiants Éco en commun)
```

### Matrice d'adjacence (1 = conflit, 0 = pas de conflit)

```
      E1  E2  E3  E4  E5  E6  E7  E8  E9  E10 E11 E12
E1  [  0   1   0   1   1   0   0   0   0   1   0   0 ]
E2  [  1   0   0   1   0   1   0   0   1   0   0   0 ]
E3  [  0   0   0   1   0   0   1   0   0   0   1   0 ]
E4  [  1   1   1   0   1   0   0   1   0   0   0   0 ]
E5  [  1   0   0   1   0   0   0   1   0   1   0   0 ]
E6  [  0   1   0   0   0   0   0   0   1   0   0   0 ]
E7  [  0   0   1   0   0   0   0   0   0   0   1   0 ]
E8  [  0   0   0   1   1   0   0   0   0   0   0   1 ]
E9  [  0   1   0   0   0   1   0   0   0   0   0   0 ]
E10 [  1   0   0   0   1   0   0   0   0   0   0   0 ]
E11 [  0   0   1   0   0   0   1   0   0   0   0   0 ]
E12 [  0   0   0   0   0   0   0   1   0   0   0   0 ]
```

### Liste d'adjacence

```
E1  : {E2, E4, E5, E10}          degré = 4
E2  : {E1, E4, E6, E9}           degré = 4
E3  : {E4, E7, E11}              degré = 3
E4  : {E1, E2, E3, E5, E8}       degré = 5  ← MAX
E5  : {E1, E4, E8, E10}          degré = 4
E6  : {E2, E9}                   degré = 2
E7  : {E3, E11}                  degré = 2
E8  : {E4, E5, E12}              degré = 3
E9  : {E2, E6}                   degré = 2
E10 : {E1, E5}                   degré = 2
E11 : {E3, E7}                   degré = 2
E12 : {E8}                       degré = 1  ← MIN
```

### Informations clés

```
Nombre d'examens (sommets) : n = 12
Nombre de conflits (arêtes) : m = 17
Degré maximum : Δ(G) = 5 (E4)
Degré minimum : δ(G) = 1 (E12)

Bornes sur χ(G) :
  Borne inférieure : ω(G) ≥ ? (à déterminer, chercher la plus grande clique)
  Borne supérieure : χ(G) ≤ Δ(G) + 1 = 6 (théorème de Brooks)
```

---

## 🛠️ Démarche Professionnelle de Résolution

---

### PHASE 1 — Analyse Mathématique (sur papier d'abord)

#### Étape 1.1 : Comprendre l'algorithme de Welsh et Powell

```
ALGORITHME DE WELSH ET POWELL :

1. Calculer le degré de chaque sommet
2. Trier les sommets par degré DÉCROISSANT
3. Pour chaque nouvelle couleur c = 1, 2, 3, ... :
     Parcourir la liste triée des sommets :
       Si le sommet n'est pas encore coloré
       ET qu'aucun de ses voisins n'a la couleur c :
         → Lui attribuer la couleur c
4. Fin quand tous les sommets sont coloriés

Critère glouton : colorer le maximum de sommets avec chaque couleur
Complexité : O(n²)
Garantie : χ(G) ≤ Δ(G) + 1
```

#### Étape 1.2 : Modèle mathématique de la coloration

```
DONNÉES :
  n = 12 sommets (examens)
  G = (V, E) graphe des conflits
  k = nombre de couleurs (créneaux) — à minimiser

VARIABLES :
  xᵢc = 1 si l'examen i reçoit le créneau c, 0 sinon
  yc  = 1 si le créneau c est utilisé, 0 sinon

MODÈLE :
              k
  Min Z =     Σ  yc                  (minimiser le nombre de créneaux)
             c=1

  s.c. :
    k
    Σ  xᵢc = 1                      ∀ i      (1 créneau par examen)
   c=1

    xᵢc + xⱼc ≤ 1                   ∀(i,j) ∈ E, ∀c  (conflit interdit)

    xᵢc ≤ yc                        ∀ i, ∀c  (liaison x-y)

    xᵢc ∈ {0,1}    yc ∈ {0,1}
```

#### Étape 1.3 : Calculer les degrés et trier

```
Degrés :

  E4  : degré 5  ← rang 1
  E1  : degré 4  ← rang 2
  E2  : degré 4  ← rang 3
  E5  : degré 4  ← rang 4
  E3  : degré 3  ← rang 5
  E8  : degré 3  ← rang 6
  E6  : degré 2  ← rang 7
  E7  : degré 2  ← rang 8
  E9  : degré 2  ← rang 9
  E10 : degré 2  ← rang 10
  E11 : degré 2  ← rang 11
  E12 : degré 1  ← rang 12

Ordre de traitement :
  [E4, E1, E2, E5, E3, E8, E6, E7, E9, E10, E11, E12]
```

#### Étape 1.4 : Déterminer les bornes

```
BORNE INFÉRIEURE — Recherche de la plus grande clique :

  Clique {E1, E4, E5} :
    E1—E4 ✅  E1—E5 ✅  E4—E5 ✅  → clique de taille 3

  Clique {E1, E2, E4} :
    E1—E2 ✅  E1—E4 ✅  E2—E4 ✅  → clique de taille 3

  Clique de taille 4 ? Essayons {E1, E2, E4, E5} :
    E2—E5 ? NON ❌ → pas une clique

  ω(G) = 3

BORNES :
  3 = ω(G) ≤ χ(G) ≤ Δ(G) + 1 = 6

  Il faut AU MOINS 3 créneaux.
  Welsh et Powell en utilisera AU PLUS 6.
```

#### Étape 1.5 : Résoudre Welsh et Powell à la main

```
Ordre de traitement : [E4, E1, E2, E5, E3, E8, E6, E7, E9, E10, E11, E12]


═══ COULEUR 1 (Créneau Lundi 8h) ═══

Parcourir la liste :

→ E4 : pas coloré, aucun voisin en couleur 1
  ✅ E4 reçoit couleur 1
  Coloriés en 1 : {E4}

→ E1 : pas coloré, voisins = {E2,E4,E5,E10}
  E4 est en couleur 1 → CONFLIT ❌

→ E2 : pas coloré, voisins = {E1,E4,E6,E9}
  E4 est en couleur 1 → CONFLIT ❌

→ E5 : pas coloré, voisins = {E1,E4,E8,E10}
  E4 est en couleur 1 → CONFLIT ❌

→ E3 : pas coloré, voisins = {E4,E7,E11}
  E4 est en couleur 1 → CONFLIT ❌

→ E8 : pas coloré, voisins = {E4,E5,E12}
  E4 est en couleur 1 → CONFLIT ❌

→ E6 : pas coloré, voisins = {E2,E9}
  Aucun en couleur 1 → PAS DE CONFLIT
  ✅ E6 reçoit couleur 1
  Coloriés en 1 : {E4, E6}

→ E7 : pas coloré, voisins = {E3,E11}
  Aucun en couleur 1 → PAS DE CONFLIT
  ✅ E7 reçoit couleur 1
  Coloriés en 1 : {E4, E6, E7}

→ E9 : pas coloré, voisins = {E2,E6}
  E6 est en couleur 1 → CONFLIT ❌

→ E10 : pas coloré, voisins = {E1,E5}
  Aucun en couleur 1 → PAS DE CONFLIT
  ✅ E10 reçoit couleur 1
  Coloriés en 1 : {E4, E6, E7, E10}

→ E11 : pas coloré, voisins = {E3,E7}
  E7 est en couleur 1 → CONFLIT ❌

→ E12 : pas coloré, voisins = {E8}
  Aucun en couleur 1 → PAS DE CONFLIT
  ✅ E12 reçoit couleur 1
  Coloriés en 1 : {E4, E6, E7, E10, E12}

Bilan : Créneau 1 = {E4, E6, E7, E10, E12} (stable ✅)


═══ COULEUR 2 (Créneau Lundi 14h) ═══

Non coloriés restants : {E1, E2, E5, E3, E8, E9, E11}

→ E1 : voisins = {E2,E4,E5,E10}
  Aucun en couleur 2
  ✅ E1 reçoit couleur 2
  Coloriés en 2 : {E1}

→ E2 : voisins = {E1,E4,E6,E9}
  E1 est en couleur 2 → CONFLIT ❌

→ E5 : voisins = {E1,E4,E8,E10}
  E1 est en couleur 2 → CONFLIT ❌

→ E3 : voisins = {E4,E7,E11}
  Aucun en couleur 2
  ✅ E3 reçoit couleur 2
  Coloriés en 2 : {E1, E3}

→ E8 : voisins = {E4,E5,E12}
  Aucun en couleur 2
  ✅ E8 reçoit couleur 2
  Coloriés en 2 : {E1, E3, E8}

→ E9 : voisins = {E2,E6}
  Aucun en couleur 2
  ✅ E9 reçoit couleur 2
  Coloriés en 2 : {E1, E3, E8, E9}

→ E11 : voisins = {E3,E7}
  E3 est en couleur 2 → CONFLIT ❌

Bilan : Créneau 2 = {E1, E3, E8, E9} (stable ✅)


═══ COULEUR 3 (Créneau Mardi 8h) ═══

Non coloriés restants : {E2, E5, E11}

→ E2 : voisins = {E1,E4,E6,E9}
  Aucun en couleur 3
  ✅ E2 reçoit couleur 3

→ E5 : voisins = {E1,E4,E8,E10}
  Aucun en couleur 3
  ✅ E5 reçoit couleur 3

→ E11 : voisins = {E3,E7}
  Aucun en couleur 3
  ✅ E11 reçoit couleur 3

Bilan : Créneau 3 = {E2, E5, E11} (stable ✅)


═══ TOUS LES SOMMETS SONT COLORIÉS ═══

RÉSULTAT :
  Créneau 1 (Lundi 8h)  : {E4, E6, E7, E10, E12}   5 examens
  Créneau 2 (Lundi 14h) : {E1, E3, E8, E9}          4 examens
  Créneau 3 (Mardi 8h)  : {E2, E5, E11}              3 examens

  χ_WP(G) = 3 créneaux

Comme ω(G) = 3, on sait que χ(G) ≥ 3.
Donc χ(G) = 3 et la solution est OPTIMALE ✅
```

#### Étape 1.6 : Vérification exhaustive des conflits

```
Créneau 1 : {E4, E6, E7, E10, E12}
  E4—E6 ?  NON ✅   E4—E7 ?  NON ✅   E4—E10 ? NON ✅   E4—E12 ? NON ✅
  E6—E7 ?  NON ✅   E6—E10 ? NON ✅   E6—E12 ? NON ✅
  E7—E10 ? NON ✅   E7—E12 ? NON ✅
  E10—E12? NON ✅   → STABLE ✅

Créneau 2 : {E1, E3, E8, E9}
  E1—E3 ?  NON ✅   E1—E8 ? NON ✅   E1—E9 ? NON ✅
  E3—E8 ?  NON ✅   E3—E9 ? NON ✅
  E8—E9 ?  NON ✅   → STABLE ✅

Créneau 3 : {E2, E5, E11}
  E2—E5 ?  NON ✅   E2—E11 ? NON ✅
  E5—E11 ? NON ✅   → STABLE ✅

17/17 arêtes de conflit respectées → COLORATION VALIDE ✅
```

> ✅ Vérifie que tu obtiens exactement 3 couleurs avant de coder.

---

### PHASE 2 — Conception (pseudo-code)

#### Étape 2.1 : Pseudo-code de Welsh et Powell

```
ALGORITHME WelshPowell

ENTRÉES :
    n                 : nombre de sommets
    adj[0..n-1]       : liste d'adjacence (adj[i] = ensemble des voisins de i)

SORTIE :
    couleurs[0..n-1]  : couleur attribuée à chaque sommet (-1 si non coloré)
    nb_couleurs       : nombre total de couleurs utilisées

DÉBUT
    ── Étape 1 : Calculer les degrés ──
    degres ← [|adj[i]| pour i de 0 à n-1]

    ── Étape 2 : Trier par degré décroissant ──
    ordre ← indices triés par degres[i] décroissant

    ── Étape 3 : Initialiser ──
    couleurs ← [-1, -1, ..., -1]    (n éléments, -1 = non coloré)
    couleur_courante ← 0

    ── Étape 4 : Colorer ──
    TANT QUE il existe des sommets non coloriés FAIRE

        POUR chaque sommet i dans ordre FAIRE
            SI couleurs[i] = -1 ALORS    (non encore coloré)

                ── Vérifier si i peut recevoir couleur_courante ──
                conflit ← FAUX
                POUR chaque voisin v de adj[i] FAIRE
                    SI couleurs[v] = couleur_courante ALORS
                        conflit ← VRAI
                        SORTIR
                    FIN SI
                FIN POUR

                SI NON conflit ALORS
                    couleurs[i] ← couleur_courante
                FIN SI

            FIN SI
        FIN POUR

        couleur_courante ← couleur_courante + 1

    FIN TANT QUE

    nb_couleurs ← couleur_courante
    RETOURNER couleurs, nb_couleurs
FIN
```

#### Étape 2.2 : Structures de données

```
1. Liste d'adjacence (la plus efficace) :
     adj = [
       {1, 3, 4, 9},       # E1 (indice 0) : voisins E2,E4,E5,E10
       {0, 3, 5, 8},       # E2 (indice 1) : voisins E1,E4,E6,E9
       {3, 6, 10},          # E3 (indice 2) : voisins E4,E7,E11
       {0, 1, 2, 4, 7},    # E4 (indice 3) : voisins E1,E2,E3,E5,E8
       {0, 3, 7, 9},       # E5 (indice 4) : voisins E1,E4,E8,E10
       {1, 8},              # E6 (indice 5) : voisins E2,E9
       {2, 10},             # E7 (indice 6) : voisins E3,E11
       {3, 4, 11},          # E8 (indice 7) : voisins E4,E5,E12
       {1, 5},              # E9 (indice 8) : voisins E2,E6
       {0, 4},              # E10 (indice 9) : voisins E1,E5
       {2, 6},              # E11 (indice 10) : voisins E3,E7
       {7},                  # E12 (indice 11) : voisin E8
     ]

2. Matrice d'adjacence (alternative) :
     matrice[i][j] = 1 si arête, 0 sinon

3. Mapping noms ↔ indices :
     noms = ["E1","E2","E3","E4","E5","E6",
             "E7","E8","E9","E10","E11","E12"]

4. Résultat :
     couleurs = [1, 2, 1, 0, 2, 0, 0, 1, 1, 0, 2, 0]
     → traduit : E1=créneau2, E2=créneau3, E3=créneau2, E4=créneau1, ...

Complexité :
  Calcul des degrés : O(n + m)
  Tri : O(n log n)
  Coloration : O(n × (n + m)) dans le pire cas
  Total : O(n² + n·m)
```

---

### PHASE 3 — Implémentation (coder)

#### Étape 3.1 : Structure du projet

```
projet_coloration/
│
├── main.py                         Programme principal
│
├── donnees.py                      Données du problème
│   ├── noms                        Noms des examens
│   ├── matieres                    Descriptions
│   ├── adjacence                   Liste d'adjacence
│   └── matrice_adjacence           Matrice (optionnel)
│
├── welsh_powell.py                 Algorithme principal
│   ├── calculer_degres()           Degrés de chaque sommet
│   ├── welsh_powell()              Algorithme complet
│   └── est_coloration_valide()     Vérification rapide
│
├── affichage.py                    Module affichage
│   ├── afficher_graphe()           Liste d'adjacence + degrés
│   ├── afficher_trace()            Trace pas à pas
│   ├── afficher_planning()         Planning des créneaux
│   └── afficher_stats()            Statistiques et bornes
│
├── verification.py                 Vérification
│   ├── verifier_coloration()       Coloration valide ?
│   ├── trouver_clique_max()        Borne inférieure
│   └── verifier_graphe()           Graphe cohérent ?
│
└── tests.py                        Tests unitaires
```

#### Étape 3.2 : Squelette des données

```python
# donnees.py

noms = ["E1", "E2", "E3", "E4", "E5", "E6",
        "E7", "E8", "E9", "E10", "E11", "E12"]

matieres = {
    "E1": "Mathématiques I",      "E2": "Algorithmique",
    "E3": "Physique Générale",    "E4": "Anglais Scientifique",
    "E5": "Statistiques",         "E6": "Bases de Données",
    "E7": "Mécanique",            "E8": "Économie Générale",
    "E9": "Programmation C",      "E10": "Algèbre Linéaire",
    "E11": "Électronique",        "E12": "Droit Commercial",
}

noms_creneaux = ["Lundi 8h", "Lundi 14h", "Mardi 8h",
                 "Mardi 14h", "Mercredi 8h", "Mercredi 14h"]

# Liste d'adjacence (indices 0 à 11)
adjacence = [
    {1, 3, 4, 9},       # E1
    {0, 3, 5, 8},       # E2
    {3, 6, 10},          # E3
    {0, 1, 2, 4, 7},    # E4
    {0, 3, 7, 9},       # E5
    {1, 8},              # E6
    {2, 10},             # E7
    {3, 4, 11},          # E8
    {1, 5},              # E9
    {0, 4},              # E10
    {2, 6},              # E11
    {7},                  # E12
]

# Conflits sous forme de liste d'arêtes (pour affichage)
conflits = [
    ("E1","E2"), ("E1","E4"), ("E1","E5"), ("E1","E10"),
    ("E2","E4"), ("E2","E6"), ("E2","E9"),
    ("E3","E4"), ("E3","E7"), ("E3","E11"),
    ("E4","E5"), ("E4","E8"),
    ("E5","E8"), ("E5","E10"),
    ("E6","E9"),
    ("E7","E11"),
    ("E8","E12"),
]
```

#### Étape 3.3 : Squelette de la fonction Welsh-Powell

```python
# welsh_powell.py

def calculer_degres(adjacence):
    """
    Calcule le degré de chaque sommet.

    Args:
        adjacence (list[set]) : liste d'adjacence

    Returns:
        list[int] : degré de chaque sommet
    """
    # degres[i] = len(adjacence[i])
    pass


def welsh_powell(adjacence):
    """
    Algorithme de Welsh et Powell pour la coloration de graphe.

    Args:
        adjacence (list[set]) : liste d'adjacence

    Returns:
        list[int] : couleur de chaque sommet (0, 1, 2, ...)
        int       : nombre de couleurs utilisées
        list[list[int]] : classes de couleur (sommets par couleur)
    """
    n = len(adjacence)

    # 1. Calculer les degrés
    #    degres = calculer_degres(adjacence)

    # 2. Trier les sommets par degré décroissant
    #    ordre = sorted(range(n), key=lambda i: degres[i], reverse=True)

    # 3. Initialiser les couleurs à -1 (non coloré)
    #    couleurs = [-1] * n

    # 4. Pour chaque nouvelle couleur :
    #      Parcourir les sommets dans l'ordre trié
    #      Si le sommet est non coloré ET compatible :
    #        Lui attribuer la couleur courante
    #    Incrémenter la couleur

    # 5. Construire les classes de couleur
    #    classes = regrouper les sommets par couleur

    # 6. Retourner couleurs, nb_couleurs, classes
    pass


def est_coloration_valide(couleurs, adjacence):
    """
    Vérifie rapidement si une coloration est valide.

    Returns:
        bool : True si aucun conflit
    """
    # Pour chaque sommet i :
    #   Pour chaque voisin v de i :
    #     Si couleurs[i] == couleurs[v] : CONFLIT → return False
    # return True
    pass
```

#### Étape 3.4 : Affichage attendu

```
════════════════════════════════════════════════════════════════
   PLANNING DES EXAMENS — UNIVERSITÉ FÉLIX HOUPHOUËT-BOIGNY
   Algorithme : Welsh et Powell
════════════════════════════════════════════════════════════════

  ÉTAPE 1 — Degrés et tri

  ┌────────┬─────────────────────┬────────┬──────┐
  │ Examen │ Matière             │ Degré  │ Rang │
  ├────────┼─────────────────────┼────────┼──────┤
  │ E4     │ Anglais Scientifique│   5    │  1   │
  │ E1     │ Mathématiques I     │   4    │  2   │
  │ E2     │ Algorithmique       │   4    │  3   │
  │ E5     │ Statistiques        │   4    │  4   │
  │ ...    │ ...                 │  ...   │ ...  │
  └────────┴─────────────────────┴────────┴──────┘

  ÉTAPE 2 — Coloration

  Couleur 1 (Lundi 8h) :
    ✅ E4 → coloré  (aucun conflit)
    ❌ E1 → refusé  (conflit avec E4)
    ...
    ✅ E6 → coloré  (aucun conflit)
    ...

  PLANNING FINAL :

  ┌─────────────────┬─────────────────────────────────────────┐
  │ Créneau         │ Examens                                 │
  ├─────────────────┼─────────────────────────────────────────┤
  │ Lundi 8h        │ E4, E6, E7, E10, E12   (5 examens)     │
  │ Lundi 14h       │ E1, E3, E8, E9         (4 examens)     │
  │ Mardi 8h        │ E2, E5, E11            (3 examens)     │
  └─────────────────┴─────────────────────────────────────────┘

  ┌──────────────────────────────────────────────┐
  │  Nombre de créneaux : 3                      │
  │  Borne inférieure ω(G) : 3                   │
  │  Borne supérieure Δ+1  : 6                   │
  │  SOLUTION OPTIMALE ✅  (3 = ω)               │
  │  Conflits détectés : 0/17 ✅                 │
  └──────────────────────────────────────────────┘
```

#### Étape 3.5 : Règles de codage

```
1. REPRÉSENTATION DU GRAPHE
     Utiliser la liste d'adjacence (ensembles Python : set)
     Plus efficace que la matrice pour les graphes creux

2. NOMMER clairement
     ✅ couleur_courante, sommet_courant, a_conflit
     ❌ c, s, f

3. SÉPARER les responsabilités
     welsh_powell.py  → logique pure
     affichage.py     → affichage et trace
     verification.py  → vérification de la coloration

4. TRACER chaque décision
     "E4 : non coloré, aucun voisin en couleur 0 → COLORÉ en 0"
     "E1 : non coloré, voisin E4 en couleur 0 → CONFLIT, passé"

5. VÉRIFICATION AUTOMATIQUE
     Après chaque coloration, vérifier :
       - Tous les sommets sont coloriés
       - Aucune arête n'a deux extrémités de même couleur
       - Chaque classe de couleur est un stable
```

---

### PHASE 4 — Tests et Validation

#### Étape 4.1 : Tests unitaires

```
TEST 1 — Données complètes (12 examens)
  Attendu : 3 couleurs
  Créneau 1 = {E4,E6,E7,E10,E12}, Créneau 2 = {E1,E3,E8,E9}, Créneau 3 = {E2,E5,E11}

TEST 2 — Graphe complet K4
  adj = [{1,2,3},{0,2,3},{0,1,3},{0,1,2}]
  Attendu : 4 couleurs (chaque sommet sa propre couleur)

TEST 3 — Graphe biparti
  adj = [{2,3},{2,3},{0,1},{0,1}]
  Attendu : 2 couleurs

TEST 4 — Graphe sans arêtes
  adj = [set(), set(), set()]
  Attendu : 1 couleur (tous au même créneau)

TEST 5 — Un seul sommet
  adj = [set()]
  Attendu : 1 couleur

TEST 6 — Cycle impair C5
  adj = [{1,4},{0,2},{1,3},{2,4},{3,0}]
  Attendu : 3 couleurs

TEST 7 — Cycle pair C6
  adj = [{1,5},{0,2},{1,3},{2,4},{3,5},{4,0}]
  Attendu : 2 couleurs

TEST 8 — Validité de la coloration
  Vérifier est_coloration_valide() sur solution connue
  Vérifier qu'une fausse coloration est détectée
```

#### Étape 4.2 : Vérification automatique

```python
def verifier_coloration(couleurs, adjacence):
    """
    Vérifie la validité complète d'une coloration.

    Vérifications :
      1. Tous les sommets sont coloriés (aucun -1)
      2. Aucune arête avec deux extrémités de même couleur
      3. Chaque classe de couleur est un stable
      4. Nombre de couleurs ≥ borne inférieure

    Returns:
        bool : True si tout OK
        list[str] : messages d'erreur
    """
    pass


def verifier_graphe(adjacence):
    """
    Vérifie la cohérence du graphe.

    Vérifications :
      1. Symétrique : si j ∈ adj[i] alors i ∈ adj[j]
      2. Pas de boucle : i ∉ adj[i]
      3. Indices valides : tous dans [0, n-1]
    """
    pass
```

---

### PHASE 5 — Extensions (aller plus loin)

#### Extension 1 : Comparer avec DSatur

```
Implémenter l'algorithme DSatur :
  - Au lieu de trier par degré une seule fois,
    choisir à chaque étape le sommet avec le plus grand
    degré de SATURATION (nombre de couleurs différentes chez ses voisins)
  - Souvent meilleur que Welsh-Powell

Comparer : nb de couleurs Welsh-Powell vs DSatur
```

#### Extension 2 : Lecture depuis un fichier

```
Lire les conflits depuis un fichier CSV :
  E1,E2
  E1,E4
  E1,E5
  ...

Permet de changer les données sans modifier le code.
Tester sur les instances DIMACS (benchmarks de coloration).
```

#### Extension 3 : Visualisation du graphe

```
Avec matplotlib + networkx :
  1. Dessiner le graphe des conflits
  2. Colorer les sommets selon la solution de Welsh-Powell
  3. Afficher les noms des examens
  4. Légende avec les créneaux
```

#### Extension 4 : Génération aléatoire d'instances

```
Générer des graphes aléatoires :
  - n sommets, probabilité p d'arête entre chaque paire
  - Tester Welsh-Powell sur n = 20, 50, 100, 200
  - Mesurer : nb de couleurs, temps d'exécution
  - Comparer avec la borne Δ+1

Tracer la courbe : nb_couleurs en fonction de n
```

#### Extension 5 : Planning réel avec contraintes supplémentaires

```
Ajouter des contraintes réelles :
  - Maximum 5 examens par créneau (capacité des salles)
  - Certains examens doivent être le matin
  - Un professeur ne peut surveiller qu'un examen à la fois

Cela transforme le problème en coloration avec contraintes.
```

---

## 📋 Checklist de Livraison

```
PHASE 1 — Analyse Mathématique
  □ Graphe des conflits construit (12 sommets, 17 arêtes)
  □ Degrés calculés, tri effectué
  □ Bornes : ω(G) = 3, Δ+1 = 6
  □ Welsh-Powell résolu à la main → 3 couleurs
  □ Vérification exhaustive des 17 arêtes ✅

PHASE 2 — Conception
  □ Pseudo-code Welsh-Powell complet
  □ Structures de données choisies (liste d'adjacence)
  □ Interface des fonctions définie

PHASE 3 — Implémentation
  □ donnees.py : adjacence + noms + matières
  □ calculer_degres() codé
  □ welsh_powell() codé
  □ est_coloration_valide() codé
  □ Affichage : trace + planning + stats
  □ Code commenté, noms explicites

PHASE 4 — Tests
  □ 8 tests unitaires validés (K4, biparti, C5, C6, etc.)
  □ verifier_coloration() implémenté
  □ verifier_graphe() implémenté
  □ 3 couleurs retrouvées par le code

PHASE 5 — Extensions (bonus)
  □ DSatur implémenté et comparé
  □ Lecture depuis fichier CSV
  □ Visualisation networkx + matplotlib
  □ Instances aléatoires testées
  □ Contraintes supplémentaires
```

---

## 📐 Rappels Théoriques

### Algorithme de Welsh et Powell

```
1. Calculer les degrés
2. Trier par degré DÉCROISSANT
3. Pour chaque couleur : parcourir et colorer les compatibles
4. Fin quand tout est coloré

Complexité : O(n² + n·m)
Garantie : χ_WP ≤ Δ(G) + 1
```

### Bornes sur χ(G)

```
ω(G) ≤ χ(G) ≤ Δ(G) + 1

ω(G) = taille de la plus grande clique
Δ(G) = degré maximum

Si χ_WP = ω(G) → solution OPTIMALE prouvée
```

### Applications de la coloration

```
Planification d'examens  →  sommets=examens, arêtes=conflits
Attribution de fréquences →  sommets=antennes, arêtes=interférences
Allocation de registres   →  sommets=variables, arêtes=simultanéité
Coloration de cartes      →  sommets=pays, arêtes=frontières
```

---

*Bonne implémentation ! 💪*
