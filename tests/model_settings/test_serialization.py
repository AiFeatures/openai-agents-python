import json
from dataclasses import fields

import pytest
from openai.types.shared import Reasoning
from pydantic import TypeAdapter
from pydantic_core import to_json

from agents.model_settings import MCPToolChoice, ModelSettings


def verify_serialization(model_settings: ModelSettings) -> None:
    """Verify that ModelSettings can be serialized to a JSON string."""
    json_dict = model_settings.to_json_dict()
    json_string = json.dumps(json_dict)
    assert json_string is not None


def test_basic_serialization() -> None:
    """Tests whether ModelSettings can be serialized to a JSON string."""

    # First, lets create a ModelSettings instance
    model_settings = ModelSettings(
        temperature=0.5,
        top_p=0.9,
        max_tokens=100,
    )

    # Now, lets serialize the ModelSettings instance to a JSON string
    verify_serialization(model_settings)


def test_model_settings_direct_constructor_preserves_openai_reasoning_extensions() -> None:
    settings = ModelSettings(
        reasoning={"context": "all_turns", "future_reasoning_option": "enabled"}
    )

    assert isinstance(settings.reasoning, Reasoning)
    assert settings.reasoning.context == "all_turns"
    assert settings.reasoning.model_extra == {"future_reasoning_option": "enabled"}


def test_model_settings_dictionary_override_preserves_omitted_values() -> None:
    settings = ModelSettings(
        temperature=0.5,
        reasoning=Reasoning.model_validate(
            {"context": "all_turns", "future_reasoning_option": "enabled"}
        ),
        retry=ModelRetrySettings(max_retries=2),
    )

    resolved = settings.resolve({"temperature": 0.0})

    assert resolved.temperature == 0.0
    assert resolved.reasoning is settings.reasoning
    assert resolved.retry is settings.retry


def test_model_settings_dictionary_override_merges_retry_settings() -> None:
    settings = ModelSettings(
        retry=ModelRetrySettings(
            max_retries=2,
            backoff=ModelRetryBackoffSettings(initial_delay=0.1, jitter=True),
        )
    )

    resolved = settings.resolve({"retry": {"max_retries": 0, "backoff": {"jitter": False}}})

    assert resolved.retry is not None
    assert resolved.retry.max_retries == 0
    assert isinstance(resolved.retry.backoff, ModelRetryBackoffSettings)
    assert resolved.retry.backoff.initial_delay == 0.1
    assert resolved.retry.backoff.jitter is False


def test_model_settings_dictionary_override_rejects_unknown_fields() -> None:
    with pytest.raises(TypeError, match="Unknown model settings: temperatur"):
        ModelSettings().resolve({"temperatur": 0.5})


def test_mcp_tool_choice_serialization() -> None:
    """Tests whether ModelSettings with MCPToolChoice can be serialized to a JSON string."""
    # First, lets create a ModelSettings instance
    model_settings = ModelSettings(
        temperature=0.5,
        tool_choice=MCPToolChoice(server_label="mcp", name="mcp_tool"),
    )
    # Now, lets serialize the ModelSettings instance to a JSON string
    verify_serialization(model_settings)


def test_all_fields_serialization() -> None:
    """Tests whether ModelSettings can be serialized to a JSON string."""

    # First, lets create a ModelSettings instance
    model_settings = ModelSettings(
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        tool_choice="auto",
        parallel_tool_calls=True,
        truncation="auto",
        max_tokens=100,
        reasoning=Reasoning(),
        metadata={"foo": "bar"},
        store=False,
        prompt_cache_retention="24h",
        include_usage=False,
        response_include=["reasoning.encrypted_content"],
        top_logprobs=1,
        verbosity="low",
        extra_query={"foo": "bar"},
        extra_body={"foo": "bar"},
        extra_headers={"foo": "bar"},
        extra_args={"custom_param": "value", "another_param": 42},
        retry=ModelRetrySettings(
            max_retries=2,
            backoff=ModelRetryBackoffSettings(
                initial_delay=0.1,
                max_delay=1.0,
                multiplier=2.0,
                jitter=False,
            ),
        ),
        context_management=[{"type": "compaction", "compact_threshold": 200000}],
        prompt_cache_options={"mode": "explicit", "ttl": "30m"},
    )

    # Verify that every single field is set to a non-None value
    for field in fields(model_settings):
        assert getattr(model_settings, field.name) is not None, (
            f"You must set the {field.name} field"
        )

    # Now, lets serialize the ModelSettings instance to a JSON string
    verify_serialization(model_settings)


def test_gpt_5_6_reasoning_and_prompt_cache_serialization() -> None:
    model_settings = ModelSettings(
        reasoning=Reasoning(mode="pro", effort="max", context="all_turns"),
        prompt_cache_options={"mode": "explicit", "ttl": "30m"},
    )

    serialized_reasoning = model_settings.to_json_dict()["reasoning"]
    assert serialized_reasoning["context"] == "all_turns"
    assert serialized_reasoning["effort"] == "max"
    assert serialized_reasoning["mode"] == "pro"
    assert model_settings.to_traceable_dict()["prompt_cache_options"] == {
        "mode": "explicit",
        "ttl": "30m",
    }


def test_prompt_cache_options_is_appended_to_public_field_order() -> None:
    field_names = [field.name for field in fields(ModelSettings)]

    assert field_names[-2:] == ["context_management", "prompt_cache_options"]


def test_extra_args_serialization() -> None:
    """Test that extra_args are properly serialized."""
    model_settings = ModelSettings(
        temperature=0.5,
        extra_args={"custom_param": "value", "another_param": 42, "nested": {"key": "value"}},
    )

    json_dict = model_settings.to_json_dict()
    assert json_dict["extra_args"] == {
        "custom_param": "value",
        "another_param": 42,
        "nested": {"key": "value"},
    }

    # Verify serialization works
    verify_serialization(model_settings)


def test_traceable_serialization_omits_request_extras() -> None:
    model_settings = ModelSettings(
        temperature=0.5,
        extra_headers={"Authorization": "Bearer provider-token"},
        extra_query={"api-key": "query-token"},
        extra_body={"secret": "body-token"},
        extra_args={"api_key": "arg-token"},
    )

    json_dict = model_settings.to_json_dict()
    assert json_dict["extra_headers"] == {"Authorization": "Bearer provider-token"}
    assert json_dict["extra_query"] == {"api-key": "query-token"}
    assert json_dict["extra_body"] == {"secret": "body-token"}
    assert json_dict["extra_args"] == {"api_key": "arg-token"}

    traceable = model_settings.to_traceable_dict()
    assert traceable["temperature"] == 0.5
    assert "extra_headers" not in traceable
    assert "extra_query" not in traceable
    assert "extra_body" not in traceable
    assert "extra_args" not in traceable


def test_extra_args_resolve() -> None:
    """Test that extra_args are properly merged in the resolve method."""
    base_settings = ModelSettings(
        temperature=0.5, extra_args={"param1": "base_value", "param2": "base_only"}
    )

    override_settings = ModelSettings(
        top_p=0.9, extra_args={"param1": "override_value", "param3": "override_only"}
    )

    resolved = base_settings.resolve(override_settings)

    # Check that regular fields are properly resolved
    assert resolved.temperature == 0.5  # from base
    assert resolved.top_p == 0.9  # from override

    # Check that extra_args are properly merged
    expected_extra_args = {
        "param1": "override_value",  # override wins
        "param2": "base_only",  # from base
        "param3": "override_only",  # from override
    }
    assert resolved.extra_args == expected_extra_args


def test_extra_args_resolve_with_none() -> None:
    """Test that resolve works properly when one side has None extra_args."""
    # Base with extra_args, override with None
    base_settings = ModelSettings(extra_args={"param1": "value1"})
    override_settings = ModelSettings(temperature=0.8)

    resolved = base_settings.resolve(override_settings)
    assert resolved.extra_args == {"param1": "value1"}
    assert resolved.temperature == 0.8

    # Base with None, override with extra_args
    base_settings = ModelSettings(temperature=0.5)
    override_settings = ModelSettings(extra_args={"param2": "value2"})

    resolved = base_settings.resolve(override_settings)
    assert resolved.extra_args == {"param2": "value2"}
    assert resolved.temperature == 0.5


def test_extra_args_resolve_both_none() -> None:
    """Test that resolve works when both sides have None extra_args."""
    base_settings = ModelSettings(temperature=0.5)
    override_settings = ModelSettings(top_p=0.9)

    resolved = base_settings.resolve(override_settings)
    assert resolved.extra_args is None
    assert resolved.temperature == 0.5
    assert resolved.top_p == 0.9


def test_pydantic_serialization() -> None:
    """Tests whether ModelSettings can be serialized with Pydantic."""

    # First, lets create a ModelSettings instance
    model_settings = ModelSettings(
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        tool_choice="auto",
        parallel_tool_calls=True,
        truncation="auto",
        max_tokens=100,
        reasoning=Reasoning(),
        metadata={"foo": "bar"},
        store=False,
        include_usage=False,
        top_logprobs=1,
        extra_query={"foo": "bar"},
        extra_body={"foo": "bar"},
        extra_headers={"foo": "bar"},
        extra_args={"custom_param": "value", "another_param": 42},
    )

    json = to_json(model_settings)
    deserialized = TypeAdapter(ModelSettings).validate_json(json)

    assert model_settings == deserialized
