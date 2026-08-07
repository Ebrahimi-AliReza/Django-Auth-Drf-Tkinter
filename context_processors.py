from services.models import Category


def general_objects(request):
    categories=Category.objects.all()
    context={'categories':categories}
    return context