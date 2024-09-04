from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField, SerializerMethodField, \
    BaseSerializer, Serializer, CharField

from products_analytics.models import Product, Lead


class ProductSerializer(ModelSerializer):
    leads_interested = SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if data['price'] < 0:
            raise ValidationError("Price can't be negative")
        return data

    def get_leads_interested(self, obj):
        return obj.leads.count()


class LeadSerializer(ModelSerializer):
    interested_products = PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['created_at']


class LeadProductsCountSerializer(BaseSerializer):
    def to_representation(self, instance):
        return {
            'lead': LeadSerializer(instance).data,
            'products_inquired': instance.interested_products.count()
        }

class UserSerializer(Serializer):
    username = CharField(min_length=4)
    password = CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'])
        return user
