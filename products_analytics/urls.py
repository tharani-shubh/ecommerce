from django.urls import path, include
from products_analytics.views import Products, Leads, get_leads_between_dates, get_top_products, get_bottom_products, \
    get_products_count_in_leads, sign_up

urlpatterns = [
    path('products/', Products.as_view()),
    path('products/<int:pk>/', Products.as_view()),
    path('leads/', Leads.as_view()),
    path('leads/between-dates', get_leads_between_dates),
    path('products/top/', get_top_products),
    path('products/bottom/', get_bottom_products),
    path('leads/products-count/', get_products_count_in_leads),
    path('sign-up/', sign_up)
]