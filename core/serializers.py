import re

from rest_framework import serializers

from core.models import Historic


class CreateParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historic
        fields = ["plate", "reserve"]
        read_only_fields = ["reserve"]

    def validate(self, data):
        if not (re.search("^[A-Z]{3}-\d{4}", data["plate"])):
            raise serializers.ValidationError("Formato de placa não permitido")
        return data


class UpdateParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historic
        fields = ["paid", "left"]


class ListParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historic
        fields = ["id", "plate", "period", "entry_time", "departure_time", "paid", "left"]
