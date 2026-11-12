from langchain_ollama import ChatOllama
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    num_predict=300
)
print("Connecting to local Qwen3 model...")
response = llm.invoke(
    "Explain RAG in two simple sentences."
)
print("\nQwen3 Response:")
print(response.content)
