from rest_framework import mixins, viewsets

class ListRetrieveUpdateDestroyViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `destroy`, `update`,
    `partial_update`,and `list` actions.
    """
    pass