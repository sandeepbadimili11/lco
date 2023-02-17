from rest_framework import serializers
from .models import Products


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(max_length=None,allow_empty_file=False,required=False,allow_null=True)

    class Meta:
        model = Products
        fields = ('id','name','description','price','image','category')

