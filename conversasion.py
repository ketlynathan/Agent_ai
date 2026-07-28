from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

load_dotenv()

model = GroqModel("llama-3.3-70b-versatile")

agent = Agent(
    model=model,
    instructions="""
Você é um especialista em Python.
Responda sempre em português.
"""
)

print("Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ")

    if pergunta.lower() == "sair":
        break

    resposta = agent.run_sync(pergunta)

    print("\nIA:")
    print(resposta.output)
    print("-" * 50)