from django.shortcuts import get_object_or_404
from rest_framework import generics
from articles.models import Article
from articles.api.serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
# Permissions
from rest_framework.permissions import (
											AllowAny,
                                            IsAuthenticated,
                                            IsAdminUser,
                                            IsAuthenticatedOrReadOnly,
                                        )
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.http import Http404
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework import permissions
# from rest_framework import filters
# from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter


# Article List
class ArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (permissions.AllowAny,)
    search_fields = ['title', 'content']


# Article detail
class ArticletDetail(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = "id"
    permission_classes = (permissions.AllowAny,)




