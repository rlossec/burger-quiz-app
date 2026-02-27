# Mixins réutilisables pour les tests du module quiz.
# Chaque mixin peut être intégré dans les fichiers de test existants.

from .auth import AuthRequiredMixin
from .author import (
    AuthorAutoAssignOnCreateMixin,
    AuthorReadOnlyOnCreateMixin,
    AuthorInDetailResponseMixin,
    AuthorInListResponseMixin,
    AuthorFilterMixin,
    AuthorNotChangedOnUpdateMixin,
)
from .tags import (
    TagsOnCreateMixin,
    TagsInDetailResponseMixin,
    TagsInListResponseMixin,
    TagsFilterMixin,
    TagsUpdateMixin,
)
from .timestamps import (
    TimestampsInDetailResponseMixin,
    TimestampsInListResponseMixin,
    TimestampsReadOnlyMixin,
)

__all__ = [
    # Auth
    "AuthRequiredMixin",
    # Author
    "AuthorAutoAssignOnCreateMixin",
    "AuthorReadOnlyOnCreateMixin",
    "AuthorInDetailResponseMixin",
    "AuthorInListResponseMixin",
    "AuthorFilterMixin",
    "AuthorNotChangedOnUpdateMixin",
    # Tags
    "TagsOnCreateMixin",
    "TagsInDetailResponseMixin",
    "TagsInListResponseMixin",
    "TagsFilterMixin",
    "TagsUpdateMixin",
    # Timestamps
    "TimestampsInDetailResponseMixin",
    "TimestampsInListResponseMixin",
    "TimestampsReadOnlyMixin",
]
