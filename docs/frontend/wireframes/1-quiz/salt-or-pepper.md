# Wireframes — Sel ou Poivre

## Sommaire

- [SaltOrPepperListPage](#1-saltorpepperlistpage)
- [SaltOrPepperDetailPage](#2-saltorpepperdetailpage)
- [SaltOrPepperCreatePage / SaltOrPepperEditPage](#3-saltorpeppercreatepage--saltorpeppereditpage)

---

## 1 - SaltOrPepperListPage

### Principe

Liste des manches Sel ou poivre : colonnes titre, original ?, nombre d’utilisation. Bouton Ajouter → SaltOrPepperCreatePage. Actions : détail, édition, suppression (modale).

### Wireframe

Même schéma que NuggetsListPage : Titre | Original ? | Utilisations | Actions.

### Appels API

| Action | Méthode | Endpoint                    | Réf.                                                    |
| ------ | ------- | --------------------------- | ------------------------------------------------------- |
| Lister | GET     | `/api/quiz/salt-or-pepper/` | [api-reference](../../../backend/api-reference.md) §2.3 |

---

## 2 - SaltOrPepperDetailPage

### Principe

Affichage en lecture : titre, description, original ?, propositions (choice_labels), liste des questions avec la réponse correcte pour chacune. Actions : SaltOrPepperEditPage, suppression (modale).

### Wireframe

```
+-------------------------------------------------------------------+
|  Détail manche Sel ou Poivre                                      |
+-------------------------------------------------------------------+
|  Titre        Noir, Blanc ou Les deux                             |
|  Description  ...                                                 |
|  Original ?   oui                                                 |
|  Propositions  Noir | Blanc | Les deux                            |
|  Questions :  1. Question 1  →  Noir  2. Question 2  →  Blanc     |
|  ( Modifier )  ( Supprimer )                                       |
+-------------------------------------------------------------------+
```

### Appels API

| Action | Méthode | Endpoint                         | Réf.                                                    |
| ------ | ------- | -------------------------------- | ------------------------------------------------------- |
| Détail | GET     | `/api/quiz/salt-or-pepper/{id}/` | [api-reference](../../../backend/api-reference.md) §2.3 |

---

## 3 - SaltOrPepperCreatePage / SaltOrPepperEditPage

### Principe

Formulaire : titre, description, original. **Propositions** (2 à 5) en champs modifiables avec [ + ] [ − ]. Questions en InlineForm : énoncé + **déroulant** (réponse = une des propositions). Contrainte API : réponses des questions cohérentes avec les propositions. Questions type SP uniquement.

### Wireframe

```
+----------------------------------------------------------------------+
|  Créer une manche Sel ou Poivre  (ou Modifier)                       |
+----------------------------------------------------------------------+
|  Titre       [________________________________________________]      |
|  Description [________________________________________________]      |
|  Original    [ ] oui                                                 |
|  Propositions (2 à 5)  [ Noir ] [ Blanc ] [ Les deux ]  [ + ] [ − ]  |
|  Questions                                                           |
|  | Énoncé [____________________________]  Réponse [ Noir ▼ ]  [🗑] |  |
|  [ + Ajouter une question ]                                          |
|  ( Annuler )                                       ( Enregistrer )   |
+----------------------------------------------------------------------+
```

### Appels API

| Action                    | Méthode   | Endpoint                                | Réf.                                                    |
| ------------------------- | --------- | --------------------------------------- | ------------------------------------------------------- |
| Créer                     | POST      | `/api/quiz/salt-or-pepper/`             | [api-reference](../../../backend/api-reference.md) §2.3 |
| Modifier                  | PUT/PATCH | `/api/quiz/salt-or-pepper/{id}/`        | idem                                                    |
| Questions (liste type SP) | GET       | `/api/quiz/questions/?question_type=SP` | §2.1                                                    |
