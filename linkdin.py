import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

# Carrega as variáveis do arquivo .env para o ambiente Python
load_dotenv()


# 1. DEPENDÊNCIAS LENDO DIRETO DO AMBIENTE
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
    access_token: str | None = field(
        default_factory=lambda: os.getenv("LINKEDIN_ACCESS_TOKEN", None)
    )


# 2. AGENTE PYDANTIC AI
linkedin_agent = Agent(
    'test',
    deps_type=LinkedInDeps,
    system_prompt="Agente de integração com o LinkedIn.",
)


# 3. TOOL USANDO AS DEPENDÊNCIAS CARREGADAS DO .ENV
@linkedin_agent.tool
def check_linkedin_credentials(ctx: RunContext[LinkedInDeps]) -> str:
    """Verifica se as credenciais do LinkedIn foram carregadas corretamente do .env."""
    if not ctx.deps.client_id or not ctx.deps.client_secret:
        return "Erro: Credenciais do LinkedIn não encontradas no .env"
    
    return f"Credenciais carregadas com sucesso! Redirect URI: {ctx.deps.redirect_uri}"