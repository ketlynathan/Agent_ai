import asyncio
from dataclasses import dataclass, field
from typing import Any
import pytest

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel


# 1. DEPENDÊNCIAS
# Aqui ficariam suas chaves de API (ex: LinkedIn, Indeed, Greenhouse) ou clientes HTTP
@dataclass
class JobSearchDeps:
    api_key: str = "fake-key"
    user_location: str = "Remoto"


# 2. DEFINIÇÃO DO AGENTE
job_agent = Agent(
    'test',
    deps_type=JobSearchDeps,
    system_prompt=(
        "Você é um recrutador especialista. Seu objetivo é ajudar o usuário "
        "a encontrar as melhores vagas de emprego de acordo com as preferências informadas."
    ),
)


# 3. FERRAMENTA DE BUSCA (TOOL)
@job_agent.tool
def search_jobs(
    ctx: RunContext[JobSearchDeps],
    role: str,
    level: str = "Pleno",
    remote_only: bool = True,
) -> list[dict[str, Any]]:
    """Busca vagas de emprego com base no cargo, nível e modalidade.

    Args:
        role: Nome do cargo (ex: 'Python Developer', 'Data Scientist')
        level: Nível de senioridade ('Júnior', 'Pleno', 'Sênior')
        remote_only: Se deve filtrar apenas por vagas remotas
    """
    # Exemplo mockado do retorno de uma API de vagas
    location_str = "Remoto" if remote_only else ctx.deps.user_location

    return [
        {
            "id": "job-101",
            "title": f"{role} {level}",
            "company": "TechCorp",
            "location": location_str,
            "salary": "R$ 8.000 - R$ 12.000",
            "tech_stack": ["Python", "FastAPI", "Docker"],
        },
        {
            "id": "job-102",
            "title": f"Lead {role}",
            "company": "StartupX",
            "location": location_str,
            "salary": "R$ 3.000 - R$ 18.000",
            "tech_stack": ["Python", "AWS", "Pydantic"],
        },
    ]


# 4. TESTE UNITÁRIO
@pytest.mark.asyncio
async def test_job_agent_search():
    deps = JobSearchDeps(user_location="São Paulo")

    # Força o TestModel a executar a ferramenta de busca de vagas
    test_model = TestModel(call_tools=['search_jobs'])

    with job_agent.override(model=test_model):
        result = await job_agent.run(
            "Procure vagas de desenvolvedor Python sênior pra mim.",
            deps=deps,
        )

    assert isinstance(result.output, str)
    # Garante que o modelo processou os dados retornados pela ferramenta
    assert "TechCorp" in result.output or "job-101" in result.output


if __name__ == "__main__":
    # Exemplo de execução local
    async def main():
        deps = JobSearchDeps()
        test_model = TestModel(call_tools=['search_jobs'])

        with job_agent.override(model=test_model):
            res = await job_agent.run(
                "Encontre vagas para Python Developer Pleno remotas.",
                deps=deps,
            )
            print("--- Resposta do Agente ---")
            print(res.output)

    asyncio.run(main())