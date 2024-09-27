"""Test harmony.exporting.models*."""

from harmony.exporting.models import export_models
from harmony.models import WaldieModel, WaldieModelData


def test_export_models() -> None:
    """Test export_models()."""
    # Given
    model1 = WaldieModel(
        id="wm-1",
        name="llama3.1",
        type="model",
        description="A model for llamas :P.",
        tags=["llama", "llama3.1"],
        requirements=[],
        data=WaldieModelData(
            base_url="https://example.com/v1",
            api_key="1234567890",
            api_type="openai",
            api_version=None,
            temperature=0.5,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0001,
                "completion_token_price_per_1k": 0.0002,
            },
        ),
    )
    model_names = {"wm-1": "llama3_1"}
    # When
    result, _ = export_models([model1], model_names, True)
    # Then
    expected = """
# ## Models

llama3_1 = {
    "model": "llama3.1",
    "base_url": "https://example.com/v1",
    "temperature": 0.5,
    "api_type": "openai",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}
"""

    assert result == expected

    # Given
    model2 = WaldieModel(
        id="wm-2",
        name="groq_model",
        type="model",
        description="A groq model.",
        tags=["groq"],
        requirements=[],
        data=WaldieModelData(
            base_url="https://example.com/v2",
            api_key="1234567890",
            api_type="groq",
            api_version=None,
            temperature=0.5,
            top_p=None,
            max_tokens=None,
            default_headers={},
            price={  # type: ignore
                "prompt_price_per_1k": 0.0001,
                "completion_token_price_per_1k": 0.0002,
            },
        ),
    )
    model_names = {"wm-1": "llama3_1", "wm-2": "groq_model"}
    # When
    result, model_import = export_models([model1, model2], model_names, True)
    # Then
    expected = """
# ## Models

llama3_1 = {
    "model": "llama3.1",
    "base_url": "https://example.com/v1",
    "temperature": 0.5,
    "api_type": "openai",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}
groq_model = {
    "model": "groq_model",
    "base_url": "https://example.com/v2",
    "temperature": 0.5,
    "api_type": "groq",
    "api_key": "1234567890",
    "price": [
        0.0001,
        0.0002
    ]
}
"""
    assert result == expected
    assert model_import == {"pyautogen[groq]"}
