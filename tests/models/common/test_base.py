"""Test harmony.models.common.base."""

from harmony.models.common.base import WaldieBase


class WaldieTestModel(WaldieBase):
    """Test model."""

    in_snake_case: str


def test_waldie_base() -> None:
    """Test mode dumps."""
    # Given
    test_model = WaldieTestModel(in_snake_case="test")
    # When
    model_dump = test_model.model_dump()
    model_dump_string = test_model.model_dump_json()
    # Then
    assert model_dump["inSnakeCase"] == "test"
    assert "in_snake_case" not in model_dump_string
    assert "inSnakeCase" in model_dump_string
    # When
    model_dump = test_model.model_dump(by_alias=False)
    model_dump_string = test_model.model_dump_json(by_alias=False)
    # Then
    assert model_dump["in_snake_case"] == "test"
    assert "inSnakeCase" not in model_dump_string
    assert "in_snake_case" in model_dump_string
    # When
    model_dump = test_model.model_dump(by_alias=4)
    model_dump_string = test_model.model_dump_json(by_alias={})
    # Then
    assert model_dump["inSnakeCase"] == "test"
    assert "in_snake_case" not in model_dump_string
    assert "inSnakeCase" in model_dump_string
