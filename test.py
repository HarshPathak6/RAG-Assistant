from ChatModels.OpenRouterLLM import llm, llm2

print("Testing OpenRouter...")

response = llm2.invoke("Say hello in one sentence.")

print(response.content)