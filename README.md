# AI-Powered IT Support Assistant

An AI-powered IT support assistant built using **Python, LangChain, LangGraph, Retrieval-Augmented Generation (RAG), Qwen3 8B, Ollama, and ChromaDB**.

The system helps users troubleshoot common IT issues using internal knowledge documents, retrieve support ticket information, and request new support tickets through a human approval workflow.

It uses a locally running Large Language Model (LLM), so it does not require a paid cloud LLM API.

## Features

- **Knowledge Base Search:** Retrieves relevant information from internal IT support documents.
- **RAG Pipeline:** Loads documents, splits text into chunks, generates embeddings, and retrieves relevant content.
- **Grounded Responses:** Generates answers using retrieved knowledge and avoids making up undocumented procedures.
- **Source Attribution:** Identifies the source documents used to answer questions.
- **Ticket Status Tracking:** Retrieves existing ticket details from JSON storage.
- **Ticket Creation:** Generates unique ticket IDs and stores approved tickets.
- **Human-in-the-Loop Approval:** Requires explicit YES/NO confirmation before creating a ticket.
- **Agentic Workflow:** Uses LangGraph to coordinate LLM decisions, tool execution, and approval.
- **Conversation Handling:** Supports follow-up questions.
- **Streamlit Interface:** Provides a web-based interface for interacting with the assistant and managing tickets.
- **Feedback Collection:** Allows users to rate assistant responses.
- **Logging and Error Handling:** Records application activity and errors.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Large Language Model | Qwen3 8B |
| Local LLM Runtime | Ollama |
| AI Framework | LangChain |
| Agent Workflow | LangGraph |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| Document Processing | PyPDF |
| Web Interface | Streamlit |
| Ticket Storage | JSON |
| Testing Framework | Pytest |

## System Architecture

```text
                       USER
                         |
                         v
              STREAMLIT WEB INTERFACE
                         |
                         v
                  LANGGRAPH AGENT
                         |
                  QWEN3 8B (OLLAMA)
                         |
                  TOOL SELECTION
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
    KNOWLEDGE BASE   TICKET STATUS   TICKET REQUEST
       SEARCH          LOOKUP           TOOL
          |              |              |
          v              v              v
      RAG PIPELINE    JSON STORAGE   HUMAN APPROVAL
          |                             |
          v                         +---+---+
      EMBEDDINGS                    |       |
          |                        YES      NO
          v                         |       |
       CHROMADB                     v       v
          |                    CREATE    CANCEL
          v                    TICKET    REQUEST
    IT DOCUMENTS
          |
          v
    GROUNDED RESPONSE
          |
          v
         USER
```

## Retrieval-Augmented Generation (RAG)

The knowledge base contains seven sample IT support documents.

1. VPN Setup
2. Password Reset
3. Laptop Configuration
4. Email Troubleshooting
5. Software Installation
6. Wi-Fi Troubleshooting
7. Printer Troubleshooting

The RAG pipeline follows these steps:

1. Load documents from the knowledge base.
2. Extract document text.
3. Split the text into smaller chunks.
4. Generate embeddings using `all-MiniLM-L6-v2`.
5. Store the embeddings in ChromaDB.
6. Retrieve relevant chunks when a user asks a question.
7. Pass the retrieved context to Qwen3 8B.
8. Generate a response grounded in the retrieved documents.

The current implementation generated 61 chunks from the seven sample documents.

## Agentic Workflow

The project uses LangGraph to coordinate the assistant's workflow.

The agent has access to these tools:

- `knowledge_base_search(query)` – searches internal IT documentation.
- `ticket_status_lookup(ticket_id)` – retrieves ticket status.
- `request_support_ticket(issue_description)` – prepares a ticket request for approval.
- `create_approved_ticket(issue_description)` – creates a ticket after approval.

### Human-in-the-Loop Ticket Approval

Ticket creation follows an explicit approval process:

1. The user describes an IT issue.
2. The agent prepares a ticket request.
3. The workflow pauses and requests user confirmation.
4. The user selects YES or NO.
5. If approved, the ticket is created and stored in `data/tickets.json`.
6. If rejected, the workflow cancels ticket creation.

This prevents the agent from creating support tickets without user authorization.

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
│   ├── ingest.py
│   ├── langchain_tools.py
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── retriever.py
│   ├── streamlit_app.py
│   ├── text_splitter.py
│   ├── ticket_approval.py
│   ├── tool_node.py
│   ├── tools.py
│   └── vector_store.py
│
├── tests/
│   ├── manual/
│   └── test_cases.md
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

**Note:** `.env`, `vector_store/`, and `logs/` are local runtime files or directories and are excluded from Git.

## Installation and Setup

### 1. Clone the repository

```powershell
git clone https://github.com/vishalrash/ai-it-support-assistant.git
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

Download and install Ollama:

https://ollama.com/

Download the Qwen3 8B model:

```powershell
ollama pull qwen3:8b
```

Verify the installation:

```powershell
ollama list
```

Make sure the Ollama service is running before starting the assistant.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3:8b
OLLAMA_BASE_URL=http://localhost:11434
```

The `.env` file is excluded from Git and should remain local.

### 6. Build the knowledge base

From the project root:

```powershell
python src/ingest.py
```

This loads the documents, splits them into chunks, generates embeddings, and stores them in ChromaDB.

### 7. Run the Streamlit application

```powershell
streamlit run src/streamlit_app.py
```

Open the local URL displayed in your terminal to access the web interface.

### Optional: Run the command-line assistant

```powershell
python src/main.py
```

## Example Queries

### Knowledge Base Search

```text
How do I reset my company password?
```

The assistant retrieves the documented password reset procedure and identifies its source.

### Ticket Status Lookup

```text
Check ticket TKT1002.
```

The assistant retrieves the ticket information from JSON storage.

### Ticket Creation

```text
Create a support ticket for my laptop overheating.
```

The assistant requests explicit approval before creating the ticket.

### Unknown Information

```text
What is our company's internal Wi-Fi password?
```

If the information is unavailable in the knowledge base, the assistant responds that it cannot find the information rather than inventing an answer.

## Testing

The project includes documented manual test scenarios in:

`tests/test_cases.md`

The scenarios cover:

- Knowledge-base retrieval
- Password reset guidance
- VPN troubleshooting
- Unknown information handling
- Ticket status lookup
- Ticket creation approval
- Ticket cancellation
- Invalid ticket IDs
- Multi-tool workflows
- Follow-up questions

Manual development scripts are maintained under `tests/manual/`.

## Configuration

- The application uses Qwen3 8B through Ollama.
- The LLM runs locally.
- No OpenAI API key is required.
- ChromaDB stores the document embeddings locally.
- Ticket records are maintained in JSON storage.
- User feedback is stored locally in `data/feedback.json`.

## Future Improvements

- User authentication and role-based access control.
- Integration with real IT ticketing platforms.
- Support for additional document formats.
- Improved retrieval and response evaluation.
- Deployment to a cloud or on-premises server.
- Production-grade database storage.

## Disclaimer

This project uses sample IT support documentation and mock ticket data for demonstration purposes. It is not connected to a real organization's IT infrastructure or ticketing system. The sample procedures should be adapted to actual organizational policies before production use.
