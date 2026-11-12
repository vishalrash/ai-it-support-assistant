# AI-Powered IT Support Assistant

An AI-powered IT support assistant built using LangChain, LangGraph, Retrieval-Augmented Generation (RAG), Qwen3 8B, Ollama, and ChromaDB.

The assistant helps users troubleshoot common IT issues, retrieve support ticket information, and create new support tickets with explicit user confirmation.

## Features

- **Knowledge Base Search:** Searches internal IT documentation to answer technical support questions.
- **RAG Pipeline:** Loads documents, splits them into chunks, generates embeddings, and retrieves relevant information.
- **Source Attribution:** Displays the source document used to generate an answer.
- **Grounded Responses:** Restricts answers to the available knowledge base and provides a fallback when information is unavailable.
- **Ticket Status Tracking:** Retrieves existing ticket information from JSON storage.
- **Ticket Creation:** Creates support tickets with unique IDs and stores them in JSON.
- **Human Approval:** Requires explicit YES/NO confirmation before creating a support ticket.
- **Agentic Workflow:** Uses LangGraph to coordinate tool selection, execution, and approval.
- **Conversation Handling:** Supports follow-up questions.
- **Logging and Error Handling:** Records application activity and errors.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| LLM | Qwen3 8B |
| Local LLM Runtime | Ollama |
| AI Framework | LangChain |
| Agent Workflow | LangGraph |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| Document Processing | PyPDF |
| Ticket Storage | JSON |
| Testing | Pytest |

## Architecture

```text
                 USER
                   |
                   v
          IT SUPPORT ASSISTANT
                   |
                   v
             LANGGRAPH AGENT
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Knowledge  Ticket   Ticket
        Search    Status   Creation
          |        |        |
          v        v        v
        RAG      JSON     Approval
       Pipeline  Lookup   Required
          |                 |
          v                 v
       ChromaDB         YES / NO
          |                 |
          v                 v
      IT Documents      Create Ticket
          |
          v
       Qwen3 8B
          |
          v
       RESPONSE
```

## Knowledge Base

The project includes seven sample IT support documents:

1. VPN Setup
2. Password Reset
3. Laptop Configuration
4. Email Troubleshooting
5. Software Installation
6. Wi-Fi Troubleshooting
7. Printer Troubleshooting

These documents contain sample support procedures and should be replaced or adapted to match actual organizational policies before production use.

## Project Structure

```text
ai-it-support-assistant/
│
├── data/
│   └── tickets.json
│
├── knowledge_base/
│   ├── vpn_setup.md
│   ├── password_reset.md
│   ├── laptop_configuration.md
│   ├── email_troubleshooting.md
│   ├── software_installation.md
│   ├── wifi_troubleshooting.md
│   └── printer_troubleshooting.md
│
├── src/
│   ├── agent.py
│   ├── agent_graph.py
│   ├── agent_state.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── langchain_tools.py
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── text_splitter.py
│   ├── ticket_approval.py
│   ├── tools.py
│   ├── tool_node.py
│   ├── vector_store.py
│   └── ingest.py
│
├── tests/
│   ├── manual/
│   └── test_cases.md
│
├── logs/
├── vector_store/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-it-support-assistant
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from:

https://ollama.com/

Pull the Qwen3 8B model:

```powershell
ollama pull qwen3:8b
```

Verify:

```powershell
ollama list
```

Make sure the Ollama service is running before starting the application.

### 5. Build the knowledge base

From the project root, run:

```powershell
python src/ingest.py
```

This loads the documents, splits them into chunks, generates embeddings, and stores them in ChromaDB.

### 6. Run the assistant

```powershell
python src/main.py
```

## Example Queries

**Knowledge Base Search**

```text
You: How do I reset my password?
```

The assistant provides the documented password reset procedure and its source filename.

**Ticket Status**

```text
You: Check ticket TKT1002.
```

The assistant retrieves the ticket details from JSON storage.

**Create Support Ticket**

```text
You: Create a support ticket for my laptop overheating.
```

The assistant requests approval before creating the ticket.

**Unknown Information**

```text
You: What is our company's internal VPN server address?
```

The assistant explains that the address is not documented and should be obtained from the IT department.

## Ticket Approval Workflow

Ticket creation follows a human-in-the-loop process:

1. The user requests a new support ticket.
2. The agent prepares the ticket request.
3. The workflow pauses and asks for approval.
4. The user enters YES or NO.
5. If approved, the ticket is created and saved in `data/tickets.json`.
6. If rejected, no ticket is created.

## Testing

The project includes documented test scenarios in:

`tests/test_cases.md`

The test cases cover:

- Knowledge-base retrieval
- Password reset
- VPN troubleshooting
- Unknown information handling
- Ticket status lookup
- Ticket creation approval
- Ticket cancellation
- Invalid ticket IDs
- Multi-tool workflows
- Follow-up questions

## Configuration

The project uses a local Ollama model and does not require an OpenAI API key.

The `.env` file is excluded from Git. Local configuration can be maintained separately.

## Future Improvements

- Streamlit-based web interface
- User authentication and role management
- Integration with a real IT ticketing platform
- Persistent conversation history
- Improved evaluation and automated testing
- Deployment to a server

## Disclaimer

This project uses sample IT support documentation and mock ticket data for demonstration purposes. It is not connected to a real organization's IT infrastructure or ticketing system.