# trips/models_mongo.py

from mongoengine import Document, StringField, FloatField, DictField, DateTimeField
import datetime

class ConfirmedTrip(Document):
    region = StringField(required=True)
    budget = FloatField(required=True)
    currency = StringField(required=True)
    lifestyle = StringField(required=True)
    selected_plan = DictField(required=True)  # storing the complete plan as a dict
    created_at = DateTimeField(default=datetime.datetime.utcnow)
