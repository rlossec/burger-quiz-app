# Constantes partagées pour les tests du module quiz.
# Alignées sur docs/backend/api-reference.md.

# Message DRF lorsque les credentials ne sont pas fournis (routes privées)
AUTHENTICATION_MISSING = "Authentication credentials were not provided."

MANDATORY_FIELD_ERROR_MESSAGE = "Ce champ est obligatoire."

# Messages d'erreur métier (contraintes manches)
NUGGETS_EVEN_QUESTIONS = "Le nombre de questions doit être pair."
NUGGETS_QUESTION_TYPE = "Toutes les questions doivent être de type Nuggets (NU)."
SALT_OR_PEPPER_PROPOSITIONS_COUNT = "Entre 2 et 5 propositions requises."
SALT_OR_PEPPER_QUESTION_TYPE = "Toutes les questions doivent être de type Sel ou Poivre (SP)."
DEADLY_BURGER_TEN_QUESTIONS = "La manche Burger de la mort doit contenir exactement 10 questions."
DEADLY_BURGER_QUESTION_TYPE = "Toutes les questions doivent être de type Burger de la mort (DB)."
ADDITION_QUESTION_TYPE = "Toutes les questions doivent être de type Addition (AD)."
MENU_THEME_QUESTION_TYPE = "Toutes les questions doivent être de type Menu (ME)."
MENUS_TWO_CLASSIC_ONE_TROLL = "La manche Menus doit avoir 2 menus classiques et 1 menu troll."
BURGER_QUIZ_AT_LEAST_ONE_ROUND = "Au moins une manche doit être fournie."

DUPLICATE_QUESTION_IDS_ERROR_MESSAGE = "Les IDs de questions ne doivent pas être dupliqués."
NONE_EXISTENT_QUESTION_ID_ERROR_MESSAGE = "Les IDs de questions ne doivent pas être inexistants."

# Types de questions (enums)
QUESTION_TYPE_NU = "NU"
QUESTION_TYPE_SP = "SP"
QUESTION_TYPE_ME = "ME"
QUESTION_TYPE_AD = "AD"
QUESTION_TYPE_DB = "DB"

# Types de thème menu
MENU_TYPE_CL = "CL"
MENU_TYPE_TR = "TR"

# Export pour tests
__all__ = [
    "AUTHENTICATION_MISSING",
    "MANDATORY_FIELD_ERROR_MESSAGE",
    "QUESTION_TYPE_NU",
    "QUESTION_TYPE_SP",
    "QUESTION_TYPE_ME",
    "QUESTION_TYPE_AD",
    "QUESTION_TYPE_DB",
    "MENU_TYPE_CL",
    "MENU_TYPE_TR",
]
