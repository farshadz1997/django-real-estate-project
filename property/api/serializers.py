from rest_framework import serializers
from ..models import Property, Category
from users.tasks import send_create_property_email_task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("slug",)


class PropertyListSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.CharField(source="category.title")
    author = serializers.CharField(source="author.username")
    property_status = serializers.CharField(source="get_property_status_display")
    pub_date = serializers.DateTimeField(read_only=True, format="%d %b %Y %H:%M")

    class Meta:
        model = Property
        depth = 1
        extra_kwargs = {"url": {"view_name": "api_property:api_property_detail", "lookup_field": "pk"}}
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
            "author",
            "pub_date",
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Category.get_categories(), source="category.title")
    property_status = serializers.ChoiceField(choices=Property.property_choices, source="get_property_status_display")
    views = serializers.IntegerField(read_only=True)
    author = serializers.CharField(read_only=True, source="author.username")
    pub_date = serializers.DateTimeField(read_only=True, format="%d %b %Y %H:%M")
    update_date = serializers.DateTimeField(read_only=True, format="%d %b %Y %H:%M")

    def create(self, **validated_data):
        category_id = Category.objects.get(title=validated_data["category"]["title"]).id
        validated_data["property_status"] = validated_data["get_property_status_display"]
        validated_data.pop("category")
        validated_data.pop("get_property_status_display")
        return Property.objects.create(author=self.context["request"].user, category_id=category_id, **validated_data)

    def update(self, instance, **validated_data):
        return super().update(instance, validated_data)
    
    def send_email(self, email: str):
        send_create_property_email_task.delay(
            self.validated_data["title"],
            self.validated_data["property_status"],
            self.validated_data["description"],
            [email],
        )

    class Meta:
        model = Property
        exclude = ("status",)
