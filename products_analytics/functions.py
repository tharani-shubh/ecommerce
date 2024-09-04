from django.db.models import Count

from products_analytics.models import Product, Lead

def get_products_based_on_leads_count(products_count, ascending=True):
    products_qs = (Product.objects.annotate(leads_count=Count('leads'))
                   .order_by('leads_count' if ascending else '-leads_count')
    [:products_count])
    return products_qs