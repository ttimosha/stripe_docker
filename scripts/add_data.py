from shop.models import Tax, Discount, Item

def run():
    if len(Discount.objects.all())==0 or len(Tax.objects.all())==0 or len(Item.objects.all())==0:
        disc10 = Discount.objects.create(percent_off = 10)
        disc10.save()
        disc30 = Discount.objects.create(percent_off = 30)
        disc30.save()
        disc50 = Discount.objects.create(percent_off = 50)
        disc50.save()

        tax1 = Tax.objects.create(code = Tax.TaxCode.ESSERVICES, tax_behavior = Tax.TaxBehavior.EXCLUSIVE)
        tax1.save()
        tax2 = Tax.objects.create(code = Tax.TaxCode.SERVICES, tax_behavior = Tax.TaxBehavior.EXCLUSIVE)
        tax2.save()
        tax3 = Tax.objects.create(code = Tax.TaxCode.ESSERVICES, tax_behavior = Tax.TaxBehavior.EXCLUSIVE)
        tax3.save()

        hobbit = Item.objects.create(
            name = 'hobbit', 
            description = 'Greate book for you to read by the fire in winter.',
            price = 1000
        )
        hobbit.save()
        orange = Item.objects.create(
            name = 'orange',
            description = 'Delicious fruit from some warm country!',
            price = 10
        )
        orange.save()
        youtube = Item.objects.create(
            name = 'youtube',
            description = 'YouTube is an American online video sharing and social media platform headquartered in San Bruno, California.',
            price = 250
        )
        youtube.save()
        art = Item.objects.create(
            name = 'art',
            description = '''Art is a diverse range of human activity, and resulting product, that involves creative or imaginative 
                            talent expressive of technical proficiency, beauty, emotional power, or conceptual ideas.''',
            price = 500
        )
        art.save()
