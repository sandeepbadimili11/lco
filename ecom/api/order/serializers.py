from rest_framework import serializers
from .models import Orders

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ('user')
