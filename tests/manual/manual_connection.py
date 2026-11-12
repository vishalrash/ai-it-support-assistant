from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
print("Connecting to OpenAI...")
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)
response = llm.invoke(
    "What is RAG? Explain in two simple sentences."
)
print("\nOpenAI Connection Successful!")
print("AI Response:")
print(response.content)
