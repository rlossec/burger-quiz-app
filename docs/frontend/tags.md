# Tags — stratégie frontend

Ce document décrit une approche **réutilisable** pour les champs « tags » (autocomplétion + badges) dans l’application. Il s’aligne sur les pratiques en place : React Hook Form, Zod, TanStack Query, composants UI (shadcn), organisation par feature `quiz/`.

**Référence API** : détail complet dans [`docs/backend/api-reference.md`](../backend/api-reference.md) — § **3.10 Tags (autocomplete)**.

---

## 1. Contexte métier et technique

- **Côté API**, les tags sont des **`string[]`** (liste de noms), gérés par **django-taggit** sur plusieurs modèles.
- **Côté UI actuelle**, certains formulaires utilisent encore une **chaîne** « séparée par des virgules » (ex. `BurgerQuizForm`) alors que le payload JSON attend un **tableau** — la migration vers un champ **`string[]` dans le formulaire** simplifiera l’usage d’un composant tags et évitera les conversions fragiles.

Objectif produit : **saisie avec suggestions** (tags déjà présents en base) + **affichage en chips** une fois validés.

---

## 2. Endpoint backend (opérationnel)

L’autocomplétion s’appuie sur :

| Élément     | Valeur                                                                    |
| ----------- | ------------------------------------------------------------------------- |
| **Méthode** | `GET`                                                                     |
| **URL**     | `/api/quiz/tags/`                                                         |
| **Auth**    | JWT (`Authorization: Bearer …`) — même règle que le reste de `/api/quiz/` |

**Query string**

| Param   | Défaut | Comportement                                                                      |
| ------- | ------ | --------------------------------------------------------------------------------- |
| `q`     | —      | Optionnel. Sous-chaîne insensible à la casse sur le **nom** du tag (`icontains`). |
| `limit` | `20`   | Entier borné entre **1** et **100** (valeur invalide → défaut).                   |

**Réponse `200`** :

```json
{
  "results": ["cinema-scope", "culture"]
}
```

- Tableau **`results`** : noms de tags, tri **alphabétique** par nom.
- Si **`q`** est absent ou vide : les **`limit`** premiers tags en base (ordre alphabétique).
- Si **`q`** est renseigné : uniquement les tags dont le nom **contient** `q`, toujours triés et plafonnés par **`limit`**.

**Exemple**

```http
GET /api/quiz/tags/?q=cult&limit=20
```

Côté front, construire l’URL avec le client HTTP existant (`apiClient`) et les paramètres encodés (`URLSearchParams`).

**Limite actuelle** : sans `q`, la réponse est plafonnée par **`limit`** (max **100**). Si le nombre de tags uniques dépasse ce plafond, il faudra soit plusieurs pages côté backend (évolution), soit compléter par des requêtes avec `q` — à trancher quand le volume le justifiera.

### 2.1 Repli sans catalogue (optionnel)

Une prop **`suggestions?: string[]`** sur le composant reste utile pour **tests**, **Storybook** ou **mode dégradé** si l’appel API échoue — ce n’est plus le chemin nominal.

---

## 3. Architecture frontend

### 3.0 Autocomplétion : pas une requête par lettre

**Non** : on ne doit **pas** appeler l’API à chaque caractère tapé. Deux stratégies possibles :

| Stratégie                               | Principe                                                                                                                                                                                                                                                                 | Quand l’utiliser                                                                                              |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **A — Catalogue en cache (recommandé)** | Une (ou peu) requête(s) pour récupérer une **liste de noms** ; les stocker dans le **cache TanStack Query** (ou état module) ; **filtrer en mémoire** (`includes` / `startsWith` sur la saisie) pour afficher les suggestions. **Aucun appel réseau pendant la frappe.** | Volume raisonnable (ex. jusqu’à la limite `limit` supportée par l’API, aujourd’hui 100 en un appel sans `q`). |
| **B — Recherche côté serveur avec `q`** | Ne pas mettre le préfixe dans la clé de requête à chaque frappe : **debounce** (200–300 ms) et/ou ne lancer la requête qu’à partir de **N caractères** ; le cache par préfixe évite de refetch si l’utilisateur revient sur un préfixe déjà vu.                          | Très gros catalogue, ou catalogue non chargé en entier.                                                       |

En pratique, pour un Burger Quiz, la stratégie **A** est en général la plus simple et la plus fluide : **charger le catalogue une fois** (ex. `GET /api/quiz/tags/?limit=100` sans `q`), `staleTime` long, puis **`TagInput` ne fait que du filtrage local** sur cette liste.

### 3.0.1 Décisions validées

- **Stratégie** : **A — Catalogue en cache**.
- **Règle de matching** : `includes`, insensible à la casse et aux accents.
- **Taille des suggestions** : **top 8**.
- **Ordre d’affichage** : priorité aux correspondances les plus proches (ex. commence par la saisie avant `includes` plus lointain), puis ordre alphabétique.
- **Création** : **free tagging autorisé** (tag nouveau non présent dans le catalogue).
- **Normalisation à l’ajout** : `trim`, suppression des doublons, conservation de la saisie utilisateur.
- **Validation** : longueur d’un tag entre **3** et une borne max (recommandé **32** caractères), avec **15 tags max** par formulaire.
- **Chargement du catalogue** : **lazy**, au premier écran/formulaire qui édite des tags.
- **Rafraîchissement du cache** : invalider `tags.catalog` après create/update qui introduit un **nouveau nom**.
- **Fallback API indisponible** : input utilisable sans suggestions + message discret.
- **Clavier / a11y** : Entrée, virgule, Backspace, navigation flèches, pattern ARIA combobox.

### 3.1 Composant UI

- **`frontend/src/components/common/TagInput/`** (ou `TagField.tsx` au début) : composant **contrôlé** (`value: string[]`, `onChange`), réutilisable sur tout écran qui édite des tags.
- Il reçoit typiquement une liste **`allTagNames: string[]`** (issue du cache) et applique **localement** le filtre sur le texte de l’input ; pas d’effet réseau dans ce composant si le catalogue est déjà fourni.
- Filtrage local recommandé :
  - normaliser `inputValue` et chaque tag (casse + accents) ;
  - calculer un score de proximité (préfixe > inclusion) ;
  - retourner les **8 meilleurs** résultats.
- Pour les tests : props **`suggestions`** ou catalogue mocké ; pas besoin d’API.

### 3.2 Couche données (TanStack Query)

- **`frontend/src/features/quiz/api/tags.ts`** :
  - **`fetchTagCatalog()`** → `GET /api/quiz/tags/?limit=100` (sans `q`) pour remplir le cache du **catalogue** (ajuster `limit` selon l’évolution backend).
  - Optionnel : **`fetchTagSuggestionsByQuery(q: string)`** → `GET /api/quiz/tags/?q=…&limit=20` si vous adoptez la stratégie **B** ou un mode hybride.
- **`useTagCatalog`** (ou équivalent) : `useQuery` avec une clé **stable**, ex. `queryKeys.tags.catalog()`, **`staleTime`** élevé (5–30 min), chargement **lazy** au premier formulaire/écran tags.
- **`TagInput`** (ou un hook léger **`useFilteredTagSuggestions(catalog, inputValue)`**) : **filtrage synchrone** sur `catalog` — pas de `queryKey` dépendant de chaque lettre pour la stratégie A.

### 3.3 Wrapper métier (recommandé)

- **`TagInputWithCatalog`** (nom indicatif) : compose `TagInput` + `useTagCatalog` pour injecter le catalogue mis en cache — **un chargement réseau** pour toute la session (ou jusqu’à invalidation), pas une boucle de requêtes à la saisie.

### 3.4 Formulaires (React Hook Form + Zod)

- Champ au type **`string[]`** (plus de CSV côté formulaire).
- **`Controller`** / **`useController`** pour lier `TagInput` à RHF.
- Schéma Zod : `z.array(z.string().min(3).max(32)).max(15)` + normalisation (`trim`, suppression doublons ; conservation de la saisie pour la casse/accents).
- **Migration** depuis l’ancien champ texte : `defaultValues` à partir de `quiz.tags` (déjà tableau) ; éviter `split(',')` sauf compatibilité temporaire.

---

## 4. Comportement UX (rappels)

- **Validation d’un tag** : Entrée ou virgule (blur optionnel) ; ne pas valider de chaînes vides ; longueur min 3.
- **Suppression** : bouton sur le chip ; retour arrière sur input vide → retirer le dernier tag (pattern courant).
- **Liste de suggestions** : Popover + liste ou `Command` (shadcn), limitée à **8** items ; **free tagging** activé.
- **Accessibilité** : pattern **combobox** (navigation clavier avec flèches, `aria-*`).
- **Doublons** : déduplication côté client après normalisation `trim`.

---

## 5. Invalidation du cache

Après **POST/PUT/PATCH** d’une ressource qui **introduit un nouveau nom de tag** (ou en supprime un), invalider **`queryKeys.tags.catalog()`** (ou équivalent) pour resynchroniser la liste locale. Les mises à jour qui ne font que réutiliser des tags existants n’ont pas besoin d’invalidation immédiate.

---

## 6. Fichiers cibles (implémentation)

| Rôle                                                                     | Emplacement indicatif                                  |
| ------------------------------------------------------------------------ | ------------------------------------------------------ |
| UI chips + input + liste                                                 | `components/common/TagInput/…`                         |
| `fetchTagCatalog` (+ optionnel `fetchTagSuggestionsByQuery`)             | `features/quiz/api/tags.ts`                            |
| `useTagCatalog` (+ optionnel filtre local / `useFilteredTagSuggestions`) | `features/quiz/hooks/…`                                |
| Clés TanStack Query                                                      | `features/quiz/api/query-keys.ts` (ex. `tags.catalog`) |
| Schémas formulaires                                                      | `tags: z.array(z.string())` par ressource              |

Après ajout des fichiers, mettre à jour **`docs/frontend/structure.md`** si besoin.

---

## 7. Prochaines étapes

1. Implémenter `fetchTagCatalog`, `query-keys`, `useTagCatalog`, filtrage local dans `TagInput`, puis wrapper.
2. Migrer progressivement les formulaires (ex. **`BurgerQuizForm`**) vers `string[]` + `TagInput`.
3. Vérifier les tests (composant + hook mockant le catalogue ; pas de dépendance à une requête par frappe).
