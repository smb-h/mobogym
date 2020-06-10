from rest_framework import serializers
from articles.models import Article
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
    BooleanField
)

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
import os
import jdatetime

User = get_user_model()


# Article Serializer
class ArticleSerializer(serializers.ModelSerializer):


    # Meta
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'image',
            'author',
            'content',
            'summary',
            'status',
            'read_time',
            'publish',
            'slug',
            'created',
            'updated',
        ]
        read_only_fields = ("created", "updated", "slug", "id")



