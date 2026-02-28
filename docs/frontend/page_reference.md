# Pages et Routes

Structure des pages et URLs du frontend.

**Docs liées :**

- Composants réutilisables : [components.md](components.md)
- Maquettes fil de fer : [wireframes/README.md](wireframes/README.md)

---

## Légende

| Statut | Description    |
| ------ | -------------- |
| ⊘      | Non implémenté |
| 🟡     | En cours       |
| ✅     | Implémenté     |

---

## Routes publiques

| Route                        | Page         | Description          | Maquette                      | Fichier |
| ---------------------------- | ------------ | -------------------- | ----------------------------- | ------- |
| `/login`                     | LoginPage    | Connexion            | [auth.md](wireframes/auth.md) | ⊘       |
| `/register`                  | RegisterPage | Inscription          | [auth.md](wireframes/auth.md) | ⊘       |
| `/auth/activate/:uid/:token` | ActivatePage | Activation du compte | [auth.md](wireframes/auth.md) | ⊘       |

| `/auth/resend-activation` | ResendActivationPage | Renvoi email d'activation | [auth.md](wireframes/auth.md) | ⊘ |
| `/auth/forgot-password` | ForgotPasswordPage | Demande reset mot de passe | [auth.md](wireframes/auth.md) | ⊘ |
| `/auth/password/reset/confirm/:uid/:token` | ResetPasswordPage | Nouveau mot de passe | [auth.md](wireframes/auth.md) | ⊘ |
| `/auth/email-sent` | EmailSentPage | Confirmation envoi email | [auth.md](wireframes/auth.md) | ⊘ |
| `*` | NotFoundPage | Page 404 | ⊘ | ⊘ |

## Routes protégées (auth requise)

### Dashboard

| Route        | Page          | Description                 | Maquette | Fichier |
| ------------ | ------------- | --------------------------- | -------- | ------- |
| `/dashboard` | DashboardPage | Tableau de bord utilisateur | ⊘        | ⊘       |

### Profil utilisateur

| Route                      | Page               | Description             | Maquette                      | Fichier |
| -------------------------- | ------------------ | ----------------------- | ----------------------------- | ------- |
| `/profile`                 | ProfilePage        | Profil utilisateur      | ⊘                             | ⊘       |
| `/profile/edit`            | ProfileEditPage    | Modifier le profil      | ⊘                             | ⊘       |
| `/profile/change-email`    | ChangeEmailPage    | Changer l'email         | [auth.md](wireframes/auth.md) | ⊘       |
| `/profile/change-password` | ChangePasswordPage | Changer le mot de passe | ⊘                             | ⊘       |

### Burger Quiz (CRUD)

#### Quiz

| Route          | Page                 | Description                         | Maquette                                           | Fichier |
| -------------- | -------------------- | ----------------------------------- | -------------------------------------------------- | ------- |
| `/quiz`        | BurgerQuizListPage   | Liste des Burger quiz               | [burger-quiz.md](wireframes/1-quiz/burger-quiz.md) | ⊘       |
| `/quiz/create` | BurgerQuizCreatePage | Créer un Burger quiz                | [burger-quiz.md](wireframes/1-quiz/burger-quiz.md) | ⊘       |
| `/quiz/:id`    | BurgerQuizDetailEdit | Détail + Édition du quiz et manches | [burger-quiz.md](wireframes/1-quiz/burger-quiz.md) | ⊘       |

> **Note** : La route `/quiz/:id/edit` a été fusionnée dans `/quiz/:id` (BurgerQuizDetailEdit).

#### Manches

| Route                     | Page                   | Description                           | Maquette                                                   | Fichier |
| ------------------------- | ---------------------- | ------------------------------------- | ---------------------------------------------------------- | ------- |
| `/nuggets`                | NuggetsListPage        | Liste des manches Nuggets             | [nuggets.md](wireframes/1-quiz/nuggets.md)                 | ⊘       |
| `/nuggets/create`         | NuggetsCreatePage      | Créer une manche Nuggets              | [nuggets.md](wireframes/1-quiz/nuggets.md)                 | ⊘       |
| `/nuggets/:id`            | NuggetsDetailPage      | Détail d'une manche Nuggets           | [nuggets.md](wireframes/1-quiz/nuggets.md)                 | ⊘       |
| `/nuggets/:id/edit`       | NuggetsEditPage        | Modifier une manche Nuggets           | [nuggets.md](wireframes/1-quiz/nuggets.md)                 | ⊘       |
| `/salt-pepper`            | SaltPepperListPage     | Liste des manches Sel ou Poivre       | [salt-or-pepper.md](wireframes/1-quiz/salt-or-pepper.md)   | ⊘       |
| `/salt-pepper/create`     | SaltPepperCreatePage   | Créer une manche Sel ou Poivre        | [salt-or-pepper.md](wireframes/1-quiz/salt-or-pepper.md)   | ⊘       |
| `/salt-pepper/:id`        | SaltPepperDetailPage   | Détail d'une manche Sel ou Poivre     | [salt-or-pepper.md](wireframes/1-quiz/salt-or-pepper.md)   | ⊘       |
| `/salt-pepper/:id/edit`   | SaltPepperEditPage     | Modifier une manche Sel ou Poivre     | [salt-or-pepper.md](wireframes/1-quiz/salt-or-pepper.md)   | ⊘       |
| `/menus`                  | MenusListPage          | Liste des manches Menus               | [menus-menutheme.md](wireframes/1-quiz/menus-menutheme.md) | ⊘       |
| `/menus/create`           | MenusCreatePage        | Créer une manche Menus                | [menus-menutheme.md](wireframes/1-quiz/menus-menutheme.md) | ⊘       |
| `/menus/:id`              | MenusDetailPage        | Détail d'une manche Menus             | [menus-menutheme.md](wireframes/1-quiz/menus-menutheme.md) | ⊘       |
| `/menus/:id/edit`         | MenusEditPage          | Modifier une manche Menus             | [menus-menutheme.md](wireframes/1-quiz/menus-menutheme.md) | ⊘       |
| `/addition`               | AdditionListPage       | Liste des manches Addition            | [addition.md](wireframes/1-quiz/addition.md)               | ⊘       |
| `/addition/create`        | AdditionCreatePage     | Créer une manche Addition             | [addition.md](wireframes/1-quiz/addition.md)               | ⊘       |
| `/addition/:id`           | AdditionDetailPage     | Détail d'une manche Addition          | [addition.md](wireframes/1-quiz/addition.md)               | ⊘       |
| `/addition/:id/edit`      | AdditionEditPage       | Modifier une manche Addition          | [addition.md](wireframes/1-quiz/addition.md)               | ⊘       |
| `/deadly-burger`          | DeadlyBurgerListPage   | Liste des manches Burger de la mort   | [deadly-burger.md](wireframes/1-quiz/deadly-burger.md)     | ⊘       |
| `/deadly-burger/create`   | DeadlyBurgerCreatePage | Créer une manche Burger de la mort    | [deadly-burger.md](wireframes/1-quiz/deadly-burger.md)     | ⊘       |
| `/deadly-burger/:id`      | DeadlyBurgerDetailPage | Détail d'une manche Burger de la mort | [deadly-burger.md](wireframes/1-quiz/deadly-burger.md)     | ⊘       |
| `/deadly-burger/:id/edit` | DeadlyBurgerEditPage   | Modifier une manche Burger de la mort | [deadly-burger.md](wireframes/1-quiz/deadly-burger.md)     | ⊘       |

#### Interludes vidéo

| Route                  | Page                 | Description                 | Maquette                                         | Fichier |
| ---------------------- | -------------------- | --------------------------- | ------------------------------------------------ | ------- |
| `/interludes`          | InterludesListPage   | Liste des interludes vidéo  | [interludes.md](wireframes/1-quiz/interludes.md) | ⊘       |
| `/interludes/create`   | InterludesCreatePage | Créer un interlude vidéo    | [interludes.md](wireframes/1-quiz/interludes.md) | ⊘       |
| `/interludes/:id`      | InterludesDetailPage | Détail d'un interlude vidéo | [interludes.md](wireframes/1-quiz/interludes.md) | ⊘       |
| `/interludes/:id/edit` | InterludesEditPage   | Modifier un interlude vidéo | [interludes.md](wireframes/1-quiz/interludes.md) | ⊘       |

### Session de jeu 🚧

| Route                      | Page              | Description                    | Maquette                                     | Fichier |
| -------------------------- | ----------------- | ------------------------------ | -------------------------------------------- | ------- |
| `/play`                    | PlayHomePage      | Accueil Play (créer/rejoindre) | [README.md](wireframes/2-sessions/README.md) | ⊘       |
| `/play/create`             | CreateSessionPage | Créer une session              | [README.md](wireframes/2-sessions/README.md) | ⊘       |
| `/play/join`               | JoinSessionPage   | Rejoindre une session          | [README.md](wireframes/2-sessions/README.md) | ⊘       |
| `/play/:sessionId/lobby`   | LobbyPage         | Salle d'attente                | [README.md](wireframes/2-sessions/README.md) | ⊘       |
| `/play/:sessionId/game`    | GamePage          | Partie en cours                | [README.md](wireframes/2-sessions/README.md) | ⊘       |
| `/play/:sessionId/results` | ResultsPage       | Résultats de la partie         | [README.md](wireframes/2-sessions/README.md) | ⊘       |

---

## Layout

| Composant  | Description                               | Maquette                          | Fichier |
| ---------- | ----------------------------------------- | --------------------------------- | ------- |
| `<Layout>` | Layout principal (Header + Main + Footer) | [layout.md](wireframes/layout.md) | ⊘       |
| `<Header>` | En-tête avec navigation                   | [layout.md](wireframes/layout.md) | ⊘       |
| `<Nav>`    | Navigation principale                     | [layout.md](wireframes/layout.md) | ⊘       |
| `<Footer>` | Pied de page                              | [layout.md](wireframes/layout.md) | ⊘       |

---

## Composants Burger Quiz

### Composants principaux

| Composant            | Description                            | Utilisé dans       |
| -------------------- | -------------------------------------- | ------------------ |
| `<BurgerQuizForm />` | Formulaire titre/toss/tags             | Create, DetailEdit |
| `<BQDetailCard />`   | Affichage lecture seule des infos quiz | DetailEdit         |
| `<RoundStructure />` | Structure des 5 manches avec slots     | DetailEdit         |
| `<RoundSlot />`      | Slot individuel pour une manche        | RoundStructure     |

### Formulaires de manches (dans modales)

| Composant              | Description                                 |
| ---------------------- | ------------------------------------------- |
| `<NuggetsForm />`      | Formulaire manche Nuggets                   |
| `<SaltOrPepperForm />` | Formulaire manche SP                        |
| `<MenusForm />`        | Formulaire manche Menus (3 slots de thèmes) |
| `<AdditionForm />`     | Formulaire manche Addition                  |
| `<DeadlyBurgerForm />` | Formulaire manche DB                        |

### Composants Menus (structure imbriquée)

| Composant                     | Description                                  |
| ----------------------------- | -------------------------------------------- |
| `<MenuThemeSlot />`           | Slot pour un thème (CL ou TR) dans MenusForm |
| `<MenuThemeInlineForm />`     | Création inline d'un thème dans un slot      |
| `<MenusQuestionInlineForm />` | Question ME dans un MenuThemeInlineForm      |

> **Note Menus** : `MenusForm` contient 3 `MenuThemeSlot` (2 Classique + 1 Troll). Chaque slot permet d'**attacher** un thème existant via `SearchAndSelectMenuTheme` ou de **créer** un thème via `MenuThemeInlineForm`.

### InlineForm pour questions

| Composant                            | Description              | Particularité                       |
| ------------------------------------ | ------------------------ | ----------------------------------- |
| `<NuggetsQuestionInlineForm />`      | Question Nuggets inline  | Par paires, 4 réponses + correcte   |
| `<SaltOrPepperQuestionInlineForm />` | Question SP inline       | Réponse = dropdown des propositions |
| `<MenusQuestionInlineForm />`        | Question Menus inline    | Dans MenuThemeInlineForm            |
| `<AdditionQuestionInlineForm />`     | Question Addition inline | Énoncé + réponse courte             |
| `<DeadlyBurgerQuestionInlineForm />` | Question DB inline       | Énoncé seul                         |

### Composants de recherche/sélection

| Composant                         | Description                             |
| --------------------------------- | --------------------------------------- |
| `<SearchAndSelectNuggets />`      | Recherche et sélection Nuggets          |
| `<SearchAndSelectSaltOrPepper />` | Recherche et sélection SP               |
| `<SearchAndSelectMenus />`        | Recherche et sélection manche Menus     |
| `<SearchAndSelectMenuTheme />`    | Recherche thème (filtre par type CL/TR) |
| `<SearchAndSelectAddition />`     | Recherche et sélection Addition         |
| `<SearchAndSelectDeadlyBurger />` | Recherche et sélection DB               |
| `<SearchAndSelectInterlude />`    | Recherche et sélection interlude        |

### Composants Interludes

| Composant            | Description                                     |
| -------------------- | ----------------------------------------------- |
| `<InterludeForm />`  | Formulaire création/édition d'un interlude      |
| `<InterludeCard />`  | Affichage d'un interlude (avec preview YouTube) |
| `<YouTubePreview />` | Miniature et aperçu d'une vidéo YouTube         |

### Composants Structure (BurgerQuizDetailEdit)

| Composant                 | Description                                             |
| ------------------------- | ------------------------------------------------------- |
| `<QuizStructureEditor />` | Éditeur drag & drop de la structure manches/interludes  |
| `<StructureElement />`    | Élément dans la structure (manche ou interlude)         |
| `<AddInterludes />`       | Bouton/menu pour insérer un interlude dans la structure |
| `<InterludeSlot />`       | Slot d'interlude dans la structure                      |

> **Note Structure** : La structure d'un Burger Quiz est désormais une liste ordonnée d'éléments (manches et interludes). L'utilisateur peut réordonner les éléments par drag & drop et insérer des interludes entre les manches.

---

## Arborescence router.tsx

```tsx
<Routes>
  {/* Public */}
  <Route path="/" element={<HomePage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/register" element={<RegisterPage />} />
  <Route path="/auth/activate/:uid/:token" element={<ActivatePage />} />
  <Route path="/auth/resend-activation" element={<ResendActivationPage />} />
  <Route path="/auth/forgot-password" element={<ForgotPasswordPage />} />
  <Route
    path="/auth/password/reset/confirm/:uid/:token"
    element={<ResetPasswordPage />}
  />
  <Route path="/auth/email-sent" element={<EmailSentPage />} />

  {/* Protected */}
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<DashboardPage />} />

    {/* Profile */}
    <Route path="/profile" element={<ProfilePage />} />
    <Route path="/profile/edit" element={<ProfileEditPage />} />
    <Route path="/profile/change-email" element={<ChangeEmailPage />} />
    <Route path="/profile/change-password" element={<ChangePasswordPage />} />

    {/* Burger Quiz CRUD */}
    <Route path="/quiz" element={<BurgerQuizListPage />} />
    <Route path="/quiz/create" element={<BurgerQuizCreatePage />} />
    <Route path="/quiz/:id" element={<BurgerQuizDetailEdit />} />

    {/* Nuggets */}
    <Route path="/nuggets" element={<NuggetsListPage />} />
    <Route path="/nuggets/create" element={<NuggetsCreatePage />} />
    <Route path="/nuggets/:id" element={<NuggetsDetailPage />} />
    <Route path="/nuggets/:id/edit" element={<NuggetsEditPage />} />

    {/* Sel ou Poivre */}
    <Route path="/salt-pepper" element={<SaltPepperListPage />} />
    <Route path="/salt-pepper/create" element={<SaltPepperCreatePage />} />
    <Route path="/salt-pepper/:id" element={<SaltPepperDetailPage />} />
    <Route path="/salt-pepper/:id/edit" element={<SaltPepperEditPage />} />

    {/* Menus */}
    <Route path="/menus" element={<MenusListPage />} />
    <Route path="/menus/create" element={<MenusCreatePage />} />
    <Route path="/menus/:id" element={<MenusDetailPage />} />
    <Route path="/menus/:id/edit" element={<MenusEditPage />} />

    {/* Addition */}
    <Route path="/addition" element={<AdditionListPage />} />
    <Route path="/addition/create" element={<AdditionCreatePage />} />
    <Route path="/addition/:id" element={<AdditionDetailPage />} />
    <Route path="/addition/:id/edit" element={<AdditionEditPage />} />

    {/* Burger de la mort */}
    <Route path="/deadly-burger" element={<DeadlyBurgerListPage />} />
    <Route path="/deadly-burger/create" element={<DeadlyBurgerCreatePage />} />
    <Route path="/deadly-burger/:id" element={<DeadlyBurgerDetailPage />} />
    <Route path="/deadly-burger/:id/edit" element={<DeadlyBurgerEditPage />} />

    {/* Interludes */}
    <Route path="/interludes" element={<InterludesListPage />} />
    <Route path="/interludes/create" element={<InterludesCreatePage />} />
    <Route path="/interludes/:id" element={<InterludesDetailPage />} />
    <Route path="/interludes/:id/edit" element={<InterludesEditPage />} />

    {/* Play 🚧 */}
    <Route path="/play" element={<PlayHomePage />} />
    <Route path="/play/create" element={<CreateSessionPage />} />
    <Route path="/play/join" element={<JoinSessionPage />} />
    <Route path="/play/:sessionId/lobby" element={<LobbyPage />} />
    <Route path="/play/:sessionId/game" element={<GamePage />} />
    <Route path="/play/:sessionId/results" element={<ResultsPage />} />
  </Route>

  {/* 404 */}
  <Route path="*" element={<NotFoundPage />} />
</Routes>
```

---

## Notes d'implémentation

### Conventions de nommage

- **Pages** : `{Nom}Page.tsx` (ex: `LoginPage.tsx`)
- **Fichiers** : kebab-case (ex: `login-page.tsx`) ou PascalCase selon préférence
- **Routes** : kebab-case pour les URLs (ex: `/forgot-password`)

### Paramètres d'URL

| Paramètre    | Type   | Description                     |
| ------------ | ------ | ------------------------------- |
| `:token`     | string | Token JWT pour activation/reset |
| `:id`        | number | ID du Burger Quiz ou manche     |
| `:sessionId` | string | UUID de la session de jeu       |

### Redirections

| Situation                                        | Redirection                          |
| ------------------------------------------------ | ------------------------------------ |
| Utilisateur non connecté accède à route protégée | → `/login?redirect={url}`            |
| Utilisateur connecté accède à `/login`           | → `/dashboard`                       |
| Après login réussi                               | → `redirect` param ou `/dashboard`   |
| Après inscription                                | → `/login` avec message              |
| Après création quiz                              | → `/quiz/:id` (BurgerQuizDetailEdit) |
