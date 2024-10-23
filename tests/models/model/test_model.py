"""Test harmony.models.model.HarmonyModel."""

import os

import pytest

from harmony.models.model import (
    HarmonyModel,
    HarmonyModelAPIType,
    HarmonyModelData,
    HarmonyModelPrice,
)


def test_valid_harmony_model() -> None:
    """Test valid HarmonyModel."""
    # Given
    api_type: HarmonyModelAPIType = "openai"
    data = HarmonyModelData(
        base_url="https://example.com",
        api_key="api_key",
        api_type=api_type,
        api_version="v1",
        temperature=0.1,
        top_p=0.2,
        max_tokens=100,
        default_headers={"Content-Type": "application/json"},
        price=HarmonyModelPrice(
            prompt_price_per_1k=0.1,
            completion_token_price_per_1k=0.2,
        ),
    )
    # When
    name = "model"
    description = "description"
    model = HarmonyModel(
        id="wm-1",
        name=name,
        description=description,
        data=data,
        type="model",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    # Then
    assert model.id == "wm-1"
    assert model.name == name
    assert model.description == description
    assert model.data == data
    assert model.type == "model"
    assert model.tags == ["tag1", "tag2"]
    assert model.requirements == ["requirement1", "requirement2"]
    assert model.api_key == "api_key"
    assert model.price == [0.1, 0.2]
    # When
    model_dump = model.model_dump()
    # Then
    assert model_dump["id"] == "wm-1"
    assert model_dump["name"] == name
    assert model_dump["description"] == description
    assert model_dump["data"] == data.model_dump()
    assert model_dump["type"] == "model"
    assert model_dump["tags"] == ["tag1", "tag2"]
    assert model_dump["requirements"] == ["requirement1", "requirement2"]
    assert model_dump["data"]["apiKey"] == "api_key"
    # When
    llm_config = model.get_llm_config()
    # # Then
    assert llm_config == {
        "model": name,
        "base_url": "https://example.com",
        "max_tokens": 100,
        "temperature": 0.1,
        "top_p": 0.2,
        "api_version": "v1",
        "api_type": "openai",
        "api_key": "api_key",
        "default_headers": {"Content-Type": "application/json"},
        "price": [0.1, 0.2],
    }


def test_harmony_model_api_key_and_price() -> None:
    """Test HarmonyModel api key from env var and price."""
    current_api_key = os.environ.pop("OPENAI_API_KEY", None)
    os.environ["OPENAI_API_KEY"] = "api_key"
    # Given
    api_type: HarmonyModelAPIType = "openai"
    data = HarmonyModelData(  # type: ignore
        base_url="https://example.com",
        api_type=api_type,
        price=HarmonyModelPrice(
            prompt_price_per_1k=0.1,
            completion_token_price_per_1k=None,
        ),
    )
    # When
    model = HarmonyModel(
        id="wm-1",
        name="model",
        description="description",
        data=data,
        type="model",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    # Then
    assert model.price is None
    assert model.api_key == "api_key"
    if current_api_key is not None:
        os.environ["OPENAI_API_KEY"] = current_api_key
    else:
        os.environ.pop("OPENAI_API_KEY", None)

    # Given
    data = HarmonyModelData(  # type: ignore
        base_url="https://example.com",
        api_type=api_type,
    )
    # When
    model = HarmonyModel(
        id="wm-1",
        name="model",
        description="description",
        data=data,
        type="model",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    # Then
    assert model.price is None
    assert model.api_key == os.environ.get("OPENAI_API_KEY", "")


def test_harmony_api_key() -> None:
    """Test HarmonyModel api key from env var."""
    current_api_key = os.environ.pop("GOOGLE_GEMINI_API_KEY", None)
    os.environ["GOOGLE_GEMINI_API_KEY"] = "gemini_api_key"
    # Given
    api_type: HarmonyModelAPIType = "google"
    data = HarmonyModelData(  # type: ignore
        base_url="https://example.com",
        api_type=api_type,
    )
    # When
    model = HarmonyModel(
        id="wm-1",
        name="model",
        description="description",
        data=data,
        type="model",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    # Then
    assert model.api_key == "gemini_api_key"
    if current_api_key is not None:
        os.environ["GOOGLE_GEMINI_API_KEY"] = current_api_key
    else:
        os.environ.pop("GOOGLE_GEMINI_API_KEY", None)

    current_api_key = os.environ.pop("GROQ_API_KEY", None)
    os.environ["GROQ_API_KEY"] = "groq_api_key"
    # Given
    api_type = "groq"
    data = HarmonyModelData(  # type: ignore
        api_type=api_type,
    )
    # When
    model = HarmonyModel(
        id="wm-1",
        name="model",
        description="description",
        data=data,
        type="model",
        tags=["tag1", "tag2"],
        requirements=["requirement1", "requirement2"],
        created_at="2021-01-01T00:00:00.000Z",
        updated_at="2021-01-01T00:00:00.000Z",
    )
    # Then
    assert model.api_key == "groq_api_key"
    if current_api_key is not None:
        os.environ["GROQ_API_KEY"] = current_api_key
    else:
        os.environ.pop("GROQ_API_KEY", None)


def test_harmony_invalid_model() -> None:
    """Test invalid HarmonyModel."""
    with pytest.raises(ValueError):
        HarmonyModel(  # type: ignore
            id="wm-1",
            name="model",
            description="description",
            type="model",
            tags=["tag1", "tag2"],
            requirements=["requirement1", "requirement2"],
        )
