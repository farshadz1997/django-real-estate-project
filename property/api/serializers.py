from rest_framework import serializers

from ..models import Property, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class PropertyListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    class Meta:
        model = Property
        depth = 1
        fields = (
            "id",
            "title",
            "property_status",
            "address",
            "city",
            "state",
            "description",
            "category",
            "price",
            "bedrooms",
            "bathrooms",
            "garage",
            "sqft",
            "MainPhoto",
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    class Meta:
        model = Property
        exclude = (
            "status",
            "author",
            "views",
            "pub_date",
        )
