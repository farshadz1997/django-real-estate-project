from .models import Property, Category
from django.db.models import Max, Min

def global_context(request):
    categories = Category.objects.all()
    property_choices = dict(Property.property_choices)
    max_and_min = Property.objects.aggregate(
            minimum_price=Min("price"), maximum_price=Max("price"), minimum_sqft=Min("sqft"), maximum_sqft=Max("sqft")
        )
    return {"categories": categories, "property_choices": property_choices, "max_and_min": max_and_min}
