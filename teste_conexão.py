from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Carrega as variáveis do .env
load_dotenv()

# Modelo da Groq
model = GroqModel("llama-3.3-70b-versatile")

# Cria o agente
agent = Agent(
    model=model,
    instructions="Você é um assistente especialista em Python. Sempre responda em português."
)

# Executa uma pergunta
result = agent.run_sync(
    "Explique em poucas palavras o que é o Pydantic AI."
)

print(result.output)