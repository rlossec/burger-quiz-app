"""
Schéma OpenAPI personnalisé.
"""

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import force_instance
from rest_framework.serializers import ModelSerializer


class DeleteBodyAwareSchema(AutoSchema):
    """Émet un corps de requête pour DELETE lorsque le serializer n'est pas un ModelSerializer."""

    def _get_request_body(self, direction: str = "request"):
        if self.method == "DELETE":
            request_serializer = self.get_request_serializer()
            if request_serializer is None:
                return None
            if isinstance(force_instance(request_serializer), ModelSerializer):
                return None
            original = self.method
            self.method = "POST"
            try:
                return super()._get_request_body(direction)
            finally:
                self.method = original
        return super()._get_request_body(direction)
