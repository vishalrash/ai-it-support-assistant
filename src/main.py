import logging
from pathlib import Path
from uuid import uuid4
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command
from agent_graph import agent_graph
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/assistant.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger(__name__)
def handle_agent_response(result, config):
    while result.get("__interrupt__"):
        interrupt_data = result["__interrupt__"][0].value
        print("\n" + "=" * 50)
        print("           TICKET APPROVAL REQUIRED")
        print("=" * 50)
        print("\nIssue:", interrupt_data["issue_description"])
        print("\n" + interrupt_data["question"])
        while True:
            approval = input("Enter YES or NO: ").strip().lower()
            if approval in ["yes", "y", "no", "n"]:
                logger.info(
                    "Ticket approval response received: %s",
                    approval
                )
                break
            print("Invalid response. Please enter YES or NO.")
        result = agent_graph.invoke(
            Command(resume=approval),
            config=config
        )
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and message.content:
            print("\nAssistant:")
            print(message.content)
            break
def main():
    print("=" * 55)
    print("       AI-POWERED IT SUPPORT ASSISTANT")
    print("=" * 55)
    print("\nModel: Qwen3 8B")
    print("LLM Provider: Ollama")
    print("Vector Database: ChromaDB")
    print("\nType 'exit' or 'quit' to close the assistant.")
    print("-" * 55)
    logger.info("IT Support Assistant started.")
    thread_id = str(uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                print("Please enter a message.")
                continue
            if user_input.lower() in ["exit", "quit"]:
                logger.info("IT Support Assistant stopped.")
                print("\nThank you for using IT Support Assistant!")
                break
            logger.info("Received a user message.")
            result = agent_graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config
            )
            handle_agent_response(result, config)
        except KeyboardInterrupt:
            logger.info("Application stopped by keyboard interrupt.")
            print("\n\nAssistant stopped by user.")
            break
        except EOFError:
            logger.info("Application stopped because input was closed.")
            print("\n\nInput closed. Goodbye!")
            break
        except Exception:
            logger.exception("An application error occurred.")
            print(
                "\nAn unexpected error occurred. "
                "Please check logs/assistant.log."
            )
if __name__ == "__main__":
    main()
