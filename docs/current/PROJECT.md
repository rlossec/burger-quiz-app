# 🍔 Burger Quiz – Project Control Center

---

## 1. Vision

L'objectif est de pouvoir créer des manches de Burger Quiz, les rassembler dans un ou plusieurs ensembles « Burger Quiz ». Ensuite : interface pour un organisateur pour présenter le flow de l'émission et jouer en vocal avec les joueurs. Puis : animations, suivi du score. Enfin : buzzer et/ou réponses des joueurs via l'interface.

---

## 2. État actuel

**Version :** 0.0

**Fonctionne :**

- Squelette app (backend Django/DRF, frontend React/Vite, Docker, PostgreSQL)
- Modèles quiz (Questions, manches, Burger Quiz)
- API CRUD quiz complète (tous les endpoints implémentés et documentés)
- Tests API quiz complets
- Fixtures et chargement de données

**Manque :**

- Parcours frontend complet (pages BurgerQuizList, BurgerQuizCreate, etc.)
- Session de jeu (V0.2)
- Animations, scores, buzzer

---

## 3. Priorités

1. ~~Structurer (docs, suivi)~~ ✅
2. ~~Endpoints API Quiz~~ ✅
3. Frontend – parcours Création Burger Quiz (V0.1)

---

## 4. Docs de suivi

| Doc                                                        | Rôle                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------ |
| [ROADMAP.md](ROADMAP.md)                                   | Étapes globales (préparation, développement)           |
| [BACKLOG.md](BACKLOG.md)                                   | User stories, parcours, ordre API, lien spec détaillée |
| [IDEAS.md](IDEAS.md)                                       | Idées / améliorations non priorisées                   |
| [../backend/api-reference.md](../backend/api-reference.md) | Référence API (Accounts + Quiz, corps, contraintes)    |
