from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from products_analytics.functions import get_products_based_on_leads_count
from products_analytics.models import Product, Lead
from products_analytics.serializers import ProductSerializer, LeadSerializer, LeadProductsCountSerializer, \
    UserSerializer


class Products(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            try:
                product = Product.objects.get(id=pk)
                product_serializer = ProductSerializer(instance=product)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            products_qs = Product.objects.all()
            product_serializer = ProductSerializer(instance=products_qs, many=True)
        return Response(product_serializer.data)

    def post(self, request):
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        return Response(product_serializer.errors)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        return Response(product_serializer.errors)

    def patch(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        return Response(product_serializer.errors)

    def delete(self, _request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class Leads(APIView):

    def post(self, request):
        lead_serializer = LeadSerializer(data=request.data)
        if lead_serializer.is_valid():
            lead_serializer.save()
            return Response(lead_serializer.data)
        return Response(lead_serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leads_between_dates(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not (start_date and end_date):
        return Response({'error': 'Both start and end dates are required'}, status=status.HTTP_400_BAD_REQUEST)
    start_date_obj = datetime.strptime(start_date, "%d/%m/%Y").date()
    end_date_obj = datetime.strptime(end_date, "%d/%m/%Y").date()
    if start_date_obj > end_date_obj:
        return Response({'error': 'Start date should be date before end date'}, status=status.HTTP_400_BAD_REQUEST)
    leads_qs = Lead.objects.filter(created_at__gte=start_date_obj, created_at__lte=end_date_obj)
    lead_serializer = LeadSerializer(instance=leads_qs, many=True)
    return Response(lead_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_top_products(request):
    products_count = request.GET.get('page_size', 10)
    top_product_qs = get_products_based_on_leads_count(products_count, ascending=False)
    product_serializer = ProductSerializer(top_product_qs, many=True)
    return Response(product_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bottom_products(request):
    products_count = request.GET.get('page_size', 10)
    bottom_product_qs = get_products_based_on_leads_count(products_count, ascending=True)
    product_serializer = ProductSerializer(bottom_product_qs, many=True)
    return Response(product_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_products_count_in_leads(request):
    leads_qs = Lead.objects.all()
    lead_serializer = LeadProductsCountSerializer(leads_qs, many=True)
    return Response(lead_serializer.data)


@api_view(['POST'])
def sign_up(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response({"message": "user created successfully"})
    return Response(user_serializer.errors, status=status.HTTP_404_NOT_FOUND)