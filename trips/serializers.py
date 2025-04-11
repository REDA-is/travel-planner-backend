from rest_framework import serializers

class PlanRequestSerializer(serializers.Serializer):
    budget = serializers.FloatField()
    currency = serializers.CharField()
    region = serializers.CharField()
    lifestyle = serializers.CharField()

class ConfirmTripSerializer(serializers.Serializer):
    region = serializers.CharField()
    budget = serializers.FloatField()
    currency = serializers.CharField()
    lifestyle = serializers.CharField()
    selectedPlan = serializers.JSONField()


class ConfirmTripByIdSerializer(serializers.Serializer):
    plan_id = serializers.CharField()
    region = serializers.CharField()
    currency = serializers.CharField()
    budget = serializers.FloatField()
    lifestyle = serializers.CharField()

from .models import ConfirmedTrip

class ConfirmedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmedTrip
        fields = '__all__'
