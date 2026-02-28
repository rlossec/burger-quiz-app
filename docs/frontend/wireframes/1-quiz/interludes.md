# Wireframes — Interludes Vidéo

Réf. : [page_reference](../../page_reference.md) · [README](README.md)

## Sommaire

- [InterludesListPage](#1-interludeslistpage)
- [InterludesCreatePage](#2-interludescreatepage)
- [InterludesDetailPage](#3-interludesdetailpage)
- [InterludesEditPage](#4-interludeseditpage)

---

## 1 - InterludesListPage

### Principe

Liste des interludes vidéo YouTube disponibles. Filtres par type (Intro, Outro, Pub, Interlude). Chaque ligne affiche une miniature YouTube, le titre, le type et les actions.

### Wireframe

```
+-------------------------------------------------------------------------+
|  Interludes vidéo                                    [ + Créer ]        |
+-------------------------------------------------------------------------+
|  Filtres : [Tous ▼] [Intro] [Outro] [Pub] [Interlude]                   |
|  Recherche : [____________________________] 🔍                          |
+-------------------------------------------------------------------------+
|  Miniature     | Titre            | Type      | Durée  | Actions        |
|----------------|------------------|-----------|--------|----------------|
|  [▶️ thumb]    | Intro Burger     | 🎬 Intro  | 0:30   | [👁][✏️][🗑]   |
|  [▶️ thumb]    | Pub Sponsor      | 📺 Pub    | 0:15   | [👁][✏️][🗑]   |
|  [▶️ thumb]    | Outro Credits    | 🎬 Outro  | 0:45   | [👁][✏️][🗑]   |
+-------------------------------------------------------------------------+
```

### Appels API

| Action     | Méthode | Endpoint                            | Params                   |
| ---------- | ------- | ----------------------------------- | ------------------------ |
| Lister     | GET     | `/api/quiz/interludes/`             | `?type=IN&search=...`    |
| Supprimer  | DELETE  | `/api/quiz/interludes/{id}/`        | —                        |

---

## 2 - InterludesCreatePage

### Principe

Formulaire de création d'un interlude vidéo. L'URL YouTube est validée et une prévisualisation s'affiche automatiquement.

### Wireframe

```
+-------------------------------------------------------------------------+
|  Créer un interlude vidéo                                               |
+-------------------------------------------------------------------------+
|                                                                         |
|  <InterludeForm />                                                      |
|                                                                         |
|  Titre *      [________________________________________________]        |
|                                                                         |
|  URL YouTube * [________________________________________________]       |
|               ℹ️ Formats acceptés : youtube.com/watch?v=, youtu.be/     |
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │  <YouTubePreview />                                             │   |
|  │  [▶️ Miniature vidéo YouTube]                                   │   |
|  │  Vidéo détectée : "Titre de la vidéo"                           │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  Type         [Interlude ▼]  (Intro | Outro | Pub | Interlude)          |
|                                                                         |
|  Options de lecture :                                                   |
|  [x] Lecture automatique                                                |
|  [x] Autoriser le skip après [___5___] secondes                         |
|                                                                         |
|  Durée (secondes)  [_______]  (optionnel)                               |
|                                                                         |
|  Tags         [________________________________________________]        |
|               (séparés par des virgules)                                |
|                                                                         |
|  ( Annuler )                                         ( Créer )          |
+-------------------------------------------------------------------------+
```

### Composants

#### `<InterludeForm />`

Formulaire de création/édition d'un interlude.

| Prop          | Type                    | Description                       |
| ------------- | ----------------------- | --------------------------------- |
| interlude?    | VideoInterlude          | Données existantes (mode édition) |
| onSubmit      | (data) => Promise<void> | Callback de soumission            |
| onCancel?     | () => void              | Callback d'annulation             |
| isSubmitting? | boolean                 | État de chargement                |

#### `<YouTubePreview />`

Prévisualisation d'une vidéo YouTube à partir de l'URL.

| Prop        | Type    | Description                      |
| ----------- | ------- | -------------------------------- |
| youtubeUrl  | string  | URL YouTube à prévisualiser      |
| showPlayer? | boolean | Afficher le player intégré       |

### Appels API

| Action | Méthode | Endpoint               | Body                                        |
| ------ | ------- | ---------------------- | ------------------------------------------- |
| Créer  | POST    | `/api/quiz/interludes/`| `{ title, youtube_url, interlude_type, ...}`|

---

## 3 - InterludesDetailPage

### Principe

Affichage en lecture seule d'un interlude avec le player YouTube intégré.

### Wireframe

```
+-------------------------------------------------------------------------+
|  Interlude — Intro Burger                        [✏️ Modifier] [🗑]     |
+-------------------------------------------------------------------------+
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │                                                                 │   |
|  │                    [▶️ Player YouTube intégré]                  │   |
|  │                                                                 │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  <InterludeCard />                                                      |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │  Type        : 🎬 Intro                                         │   |
|  │  Durée       : 30 secondes                                      │   |
|  │  Autoplay    : ✅ Oui                                           │   |
|  │  Skip        : ✅ Après 5 secondes                              │   |
|  │                                                                 │   |
|  │  Tags        : #intro #sponsor                                  │   |
|  │  Auteur      : @username                                        │   |
|  │  Créé le     : 15/02/2025                                       │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
+-------------------------------------------------------------------------+
```

### Appels API

| Action  | Méthode | Endpoint                     |
| ------- | ------- | ---------------------------- |
| Charger | GET     | `/api/quiz/interludes/{id}/` |

---

## 4 - InterludesEditPage

### Principe

Même formulaire que la création, pré-rempli avec les données existantes.

### Wireframe

```
+-------------------------------------------------------------------------+
|  Modifier l'interlude — Intro Burger                                    |
+-------------------------------------------------------------------------+
|                                                                         |
|  <InterludeForm interlude={interlude} />                                |
|                                                                         |
|  Titre *      [Intro Burger_____________________________________]       |
|                                                                         |
|  URL YouTube * [https://youtube.com/watch?v=abc123_______________]      |
|                                                                         |
|  ┌─────────────────────────────────────────────────────────────────┐   |
|  │  <YouTubePreview />                                             │   |
|  │  [▶️ Miniature vidéo YouTube]                                   │   |
|  └─────────────────────────────────────────────────────────────────┘   |
|                                                                         |
|  Type         [Intro ▼]                                                 |
|                                                                         |
|  Options de lecture :                                                   |
|  [x] Lecture automatique                                                |
|  [x] Autoriser le skip après [___5___] secondes                         |
|                                                                         |
|  Durée (secondes)  [__30___]                                            |
|                                                                         |
|  Tags         [intro, sponsor________________________________]          |
|                                                                         |
|  ( Annuler )                                      ( Enregistrer )       |
+-------------------------------------------------------------------------+
```

### Appels API

| Action   | Méthode | Endpoint                     | Body                    |
| -------- | ------- | ---------------------------- | ----------------------- |
| Charger  | GET     | `/api/quiz/interludes/{id}/` | —                       |
| Modifier | PUT     | `/api/quiz/interludes/{id}/` | `{ title, ...}`         |
| Patch    | PATCH   | `/api/quiz/interludes/{id}/` | `{ champs modifiés }`   |

---

## 5 - Modale SearchAndSelectInterlude

Pour insérer un interlude dans la structure d'un Burger Quiz.

### Wireframe

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✕  Ajouter un interlude                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  <SearchAndSelectInterlude />                                        │
│                                                                      │
│  Type : [Tous ▼] [Intro] [Outro] [Pub] [Interlude]                   │
│                                                                      │
│  Recherche : [_______________________] 🔍                            │
│                                                                      │
│  Résultats :                                                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ [▶️] ○ Intro Burger Quiz (🎬 Intro, 30s)                     │   │
│  │ [▶️] ● Pub Sponsor (📺 Pub, 15s) — sélectionné ✓             │   │
│  │ [▶️] ○ Transition musique (🎵 Interlude, 10s)                │   │
│  │ [▶️] ○ Outro Credits (🎬 Outro, 45s)                         │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ────────────────────────────────────────────────────────────────   │
│  [Annuler]                                           [Ajouter]       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 6 - Types d'interludes

| Code | Label      | Icône | Usage typique                        |
| ---- | ---------- | ----- | ------------------------------------ |
| IN   | Intro      | 🎬    | Début du quiz                        |
| OU   | Outro      | 🎬    | Fin du quiz, crédits                 |
| PU   | Pub        | 📺    | Pause publicitaire entre les manches |
| IL   | Interlude  | 🎵    | Transition musicale, pause           |
