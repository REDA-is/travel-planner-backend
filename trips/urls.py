from django.urls import path
from .views import PlanView, ConfirmTripView, ConfirmedTripsListView


urlpatterns = [
    path('plan/', PlanView.as_view(), name='generate-plan'),
    path('confirm-trip/', ConfirmTripView.as_view(), name='confirm-trip'),
    path('confirmed-trips/', ConfirmedTripsListView.as_view(), name='confirmed-trips'),
]
