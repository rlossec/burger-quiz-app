from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request


class PlaceholderViewSet(viewsets.ViewSet):
    """
    ViewSet factice pour exposer les routes API du quiz.
    Les tests définissent le comportement attendu ; remplacer par les vrais ViewSets à l'implémentation.
    """

    def list(self, request: Request, *args, **kwargs) -> Response:
        return Response(status=404)

    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        return Response(status=404)

    def create(self, request: Request, *args, **kwargs) -> Response:
        return Response(status=404)

    def update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        return Response(status=404)

    def partial_update(self, request: Request, pk=None, *args, **kwargs) -> Response:
        return Response(status=404)

    def destroy(self, request: Request, pk=None, *args, **kwargs) -> Response:
        return Response(status=404)
