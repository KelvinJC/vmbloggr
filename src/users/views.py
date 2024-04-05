from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .serializers import LoginSerializer, UserSerializer, UserCreateSerializer
from .permissions import IsUserOwner
from . import utils 


class UserCreateView(generics.GenericAPIView):
    ''' Create a user.'''
    serializer_class = UserCreateSerializer

    def post(self, request):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class UserViewSet(utils.ListRetrieveUpdateDestroyViewSet):
    ''' List all users, retrieve, update or delete a single user. '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ('destroy', 'update', 'partial_update') :
            permission_classes = [IsAuthenticated, IsUserOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]  # viewing list of all users is restricted to authenticated users

        return [permission() for permission in permission_classes]
       
    def destroy(self, request, *args, **kwargs):
        ''' Delete a user. Only a user can delete their account.'''
        instance = self.get_object()

        if instance.email != request.user.email:
            return Response(
                {"detail": "You don't have permission to delete this account."},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class LoginAPIView(generics.GenericAPIView):
    ''' Login view.'''
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




