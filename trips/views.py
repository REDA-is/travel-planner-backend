from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ml_models.planner import generate_plans
from .serializers import PlanRequestSerializer, ConfirmedTripSerializer
from .models import ConfirmedTrip
import uuid

# Currency exchange rates to MAD
EXCHANGE_RATES = {
    "MAD": 1,
    "USD": 10.2,
    "EUR": 11.1,
    "GBP": 12.5,
    "JPY": 0.072,
}

class PlanView(APIView):
    def post(self, request):
        serializer = PlanRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            print("Validated data:", data)

            currency = data['currency']
            exchange_rate = EXCHANGE_RATES.get(currency, 1)
            mad_budget = data['budget'] * exchange_rate

            result = generate_plans(
                budget=mad_budget,
                region=data['region'],
                lifestyle=data['lifestyle']
            )

            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmTripView(APIView):
    def post(self, request):
        try:
            selected_plan = request.data.get('selectedPlan')
            region = request.data.get('region')
            budget = request.data.get('budget')
            currency = request.data.get('currency')
            lifestyle = request.data.get('lifestyle')

            if not selected_plan or not selected_plan.get('id'):
                return Response({"error": "selectedPlan with id is required"}, status=400)

            trip = ConfirmedTrip.objects.create(
                region=region,
                budget=budget,
                currency=currency,
                lifestyle=lifestyle,
                selected_plan=selected_plan
            )

            serializer = ConfirmedTripSerializer(trip)
            return Response({
                "status": "confirmed",
                "message": "Trip successfully saved!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmedTripsListView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        lifestyle = request.query_params.get('lifestyle')

        trips = ConfirmedTrip.objects.all()

        if region:
            trips = trips.filter(region__iexact=region)
        if lifestyle:
            trips = trips.filter(lifestyle__iexact=lifestyle)

        trips = trips.order_by('-created_at')
        serializer = ConfirmedTripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
from django.core.cache import cache  # Optional if you want caching
from trips.models_mongo import ConfirmedTrip


  