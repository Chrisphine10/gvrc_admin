# -*- encoding: utf-8 -*-
"""
API serializers
"""

from rest_framework import serializers
from apps.home.models import Product, UserProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'