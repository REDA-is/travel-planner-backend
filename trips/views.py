from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ml_models.planner import generate_plans
from .serializers import PlanRequestSerializer
from trips.models_mongo import ConfirmedTrip  # MongoEngine model
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

            # ✅ Add UUID to each generated plan
            for plan in result["plans"]:
                plan["id"] = str(uuid.uuid4())

            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmTripView(APIView):
    def post(self, request):
        try:
            selected_plans = request.data.get('selectedPlans')
            region = request.data.get('region')
            budget = request.data.get('budget')
            currency = request.data.get('currency')
            lifestyle = request.data.get('lifestyle')

            if not selected_plans or not isinstance(selected_plans, list):
                return Response({"error": "selectedPlans must be a list of plans"}, status=400)

            saved = []

            for plan in selected_plans:
                if not plan.get("id"):
                    continue  # Skip plans without ID

                trip = ConfirmedTrip(
                    region=region,
                    budget=budget,
                    currency=currency,
                    lifestyle=lifestyle,
                    selected_plan=plan
                )
                trip.save()
                saved.append({
                    "id": str(trip.id),
                    "title": trip.selected_plan.get("title"),
                    "region": trip.region,
                    "lifestyle": trip.lifestyle
                })

            return Response({
                "status": "confirmed",
                "message": f"{len(saved)} trip(s) successfully saved!",
                "data": saved
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmedTripsListView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        lifestyle = request.query_params.get('lifestyle')

        filters = {}
        if region:
            filters['region'] = region
        if lifestyle:
            filters['lifestyle'] = lifestyle

        try:
            trips = ConfirmedTrip.objects(**filters).order_by('-created_at')

            results = []
            for trip in trips:
                results.append({
                    "id": str(trip.id),
                    "region": trip.region,
                    "budget": trip.budget,
                    "currency": trip.currency,
                    "lifestyle": trip.lifestyle,
                    "selected_plan": trip.selected_plan,
                    "created_at": trip.created_at
                })

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
