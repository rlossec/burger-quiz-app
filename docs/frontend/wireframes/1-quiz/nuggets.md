# Wireframes — Nuggets

## Nuggets

Pages :

- **NuggetsListPage** : Liste des manche Nuggets disponibles
- **NuggetsDetailPage** : Detail de la manche Nuggets cliqué
- **NuggetsCreatePage** : Création d'une manche Nuggets
- **NuggetsEditPage** : Edition de la manche Nuggets cliqué

### NuggetsListPage

On peut imaginer un tableau listant les Manches nuggets créées, avec une colonne original ?, une colonne Utilisation (correspondant au nombre de fois où elle est dans un BurgerQuiz), et une colonne nbre de Nuggets. Enfin un bouton Ajouter en haut à droite du tableau permet d'aller vers la page de création.

### NuggetsCreatePage / NuggetsEditPage

Pattern **InlineForm** pour les questions (détail : [components.md](components.md)). Champs de sélection ou création inline de questions Nuggets, de base au nombre de 6, deux par deux par ligne. En effet comme on pose des questions à tour de rôle, il faut qu'on est des couples de questions.
Aussi on pourra penser à la contrainte que lorsqu'une manche est sélectionné elle soit grisée et non cliquable pour les autres champs de sélection.

> Backend : Penser à mettre dans API reference de vérifiez à la fois le fait qu'on soumette un nombre pair de question et qu'il n'y est pas deux fois la même question

Un bouton et une modale permettront d'ajouter des questions Nuggets et des boutons avec des icones pour aller vers SaltOrPepperDetailPage ou SaltOrPepperEditPage et enfin un bouton trashicon rouge avec modale de confirmation pour supprimer une manche.

---

## NuggetsListPage

```
+------------------------------------------------------------------+
|  Manches Nuggets                              [ + Ajouter ]       |
+------------------------------------------------------------------+
|  Titre           | Original ? | Utilisations | Nbre questions | Actions   |
|------------------|------------|--------------|---------------|-----------|
|  Episode 123     | oui        | 2            | 6             | [👁][✏️][🗑] |
|  ...             | ...        | ...          | ...           | ...       |
+------------------------------------------------------------------+
```

---

## NuggetsCreatePage / NuggetsEditPage (InlineForm, 2 par 2)

```
+------------------------------------------------------------------+
|  Créer une manche Nuggets  (ou Modifier)                           |
+------------------------------------------------------------------+
|  Titre  [________________________________________________]        |
|  Original  [ ] oui                                                |
|                                                                  |
|  Questions (nombre pair, 2 par 2)                                 |
|  +-------------------------------+  +-------------------------------+    |
|  | Q1 [________________________] |  | Q2 [________________________] |[🗑] |
|  | Réponse correcte              |  | Réponses  correcte            |    |
|  | Réponse piège 1               |  | Réponse piège 1               |    |
|  | Réponse piège 2               |  | Réponse piège 2               |    |
|  | Réponse piège 3               |  | Réponse piège 3               |    |
|  +-------------------------------+  +-------------------------------+    |
|  +-------------------------------+  +-------------------------------+ [🗑]|
|  | Q3 [________________________] |  | Q4 [________________________] |    |
|  | ...                           |  | ...                           |    |
|  +-------------------------------+  +-------------------------------+    |
|  +-------------------------------+  +-------------------------------+    |
|  | Q5 [________________________] |  | Q6 [________________________] |    |
|  +-------------------------------+  +-------------------------------+    |
|                                                                  |
|  [ + Ajouter une paire de questions ]
|                                                                  |
|  ( Annuler )                                    ( Enregistrer )   |
+------------------------------------------------------------------+
```
