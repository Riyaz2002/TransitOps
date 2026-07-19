import pytest
from pydantic import ValidationError

from app.schemas.vehicle import VehicleCreate


def test_vehicle_requires_positive_load_capacity():
    with pytest.raises(ValidationError) as error:
        VehicleCreate(
            registration_number="KA 01 AB 1234",
            model_name="Cargo Van",
            vehicle_type="van",
            max_load_capacity=0,
        )
    print(error.value)
    assert "max_load_capacity" in str(error.value)

def test_vehicle_accepts_valid_data():
    vehicle = VehicleCreate(
        registration_number="KA 01 AB 1234",
        model_name="Cargo Van",
        vehicle_type="van",
        max_load_capacity=1200,
    )

    assert vehicle.max_load_capacity == 1200
    assert vehicle.odometer == 0
