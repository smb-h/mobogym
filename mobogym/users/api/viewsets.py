from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import (
                                            AllowAny,
                                            IsAuthenticated,
                                            IsAdminUser,
                                            IsAuthenticatedOrReadOnly
                                        )
from app.api.permissions import IsOwnerOrReadOnly
from users.api.permissions import IsUserOrReadOnly
from users.models import EcoUser
from app.api.pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from users.api.serializers import (
                            UserDetailSerializer,
                            ProfileSerializer
                        )
from django.shortcuts import get_object_or_404                        

User = get_user_model()


# User ViewSet
class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id = self.request.user.id)

    @action(detail = False, methods = ["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context = {"request": request})
        return Response(status = status.HTTP_200_OK, data = serializer.data)


# Profile ViewSet
class ProfileViewSet(ViewSet):
        
    # List
    # @action(detail = False, methods = ['GET'], permission_classes=[AllowAny])
    def list(self, request):
        queryset = User.objects.all()
        serializer = ProfileSerializer(queryset, many = True)
        return Response(serializer.data)

    # Retrieve
    # @action(detail = True, methods = ['GET'], permission_classes=[IsAuthenticated])
    def retrieve(self, request, id = None):
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        return Response(serializer.data)

    # Create
    # @action(detail = True, methods = ['POST'], permission_classes=[AllowAny])
    def create(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    # Update
    # @action(detail = True, methods = ['PUT'], permission_classes=[IsOwnerOrReadOnly])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileSerializer(
            instance = instance,
            data = request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Partial update
    # @action(detail = True, methods = ['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def partial_update(self, request, *args, **kwargs):
        pass

    # Destroy
    # @action(detail = True, methods = ['DELETE'], permission_classes=[IsOwnerOrReadOnly])
    def destroy(self, request, *args, **kwargs):
        pass        


profile_detail = ProfileViewSet.as_view({
    'GET': 'list',
    'GET': 'retrieve',
    'POST': 'create',
    'PUT': 'update',
    'PATCH': 'partial_update',
    'DELETE': 'destroy'    
    })





