from time import sleep
import pytest
from freezegun import freeze_time

from core.models import Historic

pytestmark = pytest.mark.django_db


def test_parking_list(client):
    Historic.objects.create(**{"plate": "AAA-1990"})
    response = client.get("/parking/")
    assert response.status_code == 200


def test_parking_listing_filtered_by_plate(client):
    Historic.objects.create(**{"plate": "AAA-1990"})
    Historic.objects.create(**{"plate": "BBB-1991"})
    Historic.objects.create(**{"plate": "CCC-1992"})

    response = client.get("/parking/?plate=AAA-1990")
    assert response.status_code == 200
    assert len(response.data) == 1


def test_parking_create(client):
    data = {"plate": "AAA-1990"}
    response = client.post("/parking/", data=data)
    assert response.status_code == 201
    assert "reserve" in response.data


def test_parking_create_invalid_plate_format(client):
    data = {"plate": "111-1990"}
    response = client.post("/parking/", data=data)
    assert response.status_code == 400
    assert (
        "Formato de placa não permitido"
        in response.data.get("non_field_errors")[0].__str__()
    )


def test_parking_pay(client):
    instance = Historic.objects.create(**{"plate": "AAA-1990"})
    data = {"paid": True}
    response = client.patch(
        f"/parking/{instance.pk}/checkout/", data=data, content_type="application/json"
    )
    assert response.status_code == 200


@freeze_time("2023-02-24T00:52:04.952459Z")
def test_parking_out(client):
    instance = Historic.objects.create(**{"plate": "AAA-1990", "paid": True})
    data = {"left": True}
    client.patch(
        f"/parking/{instance.pk}/out/", data=data, content_type="application/json"
    )

    instance_updated = Historic.objects.last()
    assert "2023-02-24T00:52:04.952459" in instance_updated.departure_time.isoformat()
    assert True is instance_updated.left


def test_parking_valid_if_parking_period_is_being_displayed(client):
    instance = Historic.objects.create(**{"plate": "AAA-1990", "paid": True})
    sleep(3)
    data = {"left": True}
    client.patch(
        f"/parking/{instance.pk}/out/", data=data, content_type="application/json"
    )
    response_list = client.get("/parking/")    
    assert "0:00:03" in response_list.json()[0].get("period")


def test_parking_validates_payment_was_made_before_registering_departure(client):
    instance = Historic.objects.create(**{"plate": "AAA-1990"})
    data = {"left": True}
    response = client.patch(
        f"/parking/{instance.pk}/out/", data=data, content_type="application/json"
    )
    assert response.status_code == 400
    assert (
        "A saída só pode ser registrada depois que o pagamento for efetuado."
        in response.data
    )
