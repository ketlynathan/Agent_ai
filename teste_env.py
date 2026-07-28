import asyncio
from dataclasses import dataclass, field
import os
import pytest
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

# 1. Carrega o arquivo .env
load_dotenv()


# 2. Classe de Dependências
@dataclass
class LinkedInDeps:
    client_id: str = field(
        default_factory=lambda: os.getenv("LINKEDIN_CLIENT_ID", "")
    )
    client_secret: str = field(
        default_factory=lambda: os.getenv("LINKEDIN_CLIENT_SECRET", "")
    )
    redirect_uri: str = field(
        default_factory=lambda: os.getenv(
            "LINKEDIN_REDIRECT_URI", "https://www.linkedin.com/jobs/"
        )
    )


# 3. Agente do LinkedIn
linkedin_agent = Agent(
    "test",
    deps_type=LinkedInDeps,
    system_prompt="Agente para validação e integração com o LinkedIn.",
)


# 4. Ferramenta para checar as dependências
@linkedin_agent.tool
def check_env_credentials(ctx: RunContext[LinkedInDeps]) -> dict[str, str]:
    """Retorna o estado do carregamento do .env sem expor o secret completo."""
    return {
        "has_client_id": str(bool(ctx.deps.client_id)),
        "has_client_secret": str(bool(ctx.deps.client_secret)),
        "redirect_uri": ctx.deps.redirect_uri,
    }


# 5. O TESTE DO PYTEST
@pytest.mark.asyncio
async def test_linkedin_env_credentials():
    deps = LinkedInDeps()

    # Força o TestModel a executar a ferramenta de checagem
    test_model = TestModel(call_tools=["check_env_credentials"])

    with linkedin_agent.override(model=test_model):
        result = await linkedin_agent.run(
            "Verifique se as credenciais do .env estão presentes.",
            deps=deps,
        )

    # Asserções do teste
    assert isinstance(result.output, str)
    
    # Validações diretas na instância de dependências carregada
    assert deps.client_id != "", "O LINKEDIN_CLIENT_ID não pode estar vazio no .env"
    assert deps.client_secret != "", "O LINKEDIN_CLIENT_SECRET não pode estar vazio no .env"
    assert deps.redirect_uri == "https://www.linkedin.com/jobs/"


if __name__ == "__main__":
    asyncio.run(test_linkedin_env_credentials())