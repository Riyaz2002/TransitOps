import jwt

from app.core.security import ALGORITHM, hash_password, hash_token_id, verify_password


def test_password_can_be_verified_but_wrong_password_cannot():
    hashed_password = hash_password("CorrectHorseBatteryStaple")

    assert verify_password("CorrectHorseBatteryStaple", hashed_password) is True
    assert verify_password("not-the-password", hashed_password) is False


def test_hash_token_id_is_deterministic_and_not_the_original_value():
    token_id = "a-token-id"

    result = hash_token_id(token_id)

    assert result == hash_token_id(token_id)
    print(result)
    assert result != token_id
    assert len(result) == 64
