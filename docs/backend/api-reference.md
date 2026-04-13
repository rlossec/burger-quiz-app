# Burger Quiz API reference

Welcome to the API documentation for the Burger Quiz backend. This API provides the infrastructure for user management and the core "Burger Quiz" game logic.

## 1. General Information

### 🏛 1.1. Architecture Overview

The backend is built with **Django REST Framework**, organized into two primary modules:

- **Accounts**: Handles identity management, including JWT authentication, user registration, and profile management.
- **Quiz**: Manages the game engine, including the various rounds, question banks, and quiz.

### 📡 1.2. Response Format

- **Transport**: All responses are delivered in **JSON** with the `Content-Type: application/json` header.
- **Single Resources**: The response body contains the serialized object directly.
- **Paginated Lists**: Endpoints returning lists use DRF's `PageNumberPagination` (default size: **20**).

**Pagination Schema:**

JSON

```json
{
  "count": 42,
  "next": "https://example.com/api/quiz/.../?page=2",
  "previous": null,
  "results": []
}
```

### 🔑 1.3. Authentication & Permissions

**JWT**

All requests to **protected** endpoints must include a valid **access** token:

- **Header**: `Authorization: Bearer <your_access_token>`

**Default permissions (Django REST Framework)**

- **`IsAuthenticated`** is the **default** for the API: without a valid JWT, these routes return **401**.
- **Exceptions (`AllowAny`)** — no JWT required, used for:
  - JWT endpoints: `POST /api/auth/jwt/create/`, `POST /api/auth/jwt/refresh/`, `POST /api/auth/jwt/verify/`
  - User registration: `POST /api/auth/users/`
  - Djoser e-mail flows: activation, resend activation, password/username reset and confirm (see § 2.1)

**Quiz vs accounts**

- **`/api/quiz/...`**: all routes require authentication by default (JWT).
- **`/api/auth/...`**: follows the mix above; authenticated routes include `/api/auth/users/me/`, `set_password`, `set_username`, and user list/detail/update/delete where Djoser applies **`CurrentUserOrAdmin`** (non-staff users are typically limited to their own user record).

### ⚠️ 1.4. Typical Errors

The API uses standard **Django REST Framework** exception handling.

| **Code** | **Use Case**                    | **Typical JSON Body**                                                                                                                                                         |
| -------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **400**  | Validation/Business Logic error | Object where keys are **field names** and values are **lists of error strings**. Global errors use the **`non_field_errors`** key.                                            |
| **401**  | Missing or expired JWT          | `{"detail": "Authentication credentials were not provided."}`                                                                                                                 |
| **403**  | Permission denied               | `{"detail": "You do not have permission to perform this action."}`                                                                                                            |
| **404**  | Resource not found              | `{"detail": "Not found."}`                                                                                                                                                    |
| **405**  | Method Not Allowed              | `{"detail": "Method \"POST\" not allowed."}`                                                                                                                                  |
| **429**  | Rate limiting (Throttling)      | **TODO** — throttling is not configured in `REST_FRAMEWORK`; this row documents the **expected** DRF shape once rate limits are added: `{"detail": "Request was throttled."}` |
| **500**  | Server Error                    | Standard Django error response.                                                                                                                                               |

## 2. Accounts

All Accounts endpoints are prefixed with **`/api/auth/`**.

There is 3 section :

1. **Authentification** — JWT (login, refresh, verify), **sign up**, and e-mail flows (activation, resend, password/username reset).
2. **Users Profile** — profile `/me/`, `set_password`, `set_username` (authenticated).
3. **Users — administration** — list and `{id}` routes (staff-oriented; non-staff users only see themselves where Djoser's `CurrentUserOrAdmin` applies).

### 2.1 Authentication

| Method | Endpoint                                  | Description                                       |
| ------ | ----------------------------------------- | ------------------------------------------------- |
| `POST` | `/api/auth/jwt/create/`                   | Create access/refresh pair from credentials       |
| `POST` | `/api/auth/jwt/refresh/`                  | Refresh access token with refresh token           |
| `POST` | `/api/auth/jwt/verify/`                   | Verify token validity                             |
| `POST` | `/api/auth/users/`                        | Sign up                                           |
| `POST` | `/api/auth/users/activation/`             | Activate account (uid + token)                    |
| `POST` | `/api/auth/users/resend_activation/`      | Resend activation e-mail                          |
| `POST` | `/api/auth/users/reset_password/`         | Request password reset (e-mail)                   |
| `POST` | `/api/auth/users/reset_password_confirm/` | Confirm password reset (uid, token, new password) |
| `POST` | `/api/auth/users/reset_username/`         | Request username reset (e-mail)                   |
| `POST` | `/api/auth/users/reset_username_confirm/` | Confirm username reset (uid, token, new username) |

#### 2.1.1. Login

**Endpoint** : `POST /api/auth/jwt/create/`
**Permissions** : `AllowAny`
**Request Body :**

```json
{
  "username": "string",
  "password": "securePassword123"
}
```

**Response** :

- 200
  ```json
  {
    "access": "string",
    "refresh": "string"
  }
  ```

#### 2.1.2. Token refresh

**Endpoint**: `POST /api/auth/jwt/refresh/`
**Permissions**: `AllowAny`
**Body**:

```json
{
  "refresh": "string"
}
```

**Response**:

- **200** — with the current **SimpleJWT** settings (`ROTATE_REFRESH_TOKENS`: `false`), the body contains **only a new access token** (no new refresh token):

  ```json
  {
    "access": "string"
  }
  ```

#### 2.1.3. Token verification

**Endpoint**: `POST /api/auth/jwt/verify/`  
**Authentication**: AllowAny  
**Body**:

```json
{
  "token": "string"
}
```

**Response**:

- 200 `{}`
  if the token is valid.
- 401
  ```json
  {
    "detail": "Token is invalid",
    "code": "token_not_valid"
  }
  ```

#### 2.1.4. Sign up

`POST /api/auth/users/`

Registers a new user in the system.

**Permissions & Headers**

- **Authentication**: `AllowAny`
- **Content-Type**: `application/json`

**Request Body**
| Field | Type | Constraints |
| ---------- |------- | ---------------------------------------------- |
| email | string | Required. Unique, valid email format. |
| username | string | Required. Unique, max 150 chars. |
| password | string | Required. Must follow Django complexity rules. |
| re_password| string | Required. Must match password. |

**Example Request**:

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securePassword123",
  "re_password": "securePassword123"
}
```

**Responses**

- **201 Created**: User successfully created.
  ```json
  {
    "id": 2,
    "email": "user@example.com",
    "username": "johndoe"
  }
  ```
- **400 Bad Request**: Validation failed
  ```json
  {
    "password": ["The two password fields didn't match."],
    "email": ["user with this email already exists."]
  }
  ```

#### 2.1.5. Activation

Implemented by **Djoser** (`ActivationSerializer`). **`SEND_ACTIVATION_EMAIL`** is enabled in settings: new users are **inactive** until they activate via e-mail.

**Activate account** — `POST /api/auth/users/activation/`

- **Permissions**: `AllowAny`
- **Body** (JSON):

| Field   | Type   | Description                                      |
| ------- | ------ | ------------------------------------------------ |
| `uid`   | string | User id encoded by Djoser (from the e-mail link) |
| `token` | string | Token from the e-mail link                       |

**Success**: **204 No Content** (empty body).

**Typical errors**: **400** if `uid` / `token` missing, invalid, expired, or account already active (field-level messages on `uid` / `token` as returned by Djoser).

**Resend activation e-mail** — `POST /api/auth/users/resend_activation/`

- **Permissions**: `AllowAny`
- **Body**: `{ "email": "<registered_email>" }`
- **Success**: **204 No Content** (even if the e-mail is unknown — avoids e-mail enumeration; aligned with Djoser behaviour).

#### 2.1.7. Reset password

Implemented by Djoser: **`SendEmailResetSerializer`** (request) and **`PasswordResetConfirmSerializer`** (confirm) — **no** `re_new_password` in this project (`accounts/serializers/docs.py`).

**Request reset e-mail** — `POST /api/auth/users/reset_password/`

- **Permissions**: `AllowAny`
- **Body**: `{ "email": "user@example.com" }`
- **Success**: **204 No Content**

**Confirm new password** — `POST /api/auth/users/reset_password_confirm/`

- **Permissions**: `AllowAny`
- **Body**:

```json
{
  "uid": "<from_email_link>",
  "token": "<from_email_link>",
  "new_password": "newSecurePassword123"
}
```

- **Success**: **204 No Content** — password is updated; validators from Django / `DJOSER['PASSWORD_VALIDATORS']` apply.
- **Typical errors**: **400** for missing fields, invalid `uid`/`token`, or weak `new_password` (see `accounts/tests/test_reset_password.py`).

#### 2.1.8. Reset username

Same pattern as password reset: e-mail request, then confirm with `uid` / `token` from the link.

**Request reset e-mail** — `POST /api/auth/users/reset_username/`

- **Permissions**: `AllowAny`
- **Body**: `{ "email": "user@example.com" }`
- **Success**: **204 No Content**

**Confirm new username** — `POST /api/auth/users/reset_username_confirm/`

- **Permissions**: `AllowAny`
- **Body**:

```json
{
  "uid": "<from_email_link>",
  "token": "<from_email_link>",
  "new_username": "new_username"
}
```

- **Success**: **204 No Content**
- **Typical errors**: **400** for validation (see `accounts/tests/test_reset_username.py`).

### 2.2 User Profile

Endpoints for reading or updating the **authenticated** user's profile, changing password or username while logged in, and deleting one's own account.

| Method   | Endpoint                        | Description                                     |
| -------- | ------------------------------- | ----------------------------------------------- |
| `GET`    | `/api/auth/users/me/`           | Current user                                    |
| `PUT`    | `/api/auth/users/me/`           | Full update own profile                         |
| `PATCH`  | `/api/auth/users/me/`           | Partial update own profile                      |
| `DELETE` | `/api/auth/users/me/`           | Delete own account (`current_password` in body) |
| `POST`   | `/api/auth/users/set_password/` | Change password (logged in)                     |
| `POST`   | `/api/auth/users/set_username/` | Change username (logged in)                     |

**Permissions (overview)** — Djoser `CurrentUserOrAdmin` for `set_password` and `set_username`: in practice these actions apply to the authenticated user (same idea as `/me/`). Unauthenticated clients receive **401**.

#### 2.2.1. Retrieve current user

**Endpoint**: `GET /api/auth/users/me/`

Retrieves the profile of the currently authenticated user.

**Permissions & Headers**

- Authentication: IsAuthenticated
- Header: Authorization: Bearer <token>

**Responses**:

- **200 OK**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "https://cdn.example.com/media/avatars/johndoe.png"
  }
  ```
- **401 Unauthorized**: Missing or invalid token.

#### 2.2.2. Update current user

**Endpoint**: PUT / PATCH /api/auth/users/me/

Updates the profile of the authenticated user (`PUT` replaces writable fields; `PATCH` only the fields sent).

**Permissions & Headers**

- **Authentication**: `IsAuthenticated`
- **Content-Type**: `multipart/form-data` or `application/json`.

**Request Body**

- `first_name`: `string` (max 150)
- `last_name`: `string` (max 150)
- `email`: `string` (unique)
- `avatar`: `file` (image format)

#### 2.2.3. Delete current user

**Endpoint**: `DELETE /api/auth/users/me/`

Deletes the authenticated account.

**Body**: **`current_password`**

**Responses**:

- **204** on success;
- **400** if `current_password` is missing or invalid; **401** if not authenticated.

#### 2.2.4. Change password (authenticated)

**Endpoint**: `POST /api/auth/users/set_password/`

Changes the password for the logged-in user.

**Permissions & Headers**

- **Authentication**: `IsAuthenticated` (via `CurrentUserOrAdmin` in `DJOSER['PERMISSIONS']`)
- **Content-Type**: `application/json`

**Request body**

| Field              | Type   | Description      |
| ------------------ | ------ | ---------------- |
| `current_password` | string | Current password |
| `new_password`     | string | New password     |

**Responses**

- **204 No Content** on success (empty body).
- **400** validation errors (weak password, wrong `current_password`, etc.).
- **401** if not authenticated.

#### 2.2.5. Change username (authenticated)

**Endpoint**: `POST /api/auth/users/set_username/`

Changes the username for the logged-in user (Djoser `SetUsernameSerializer`).

**Permissions & Headers**

- **Authentication**: `IsAuthenticated` (via `CurrentUserOrAdmin`)
- **Content-Type**: `application/json`

**Request body**

| Field              | Type   | Description         |
| ------------------ | ------ | ------------------- |
| `current_password` | string | Current password    |
| `new_username`     | string | New unique username |

**Responses**

- **204 No Content** on success.
- **400** validation errors.
- **401** if not authenticated.

### 2.3. Users — administration

| Method   | Endpoint                | Description    |
| -------- | ----------------------- | -------------- |
| `GET`    | `/api/auth/users/`      | User list      |
| `GET`    | `/api/auth/users/{id}/` | User detail    |
| `PUT`    | `/api/auth/users/{id}/` | Full update    |
| `PATCH`  | `/api/auth/users/{id}/` | Partial update |
| `DELETE` | `/api/auth/users/{id}/` | Delete account |

#### 2.3.1. User list

**Endpoint**: `GET /api/auth/users/`

- **Staff / superuser**: returns all users (see project tests: `test_user_list.py`).
- **Simple user**: results contain **only their own** row.

**Responses**:

- **200 OK**:
  ```json
  {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "email": "user@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "avatar": "https://cdn.example.com/media/avatars/johndoe.png"
      }
    ]
  }
  ```
- **401 Unauthorized**: missing or invalid token.

#### 2.3.2. User detail

**Endpoint**: `GET /api/auth/users/{id}/`

**Permissions**: same visibility rules as above: only **owner or staff** can load the object; otherwise **404**.

**Response**:

- 200 OK
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "url_or_null"
  }
  ```

#### 2.3.3. Update user (by id) — `PUT` and `PATCH`

| Method  | Endpoint                | Role                                                                    |
| ------- | ----------------------- | ----------------------------------------------------------------------- |
| `PUT`   | `/api/auth/users/{id}/` | **Full update** — replaces writable profile fields for the user `{id}`. |
| `PATCH` | `/api/auth/users/{id}/` | **Partial update** — only the keys you send are applied.                |

**Permissions & Headers**

- **Authentication**: `IsAuthenticated`
- **Header**: `Authorization: Bearer <token>`
- **Content-Type**: `multipart/form-data` (e.g. avatar upload) or `application/json`

**Request body**

| Field        | Type   | Constraints                                                                                                                              |
| ------------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `email`      | string | Unique. With **PUT**, follow your “full resource” contract; with **PATCH**, omit if unchanged. Changing email may require re-activation. |
| `first_name` | string | Optional on **PUT**; max 150 characters. On **PATCH**, include only if updating.                                                         |
| `last_name`  | string | Same as `first_name`.                                                                                                                    |
| `avatar`     | file   | Optional image when using `multipart/form-data`.                                                                                         |

**Example — `PUT`** (`application/json`):

```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Example — `PATCH`** (only fields to change):

```json
{
  "first_name": "Jane"
}
```

**Responses** (both methods)

- **200 OK**: Updated user.
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "https://cdn.example.com/media/avatars/johndoe.png"
  }
  ```
- **400 Bad Request**: Validation error (e.g. duplicate email, invalid email).
  ```json
  {
    "email": ["user with this email already exists."]
  }
  ```
- **401 Unauthorized**: Missing or invalid token.
- **404 Not Found**: No user with this `id`, or you are not allowed to target that user.

#### 2.3.4. Delete user (by id)

**Endpoint**: `DELETE /api/auth/users/{id}/`

Permanently deletes the user `{id}`.

**Permissions & Headers**

- **Authentication**: `IsAuthenticated`
- **Header**: `Authorization: Bearer <token>`
- **Content-Type**: `application/json` (request body with `current_password`)

**Request body**

| Field              | Type   | Constraints                                                                                                |
| ------------------ | ------ | ---------------------------------------------------------------------------------------------------------- |
| `current_password` | string | Required for successful deletion when the server validates it; omission yields **400** with a field error. |

**Example request**:

```json
{
  "current_password": "securePassword123"
}
```

**Responses**

- **204 No Content**: User deleted; empty body.
- **400 Bad Request**: e.g. missing `current_password`.
  ```json
  {
    "current_password": ["This field is required."]
  }
  ```
- **401 Unauthorized**: Not authenticated.
- **403 Forbidden**: Authenticated but not allowed to delete this user (e.g. simple user deleting another user).
  ```json
  {
    "detail": "You do not have permission to perform this action."
  }
  ```
- **404 Not Found**: No user with this `id`.

## 3. Quiz

All Quiz endpoints are prefixed with **`/api/quiz/`**.

**Flow overview (creating a Burger Quiz)**

1. Create rounds: Nuggets, Salt or pepper, Menus, Addition, Deadly burger.
2. Create video interludes (optional): as many as needed.
3. Create a Burger Quiz with **`title`**, **`toss`**, and optional **`tags`**
4. Configure **structure**: `PUT …/structure/` with an `elements` array of `{ "type", "id" }` in the desired order (implicit order).

Rounds and interludes are **independent** resources; the run is wired to a quiz **only** through **`BurgerQuizElement`** rows created by the structure `PUT`.

**Recommended API call order**

1. **Questions and answers**: create Questions with `question_type`, `original`, type-conforming Answers, and optionally `video_url` / `image_url`.
2. **Rounds**: Nuggets (`POST /api/quiz/nuggets/`), Salt or pepper (`POST /api/quiz/salt-or-pepper/`), Menus (three `POST /api/quiz/menu-theme/` then `POST /api/quiz/menus/`), Addition (`POST /api/quiz/additions/`), Deadly burger (`POST /api/quiz/deadly-burgers/`).
3. **Interludes**: create `VideoInterlude` resources with `POST /api/quiz/interludes/`.
4. **Burger Quiz**: `POST /api/quiz/burger-quizzes/` with **`title`**, **`toss`**, optional **`tags`** (no `nuggets_id` / … in the current serializer).
5. **Structure**: `PUT /api/quiz/burger-quizzes/{id}/structure/` — ordered list of **`type` + `id`** (`nuggets`, `video_interlude`, …); rank follows **array position**.

### 3.0.1 End-to-end call sequence (from scratch)

Use this sequence to build one complete Burger Quiz with rounds and interludes.
Replace `BASE_URL` and `TOKEN` with your environment values.

```bash
BASE_URL="http://localhost:8000/api/quiz"
AUTH="Authorization: Bearer <TOKEN>"
JSON="Content-Type: application/json"
```

1. Create Questions (minimum required set):

- NU: 4 questions (or any even number)
- SP: 2+ questions
- ME: enough questions for 3 menu themes
- AD: 1+ questions
- DB: exactly 10 questions

Example (one NU question):

```bash
curl -s -X POST "$BASE_URL/questions/" \
  -H "$AUTH" -H "$JSON" \
  -d '{
    "text": "Capitale de la France ?",
    "question_type": "NU",
    "original": true,
    "answers": [
      {"text": "Paris", "is_correct": true},
      {"text": "Lyon", "is_correct": false},
      {"text": "Marseille", "is_correct": false},
      {"text": "Toulouse", "is_correct": false}
    ]
  }'
```

2. Create rounds:

- `POST /nuggets/` with NU `question_ids`
- `POST /salt-or-pepper/` with `propositions` + SP `question_ids`
- `POST /menu-theme/` three times (2x `CL`, 1x `TR`), then `POST /menus/`
- `POST /additions/` with AD `question_ids`
- `POST /deadly-burgers/` with exactly 10 DB `question_ids`

Examples:

```bash
# Nuggets
curl -s -X POST "$BASE_URL/nuggets/" -H "$AUTH" -H "$JSON" -d '{
  "title": "Nuggets Culture G",
  "question_ids": ["<NU_Q1>", "<NU_Q2>", "<NU_Q3>", "<NU_Q4>"]
}'

# Salt or pepper
curl -s -X POST "$BASE_URL/salt-or-pepper/" -H "$AUTH" -H "$JSON" -d '{
  "title": "Noir, Blanc ou Les deux",
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["<SP_Q1>", "<SP_Q2>"]
}'

# Menus (after creating 3 menu themes)
curl -s -X POST "$BASE_URL/menus/" -H "$AUTH" -H "$JSON" -d '{
  "title": "Menus du jour",
  "menu_1_id": "<THEME_CL_1>",
  "menu_2_id": "<THEME_CL_2>",
  "menu_troll_id": "<THEME_TR_1>"
}'
```

3. Create interludes (optional but typical):

```bash
curl -s -X POST "$BASE_URL/interludes/" -H "$AUTH" -H "$JSON" -d '{
  "title": "Intro Episode 1",
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "autoplay": true,
  "skip_allowed": true
}'
```

4. Create Burger Quiz shell:

```bash
curl -s -X POST "$BASE_URL/burger-quizzes/" -H "$AUTH" -H "$JSON" -d '{
  "title": "Burger Quiz Episode 1",
  "toss": "Presentation and game rules.",
  "tags": ["episode-1", "culture"]
}'
```

Save returned IDs: `<BQ_ID>`, `<NUGGETS_ID>`, `<SP_ID>`, `<MENUS_ID>`, `<ADDITION_ID>`, `<DB_ID>`, and optional `<INTRO_ID>`, `<PUB_ID>`, `<OUTRO_ID>`.

5. Attach everything through structure:

```bash
curl -s -X PUT "$BASE_URL/burger-quizzes/<BQ_ID>/structure/" \
  -H "$AUTH" -H "$JSON" \
  -d '{
    "elements": [
      {"type": "video_interlude", "id": "<INTRO_ID>"},
      {"type": "nuggets", "id": "<NUGGETS_ID>"},
      {"type": "salt_or_pepper", "id": "<SP_ID>"},
      {"type": "video_interlude", "id": "<PUB_ID>"},
      {"type": "menus", "id": "<MENUS_ID>"},
      {"type": "addition", "id": "<ADDITION_ID>"},
      {"type": "deadly_burger", "id": "<DB_ID>"},
      {"type": "video_interlude", "id": "<OUTRO_ID>"}
    ]
  }'
```

6. Verify final result:

```bash
curl -s -H "$AUTH" "$BASE_URL/burger-quizzes/<BQ_ID>/?expand=full"
curl -s -H "$AUTH" "$BASE_URL/burger-quizzes/<BQ_ID>/structure/"
```

Notes:

- Structure order is implicit: array position = `order`.
- Round slugs (`nuggets`, `menus`, etc.) may appear at most once in one structure.
- Interludes may appear multiple times (same UUID reused is allowed).

### 3.1 Questions and answers

| Method   | Endpoint                    | Description                           |
| -------- | --------------------------- | ------------------------------------- |
| `GET`    | `/api/quiz/questions/`      | Question list                         |
| `GET`    | `/api/quiz/questions/{id}/` | Question detail                       |
| `POST`   | `/api/quiz/questions/`      | Create question with answers per type |
| `PUT`    | `/api/quiz/questions/{id}/` | Full replace (idempotent)             |
| `PATCH`  | `/api/quiz/questions/{id}/` | Partial update                        |
| `DELETE` | `/api/quiz/questions/{id}/` | Delete question                       |

#### 3.1.1. Question list

**Endpoint**: `GET /api/quiz/questions/`

**Filters**:

- `original`: `true` | `false`
- `question_type`: `NU` | `SP` | `ME` | `AD` | `DB`
- `search`: string; full-text on question text (question list, add-question modal). Combinable with other filters.

**Expected response**:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "c8d5d5c0-1234-4b8f-9c2a-111111111111",
      "text": "Question Nuggets",
      "question_type": "NU",
      "original": false,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
      "text": "Question SP",
      "question_type": "SP",
      "original": true,
      "explanations": "Explications",
      "video_url": "https://video.com",
      "image_url": "https://image.com",
      "created_at": "2025-01-02T09:30:00Z",
      "updated_at": "2025-01-02T09:30:00Z"
    }
  ]
}
```

#### 3.1.2. Question detail

**Endpoint**: `GET /api/quiz/questions/{id}/`

**Expected response**:

```json
{
  "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
  "text": "Question NU",
  "question_type": "NU",
  "original": true,
  "explanations": "Explications",
  "video_url": "https://video.com",
  "image_url": "https://image.com",
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "answers": [
    { "text": "Paris", "is_correct": true, "image_url": null },
    { "text": "Lyon", "is_correct": false, "image_url": null },
    { "text": "Marseille", "is_correct": false, "image_url": null },
    { "text": "Toulouse", "is_correct": false, "image_url": null }
  ]
}
```

#### 3.1.3. Create question

**Endpoint**: `POST /api/quiz/questions/`

**Body**:

- **Required**: `text`, **`question_type`** (NU | SP | ME | AD | DB) for all questions.
- **Per type**: `answers` required for NU, SP, ME, AD; omitted or empty array for DB. Per-type constraints (answer count, single vs multiple correct, no trick answers for SP/ME/AD) — see `docs/tests/quiz.md` and the Quiz section below.
- **Optional**: `original` (boolean, default **`true`** = authored directly; `false` = from a broadcast), `video_url`, `image_url` (valid URLs), `explanations`.

```json
{
  "text": "Question wording",
  "question_type": "NU",
  "original": true,
  "answers": [
    { "text": "Paris", "is_correct": true, "image_url": null },
    { "text": "Lyon", "is_correct": false, "image_url": null },
    {
      "text": "Marseille",
      "is_correct": false,
      "image_url": "https://example.com/lyon.jpg"
    },
    { "text": "Toulouse", "is_correct": false, "image_url": null }
  ],
  "video_url": "https://example.com/video.mp4",
  "image_url": "https://example.com/image.jpg"
}
```

**Expected response**:

- 201

```json
{
  "id": "d3a9f3b1-5678-4c1b-8f3e-222222222222",
  "text": "Question NU",
  "question_type": "NU",
  "original": true,
  "explanations": "Explications",
  "video_url": "https://video.com",
  "image_url": "https://image.com",
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "answers": [
    { "text": "Paris", "is_correct": true, "image_url": null },
    { "text": "Lyon", "is_correct": false, "image_url": null },
    { "text": "Marseille", "is_correct": false, "image_url": null },
    { "text": "Toulouse", "is_correct": false, "image_url": null }
  ]
}
```

#### 3.1.4. Full question update

**Endpoint**: `PUT /api/quiz/questions/{id}/`

**Body** (example):

```json
{
  "text": "Updated NU question",
  "question_type": "NU",
  "answers": [
    { "text": "Paris", "is_correct": true },
    { "text": "Lyon", "is_correct": false },
    { "text": "Marseille", "is_correct": false },
    { "text": "Toulouse", "is_correct": false }
  ],
  "video_url": "https://video.com/updated",
  "image_url": "https://image.com/updated",
  "original": true,
  "explanations": "Updated explanations"
}
```

**Expected response (200)**: same shape as detail (see § 3.2.2), with updated fields.

#### 3.1.5. Partial question update

**Endpoint**: `PATCH /api/quiz/questions/{id}/`

**Body** (example):

```json
{
  "text": "Libellé corrigé",
  "original": false
}
```

**Expected response (200)**: full question resource with changes; same shape as § 3.2.2.

#### 3.1.6. Delete question

**Endpoint**: `DELETE /api/quiz/questions/{id}/`

- **204 No Content** on success.
- **404 Not Found** si l'`id` n'existe pas.

---

### 3.2 Rounds — Nuggets

| Method          | Endpoint                  | Description                      |
| --------------- | ------------------------- | -------------------------------- |
| `GET`           | `/api/quiz/nuggets/`      | Nuggets round list               |
| `GET`           | `/api/quiz/nuggets/{id}/` | Détail d'une manche Nuggets      |
| `POST`          | `/api/quiz/nuggets/`      | Create                           |
| `PATCH`\| `PUT` | `/api/quiz/nuggets/{id}/` | Update                           |
| `DELETE`        | `/api/quiz/nuggets/{id}/` | Suppression d'une manche Nuggets |

#### 3.2.1. Nuggets round list

**Endpoint**: `GET /api/quiz/nuggets/`

**Expected response**:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-nuggets-1",
      "title": "Culture générale",
      "original": false,
      "author": { "id": 1, "username": "johndoe" },
      "tags": ["culture"],
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z",
      "questions": [
        {
          "id": "uuid-question-1",
          "text": "Question Nuggets 1",
          "question_type": "NU",
          "original": false,
          "explanations": "Optionnel",
          "video_url": "https://video.com/q1",
          "image_url": "https://image.com/q1",
          "answers": [
            { "text": "Réponse A", "is_correct": true },
            { "text": "Réponse B", "is_correct": false },
            { "text": "Réponse C", "is_correct": false },
            { "text": "Réponse D", "is_correct": false }
          ]
        },
        {
          "id": "uuid-question-2",
          "text": "Question Nuggets 2",
          "question_type": "NU",
          "original": true,
          "answers": [
            { "text": "Vrai", "is_correct": true },
            { "text": "Faux", "is_correct": false },
            { "text": "Peut-être", "is_correct": false },
            { "text": "Aucune idée", "is_correct": false }
          ]
        }
      ]
    }
  ]
}
```

#### 3.2.2. Nuggets round detail

**Endpoint**: `GET /api/quiz/nuggets/{id}/`

On **read**, detail returns **full questions** (and answers), not only `question_ids`:

**Expected response**:

```json
{
  "id": "uuid-nuggets-1",
  "title": "Nuggets détail",
  "original": true,
  "questions_count": 4,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question Nuggets 1",
      "question_type": "NU",
      "original": false,
      "explanations": "Optionnel",
      "video_url": "https://video.com/q1",
      "image_url": "https://image.com/q1",
      "answers": [
        { "text": "Réponse A", "is_correct": true },
        { "text": "Réponse B", "is_correct": false },
        { "text": "Réponse C", "is_correct": false },
        { "text": "Réponse D", "is_correct": false }
      ]
    }
  ],
  "burger_quiz_count": 0
}
```

#### 3.2.3. Create Nuggets round

**Endpoint**: `POST /api/quiz/nuggets/`
**Body**:

```json
{
  "title": "Culture générale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

- `title`: required.
- `question_ids` : liste d'UUID de questions existantes, ordre = ordre d'affichage.
- `original` : optionnel (défaut `false`).

**Constraints**: **even** number of questions; all questions must have `question_type = NU`; no duplicates in `question_ids`.

**Response fields**: id, title, ordered questions, `original`. Possible computed fields: `questions_count`, `burger_quiz_count` (or `used_in_burger_quizzes_count`).

#### 3.2.4. Update Nuggets round

**Endpoint**:

- `PATCH /api/quiz/nuggets/{id}/` for partial update (e.g. title, original).
- `PUT /api/quiz/nuggets/{id}/` to fully replace the question list.

**PATCH body** (example):

```json
{
  "title": "Nouveau titre Nuggets",
  "original": true
}
```

**PUT body** (example):

```json
{
  "title": "Culture générale (v2)",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4"]
}
```

**Expected response (200)**: same shape as detail (see § 3.3.2), with full questions.

#### 3.2.5. Delete Nuggets round

**Endpoint**: `DELETE /api/quiz/nuggets/{id}/`

- **204 No Content** on success.
- **404 Not Found** si l'`id` n'existe pas.

### 3.3 Rounds — Salt or pepper

| Method           | Endpoint                         | Description                            |
| ---------------- | -------------------------------- | -------------------------------------- |
| `GET`            | `/api/quiz/salt-or-pepper/`      | List                                   |
| `GET`            | `/api/quiz/salt-or-pepper/{id}/` | Detail                                 |
| `POST`           | `/api/quiz/salt-or-pepper/`      | Create                                 |
| `PATCH` \| `PUT` | `/api/quiz/salt-or-pepper/{id}/` | Update                                 |
| `DELETE`         | `/api/quiz/salt-or-pepper/{id}/` | Suppression d'une manche Sel ou poivre |

#### 3.3.1. Salt or pepper round list

**Endpoint**: `GET /api/quiz/salt-or-pepper/`

**Expected response**:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-sop-1",
      "title": "Noir, Blanc ou Les deux",
      "description": "Optionnel",
      "original": false,
      "author": {
        "id": 1,
        "username": "johndoe"
      },
      "tags": ["culture"],
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z",
      "propositions": ["Noir", "Blanc", "Les deux"],
      "questions": [
        {
          "id": "uuid-question-1",
          "text": "Le corbeau ?",
          "question_type": "SP",
          "original": false,
          "answers": [{ "text": "Noir", "is_correct": true }]
        },
        {
          "id": "uuid-question-2",
          "text": "La neige ?",
          "question_type": "SP",
          "original": true,
          "answers": [{ "text": "Noir", "is_correct": false }]
        }
      ]
    }
  ]
}
```

#### 3.3.2. Salt or pepper round detail

**Endpoint**: `GET /api/quiz/salt-or-pepper/{id}/`

On **read**, detail returns **full questions** and answers, consistent with the choices:

**Expected response**:

```json
{
  "id": "uuid-sop-1",
  "title": "Noir ou Blanc",
  "original": false,
  "propositions": ["Noir", "Blanc"],
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question 1",
      "question_type": "SP",
      "answers": [
        { "text": "Noir", "is_correct": true },
        { "text": "Blanc", "is_correct": false }
      ]
    }
  ],
  "burger_quiz_count": 0
}
```

#### 3.3.3. Create Salt or pepper round

**Endpoint**: `POST /api/quiz/salt-or-pepper/`
**Body** :

```json
{
  "title": "Noir, Blanc ou Les deux",
  "description": "Optionnel",
  "original": false,
  "tags": ["string"],
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

- `title` : m.
- `propositions` (stored as `choice_labels`): required, 2–5 labels, no duplicates.
- `question_ids` : ordered list of questions UUID.
- `tags` : optionnal.
- `original` : optionnal.

**Constraints**: `SP` questions; for each question, 1 correct answer who match one of `propositions` labels exactly.

**Response**: resource with `propositions` / `choice_labels`. Possible computed fields: `burger_quiz_count`, `questions_count`.

#### 3.3.4. Update Salt or pepper round

**Endpoint**:

- `PATCH /api/quiz/salt-or-pepper/{id}/` to change e.g. title.
- `PUT /api/quiz/salt-or-pepper/{id}/` to fully replace the round.

**Body PATCH** (exemple) :

```json
{
  "title": "Noir, Blanc ou Les deux (v2)"
}
```

**Body PUT** (exemple) :

```json
{
  "title": "Noir, Blanc ou Les deux",
  "original": false,
  "description": "Optionnel",
  "propositions": ["Noir", "Blanc", "Les deux"],
  "question_ids": ["uuid-1", "uuid-2"]
}
```

**Expected response (200)**: same shape as detail (see § 3.4.2), with full questions.

#### 3.3.5. Delete Salt or pepper round

**Endpoint**: `DELETE /api/quiz/salt-or-pepper/{id}/`

- **204 No Content** on success.
- **404 Not Found** si l'`id` n'existe pas.

### 3.4 Rounds — Menus

#### 3.4.1. Menu themes

| Method           | Endpoint                     | Description                    |
| ---------------- | ---------------------------- | ------------------------------ |
| `GET`            | `/api/quiz/menu-theme/`      | Theme list                     |
| `GET`            | `/api/quiz/menu-theme/{id}/` | Detail                         |
| `POST`           | `/api/quiz/menu-theme/`      | Create                         |
| `PATCH` \| `PUT` | `/api/quiz/menu-theme/{id}/` | Update                         |
| `DELETE`         | `/api/quiz/menu-theme/{id}/` | Suppression d'un thème de menu |

**POST /api/quiz/menu-theme/** — **Body** (example):

```json
{
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "original": true,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

- `type`: `"CL"` (Classic) or `"TR"` (Troll).
- `original`: optional (default **`true`** = authored directly).
- Questions: type `ME`; order via `question_ids`.

**Computed fields**: `questions_count`, `used_in_menus_count`.

**GET /api/quiz/menu-theme/{id}/** — Detail (example response):

```json
{
  "id": "uuid-theme-1",
  "title": "Histoire de la gastronomie",
  "type": "CL",
  "original": true,
  "questions_count": 3,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question Menu 1",
      "question_type": "ME",
      "answers": [{ "text": "Réponse 1", "is_correct": true }]
    }
  ],
  "used_in_menus_count": 1
}
```

**PUT / PATCH /api/quiz/menu-theme/{id}/** — same body as POST, 200 response with full theme (as above).  
**DELETE /api/quiz/menu-theme/{id}/** — 204 No Content on success.

#### 3.4.2. Menus round (three themes)

| Method           | Endpoint                | Description                    |
| ---------------- | ----------------------- | ------------------------------ |
| `GET`            | `/api/quiz/menus/`      | List                           |
| `GET`            | `/api/quiz/menus/{id}/` | Détail                         |
| `POST`           | `/api/quiz/menus/`      | Création                       |
| `PATCH` \| `PUT` | `/api/quiz/menus/{id}/` | Mise à jour                    |
| `DELETE`         | `/api/quiz/menus/{id}/` | Suppression d'une manche Menus |

**POST /api/quiz/menus/** — **Body** (example):

```json
{
  "title": "Menus du jour",
  "description": "Optionnel",
  "original": false,
  "menu_1_id": "uuid-theme-1",
  "menu_2_id": "uuid-theme-2",
  "menu_troll_id": "uuid-theme-troll"
}
```

**Constraints**: exactly 2 classic menus (`menu_1`, `menu_2` with `type = "CL"`) and 1 troll menu (`menu_troll` with `type = "TR"`); the three IDs must be distinct and exist.

**GET /api/quiz/menus/{id}/** — Detail (example response):

On **read**, detail returns **full themes** with **deserialized questions**:

```json
{
  "id": "uuid-menus-1",
  "title": "Menus du jour",
  "description": "Optionnel",
  "original": false,
  "author": { "id": 1, "username": "johndoe" },
  "tags": ["culture"],
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "menu_1": {
    "id": "uuid-theme-1",
    "title": "Cinéma",
    "type": "CL",
    "original": true,
    "author": { "id": 1, "username": "johndoe" },
    "tags": ["cinéma"],
    "questions": [
      {
        "id": "uuid-q1",
        "text": "Qui a réalisé Pulp Fiction ?",
        "question_type": "ME",
        "answers": [
          { "id": "uuid-a1", "text": "Quentin Tarantino", "is_correct": true }
        ]
      }
    ]
  },
  "menu_2": {
    "id": "uuid-theme-2",
    "title": "Musique",
    "type": "CL",
    "questions": []
  },
  "menu_troll": {
    "id": "uuid-theme-troll",
    "title": "Piège",
    "type": "TR",
    "questions": []
  }
}
```

**PUT / PATCH /api/quiz/menus/{id}/** — same body as POST (with theme IDs), 200 response with full round including themes and deserialized questions.  
**DELETE /api/quiz/menus/{id}/** — 204 No Content on success.

---

### 3.5 Rounds — Addition

| Method           | Endpoint                    | Description              |
| ---------------- | --------------------------- | ------------------------ |
| `GET`            | `/api/quiz/additions/`      | List                     |
| `GET`            | `/api/quiz/additions/{id}/` | Détail                   |
| `POST`           | `/api/quiz/additions/`      | Création                 |
| `PATCH` \| `PUT` | `/api/quiz/additions/{id}/` | Update                   |
| `DELETE`         | `/api/quiz/additions/{id}/` | Delete an Addition round |

#### 3.5.1. Addition round list

**Endpoint**: `GET /api/quiz/additions/`

**Expected response** (paginated list):

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-addition-1",
      "title": "Addition rapide",
      "description": "Optionnel",
      "original": false,
      "author": { "id": 1, "username": "johndoe" },
      "tags": ["culture"],
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z",
      "questions": [
        {
          "id": "uuid-question-1",
          "text": "2 + 2 ?",
          "question_type": "AD",
          "original": false,
          "answers": [{ "text": "4", "is_correct": true }]
        }
      ]
    }
  ]
}
```

#### 3.5.2. Create Addition round

**POST /api/quiz/additions/** — **Body** (example):

```json
{
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

**Constraints**: `AD` questions; no duplicates in `question_ids`. Possible computed fields: `burger_quiz_count`, `questions_count`.

#### 3.5.3. Retrieve Addition round

**GET /api/quiz/additions/{id}/** — Detail (example response):

```json
{
  "id": "uuid-addition-1",
  "title": "Addition rapide",
  "description": "Optionnel",
  "original": false,
  "questions_count": 3,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question AD 1",
      "question_type": "AD",
      "answers": [{ "text": "42", "is_correct": true }]
    }
  ],
  "burger_quiz_count": 0
}
```

#### 3.5.4. Update Addition round

**PUT / PATCH /api/quiz/additions/{id}/** — same body as POST, 200 response with full round (as above).

#### 3.5.5. Delete Addition round

**DELETE /api/quiz/additions/{id}/** — 204 No Content on success.

---

### 3.6 Rounds — Deadly burger

| Method           | Endpoint                         | Description                                |
| ---------------- | -------------------------------- | ------------------------------------------ |
| `GET`            | `/api/quiz/deadly-burgers/`      | List                                       |
| `GET`            | `/api/quiz/deadly-burgers/{id}/` | Détail                                     |
| `POST`           | `/api/quiz/deadly-burgers/`      | Création                                   |
| `PATCH` \| `PUT` | `/api/quiz/deadly-burgers/{id}/` | Mise à jour                                |
| `DELETE`         | `/api/quiz/deadly-burgers/{id}/` | Suppression d'une manche Burger de la mort |

**POST /api/quiz/deadly-burgers/** — **Body** (example):

```json
{
  "title": "Burger de la mort - Finale",
  "original": false,
  "question_ids": ["uuid-1", "uuid-2", "…", "uuid-10"]
}
```

**Constraints**: exactly **10** questions; all type `DB`. Possible computed fields: `burger_quiz_count`.

**GET /api/quiz/deadly-burgers/{id}/** — Detail (example response):

```json
{
  "id": "uuid-db-1",
  "title": "Burger de la mort - Finale",
  "original": false,
  "questions": [
    {
      "id": "uuid-question-1",
      "text": "Question DB 1",
      "question_type": "DB"
    }
  ],
  "burger_quiz_count": 0
}
```

**PUT / PATCH /api/quiz/deadly-burgers/{id}/** — same body as POST, 200 response with full round (as above).  
**DELETE /api/quiz/deadly-burgers/{id}/** — 204 No Content on success.

### 3.7 Video interludes

An interlude is a **standalone** resource (title, YouTube URL, playback options). There is no catalog “type” field (intro / ad / …): role follows from the title, **tags**, and especially **position** in the Burger Quiz structure.

| Method   | Endpoint                     | Description      |
| -------- | ---------------------------- | ---------------- |
| `GET`    | `/api/quiz/interludes/`      | Interlude list   |
| `GET`    | `/api/quiz/interludes/{id}/` | Interlude detail |
| `POST`   | `/api/quiz/interludes/`      | Create interlude |
| `PUT`    | `/api/quiz/interludes/{id}/` | Full update      |
| `PATCH`  | `/api/quiz/interludes/{id}/` | Partial update   |
| `DELETE` | `/api/quiz/interludes/{id}/` | Delete interlude |

#### 3.7.1. Interlude list

**Endpoint**: `GET /api/quiz/interludes/`

**Filters**:

- `search`: text search on title
- `tags`: tag filter (per API conventions)

**Expected response**:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid-interlude-1",
      "title": "Intro Burger Quiz",
      "youtube_url": "https://www.youtube.com/watch?v=xxx",
      "youtube_video_id": "xxx",
      "duration_seconds": 45,
      "autoplay": true,
      "skip_allowed": true,
      "skip_after_seconds": 5,
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    },
    {
      "id": "uuid-interlude-2",
      "title": "Pub Ketchup",
      "youtube_url": "https://www.youtube.com/watch?v=yyy",
      "youtube_video_id": "yyy",
      "duration_seconds": 30,
      "autoplay": true,
      "skip_allowed": true,
      "skip_after_seconds": null,
      "created_at": "2025-01-02T09:00:00Z",
      "updated_at": "2025-01-02T09:00:00Z"
    }
  ]
}
```

#### 3.7.2. Interlude detail

**Endpoint**: `GET /api/quiz/interludes/{id}/`

**Expected response**:

```json
{
  "id": "uuid-interlude-1",
  "title": "Intro Burger Quiz",
  "youtube_url": "https://www.youtube.com/watch?v=xxx",
  "youtube_video_id": "xxx",
  "duration_seconds": 45,
  "autoplay": true,
  "skip_allowed": true,
  "skip_after_seconds": 5,
  "author": { "id": 1, "username": "johndoe" },
  "tags": ["intro", "officiel"],
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z"
}
```

#### 3.7.3. Create interlude

**Endpoint**: `POST /api/quiz/interludes/`

**Body**:

```json
{
  "title": "Intro Burger Quiz",
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "duration_seconds": 45,
  "autoplay": true,
  "skip_allowed": true,
  "skip_after_seconds": 5,
  "tags": ["intro", "officiel"]
}
```

- `title`: required.
- `youtube_url`: required, valid YouTube URL.
- `duration_seconds`: optional (may be fetched via YouTube API on the client).
- `autoplay`: optional (default `true`).
- `skip_allowed`: optional (default `true`).
- `skip_after_seconds`: optional (seconds before skip is allowed).
- `tags`: optional.

**201 response**: same shape as detail (see § 3.1.2).

**Note**: `youtube_video_id` is derived automatically from `youtube_url`.

#### 3.7.4. Update interlude

**Endpoint**: `PUT /api/quiz/interludes/{id}/` or `PATCH /api/quiz/interludes/{id}/`

**PATCH body** (example):

```json
{
  "title": "Intro Burger Quiz v2",
  "skip_after_seconds": 10
}
```

**200 response**: same shape as detail.

#### 3.7.5. Delete interlude

**Endpoint**: `DELETE /api/quiz/interludes/{id}/`

- **204 No Content** on success.
- **400 Bad Request** if the interlude is used by one or more Burger Quizzes (per deletion policy).
- **404 Not Found** if `id` does not exist.

---

### 3.8 Burger Quiz

| Method           | Endpoint                         | Description                                             |
| ---------------- | -------------------------------- | ------------------------------------------------------- |
| `GET`            | `/api/quiz/burger-quizzes/`      | List (with `created_at`, `updated_at` for sort/display) |
| `GET`            | `/api/quiz/burger-quizzes/{id}/` | Détail                                                  |
| `POST`           | `/api/quiz/burger-quizzes/`      | Création                                                |
| `PATCH` \| `PUT` | `/api/quiz/burger-quizzes/{id}/` | Update                                                  |
| `DELETE`         | `/api/quiz/burger-quizzes/{id}/` | Delete a Burger Quiz                                    |

#### 3.8.1. Create Burger quiz

**POST /api/quiz/burger-quizzes/** — **Body**

```json
{
  "title": "Burger PCaT Episode 1",
  "toss": "Toss description or instructions.",
  "tags": ["humour", "culture"]
}
```

- **`toss`**: required.
- **`title`**, **`tags`**: optional.

**201 response**: `id`, `title`, `toss`, `author`, `tags`, `created_at`, `updated_at`, **`structure`** (see below).

#### 3.8.2. Retrieve Burger quiz

**GET /api/quiz/burger-quizzes/{id}/**

- **`structure`**: built from **`BurgerQuizElement`** rows. **Empty array `[]`** until the first successful **`PUT …/structure/`**.
- **`?expand=full`**: each structure item includes the nested object under the type key (`nuggets`, `video_interlude`, …), same helper as **`GET …/structure/`**.

```json
{
  "id": "uuid-bq-1",
  "title": "Burger PCaT Episode 1",
  "toss": "Description ou consigne du toss.",
  "author": { "id": 1, "username": "johndoe" },
  "tags": ["humour", "culture"],
  "created_at": "2025-01-02T09:30:00Z",
  "updated_at": "2025-01-02T09:30:00Z",
  "structure": []
}
```

Example **after** `PUT …/structure/` with **`?expand=full`** (shape only; payloads mirror `/structure/`):

```json
{
  "id": "uuid-bq-1",
  "title": "Burger PCaT Episode 1",
  "toss": "…",
  "author": { "id": 1, "username": "johndoe" },
  "tags": [],
  "created_at": "…",
  "updated_at": "…",
  "structure": [
    {
      "order": 1,
      "type": "video_interlude",
      "id": "uuid-intro",
      "video_interlude": {
        "id": "uuid-intro",
        "title": "Intro",
        "youtube_video_id": "abc123"
      }
    },
    {
      "order": 2,
      "type": "nuggets",
      "id": "uuid-nuggets",
      "nuggets": { "id": "uuid-nuggets", "title": "Culture G" }
    }
  ]
}
```

#### 3.8.3. Update Burger quiz

**PUT / PATCH /api/quiz/burger-quizzes/{id}/** — Body: **`title`**, **`toss`**, **`tags`** (same rules as POST); response shape as **GET** detail.

#### 3.8.4. Delete Burger quiz

**DELETE /api/quiz/burger-quizzes/{id}/** — 204 No Content on success.

### 3.9 Burger Quiz structure

| Method | Endpoint                                   | Description       |
| ------ | ------------------------------------------ | ----------------- |
| `GET`  | `/api/quiz/burger-quizzes/{id}/structure/` | Read structure    |
| `PUT`  | `/api/quiz/burger-quizzes/{id}/structure/` | Replace structure |

#### 3.9.1. Read structure

**Endpoint**: `GET /api/quiz/burger-quizzes/{id}/structure/`

**Description**: Retrieve quiz structure.

**Expected response**:

```json
{
  "burger_quiz_id": "uuid-bq-1",
  "elements": [
    {
      "order": 1,
      "type": "video_interlude",
      "id": "uuid-intro",
      "video_interlude": {
        "id": "uuid-intro",
        "title": "Intro",
        "youtube_video_id": "abc123"
      }
    },
    {
      "order": 2,
      "type": "nuggets",
      "id": "uuid-nuggets",
      "nuggets": { "id": "uuid-nuggets", "title": "Culture G" }
    },
    {
      "order": 3,
      "type": "video_interlude",
      "id": "uuid-pub-1",
      "video_interlude": {
        "id": "uuid-pub-1",
        "title": "Pub Ketchup",
        "youtube_video_id": "def456"
      }
    },
    {
      "order": 4,
      "type": "addition",
      "id": "uuid-addition",
      "addition": { "id": "uuid-addition", "title": "Addition rapide" }
    }
  ]
}
```

**Fields**:

- `order`: rank 1…n.
- `type` : `nuggets` | `salt_or_pepper` | `menus` | `addition` | `deadly_burger` | `video_interlude`.
- `id`: UUID of referenced object.
- Key matching `type` (for a round) or `video_interlude`: minimal read object.

#### 3.9.2. Update structure

**Endpoint**: `PUT /api/quiz/burger-quizzes/{id}/structure/`

**Description**: Replace the structure of rounds and interludes.

**Order** is **implicit**: **array position** in `elements` sets `order` (1 = first item).

**Body** (shape supported by the API):

```json
{
  "elements": [
    { "type": "video_interlude", "id": "uuid-intro" },
    { "type": "nuggets", "id": "uuid-nuggets" },
    { "type": "salt_or_pepper", "id": "uuid-sp" },
    { "type": "video_interlude", "id": "uuid-pub" }
  ]
}
```

- Each item must be **`{ "type": "<slug>", "id": "<uuid>" }`** where **`type`** is one of: `nuggets`, `salt_or_pepper`, `menus`, `addition`, `deadly_burger`, `video_interlude`.
- For a **round**, **`id`** is the UUID of the **concrete** round object (Nuggets, SaltOrPepper, …), which matches **`Round.id`** and the corresponding **`Round`** row.

**Validation rules** (current `BurgerQuizStructureSerializer`):

- Each **round slug** (`nuggets`, `menus`, …) may appear **at most once**; the same round **UUID** cannot appear twice.
- Each **`id`** must refer to an **existing** object of the given **`type`** (Nuggets row, `VideoInterlude`, …).
- **Interludes**: only **`{ "type": "video_interlude", "id": "<uuid>" }`** is accepted

**200 response**: same shape as read (see § 3.9.1).

**Errors**:

- **400 Bad Request**: duplicate round slug/UUID, unknown `id` / `type`, malformed payload, missing `elements`.
- **404 Not Found**: Burger Quiz not found.

---

### 3.10 Quiz recap — Constraints per round

| Round              | Constraint                                                                |
| ------------------ | ------------------------------------------------------------------------- |
| **Nuggets**        | Nombre **pair** de questions ; type `NU`. 4 réponses avec 1 seul correcte |
| **Salt or pepper** | 2–5 choices; consistent answers; type `SP`.                               |
| **Menus**          | 2 menus classiques + 1 menu troll ; questions des thèmes type `ME`.       |
| **Addition**       | Questions type `AD`.                                                      |
| **Deadly burger**  | Exactly **10** questions; type `DB`.                                      |

---
