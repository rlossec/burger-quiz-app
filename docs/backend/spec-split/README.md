# Spec API découpée (pilote)

Ce dossier est un **brouillon structuré** pour valider le découpage de la documentation monolithique avant migration éventuelle.

| Source (monolithe) | Rôle |
| --- | --- |
| [`../api-specifications.md`](../api-specifications.md) | Référence endpoints + exemples JSON |
| [`../api-endpoints-et-contraintes.md`](../api-endpoints-et-contraintes.md) | Flux de création, contraintes métier, récapitulatifs |

## Modèles suivis

- Vue transverse : [`../../api-specifications-template.md`](../../api-specifications-template.md)
- Détail par endpoint : [`../../endpoints-specification-template.md`](../../endpoints-specification-template.md)
- Index par module (tableau + liens groupes) : [`../../module-endpoints-index-template.md`](../../module-endpoints-index-template.md)

## Fichiers de ce pilote

| Fichier | Contenu |
| --- | --- |
| [`api-specifications.md`](api-specifications.md) | Auth, formats, erreurs, permissions, **index** modules |
| [`accounts/README.md`](accounts/README.md) | Récap `/api/auth/` + fiches courtes |
| [`quiz/README.md`](quiz/README.md) | Récap `/api/quiz/` + fiches `questions`, `nuggets`, `salt-or-pepper`, `menus`, `additions`, `deadly-burger`, `quizzes`, `contraintes` |

Les libellés **Permissions** dans les fiches endpoints restent alignés sur le monolithe : préciser staff / authentifié lorsque l’implémentation sera figée.
