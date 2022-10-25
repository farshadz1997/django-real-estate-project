from rest_framework import serializers

from ..models import Property, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class PropertyListSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SerializerMethodField()
    
    def get_category(self, obj):
        return obj.category.title
    
    class Meta:
        model = Property
        depth = 1
        extra_kwargs = {"url": {"view_name": "property:api_property_detail", "lookup_field": "pk"}}
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
            "url",
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
