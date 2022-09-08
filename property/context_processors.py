from .models import Property, Category


def global_context(request):
    categories = Category.objects.all()
    property_choices = dict(Property.property_choices)
    return {"categories": categories, "property_choices": property_choices}
