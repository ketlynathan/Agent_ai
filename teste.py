import asyncio
from dataclasses import dataclass
from datetime import date
import pytest
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel


@dataclass
class MockDeps:
    weather_api: object | None = None


weather_agent = Agent(
    'test',
    deps_type=MockDeps,
    system_prompt="Stubbed weather agent for testing",
)


@weather_agent.tool
def run_weather_forecast(
    ctx: RunContext[MockDeps],
    city: str = "São Paulo",
    when: date | None = None,
) -> str:
    d = (when or date.today()).isoformat()
    return f"Previsão fake para {city} em {d}: céu limpo."


@pytest.mark.asyncio
async def test_weather_agent_simple():
    deps = MockDeps()

    # Força o TestModel a simular a chamada da ferramenta
    test_model = TestModel(call_tools=['run_weather_forecast'])

    with weather_agent.override(model=test_model):
        result = await weather_agent.run(
            "Como está o tempo em SP?",
            deps=deps,
        )

    # Voltou para result.output
    assert isinstance(result.output, str)
    assert "Previsão fake" in result.output


if __name__ == "__main__":
    asyncio.run(test_weather_agent_simple())