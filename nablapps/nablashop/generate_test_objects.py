import faker

from .models import Category, Product

text = faker.text()


def create():
    daljer, _ = Category.objects.get_or_create(
        name="Daljer", description="Her er masse daljer", pk=2
    )
    kompendier, _ = Category.objects.get_or_create(
        name="Kompendier", description="Her er masse kompendier", pk=3
    )

    for i in range(1, 6):
        name = "Dalje %d"
        dalje, _ = Product.objects.get_or_create(
            name=(name % i), category=daljer, pk=i, description=text
        )
        dalje.photo.name = "product_photo/medal.jpg"
        dalje.save()

    for i in range(6, 11):
        name = "Kompendium %d"
        k, _ = Product.objects.get_or_create(
            name=(name % (i - 5)), category=kompendier, pk=i, description=text
        )
        k.photo.name = "product_photo/kompendium.jpg"
        k.save()

    print("Objects generated")
