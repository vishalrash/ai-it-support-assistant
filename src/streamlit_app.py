import re
import streamlit as st
import logging
import json
import streamlit.components.v1 as components
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command

from agent_graph import agent_graph
from tools import get_ticket_details

# --------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/assistant.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "show_clear_confirmation" not in st.session_state:
    st.session_state.show_clear_confirmation = False
# --------------------------------------------------
# LANGGRAPH CONFIGURATION
# --------------------------------------------------

def get_graph_config():

    return {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }


def extract_sources(response):

    sources = []

    # Extract source filenames from the response.
    patterns = [
        r"Source filename:\s*([^\n]+)",
        r"Sources:\s*([^\n]+)"
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            response,
            flags=re.IGNORECASE
        )

        for match in matches:

            filenames = [
                name.strip()
                for name in re.split(r"[,;]", match)
                if name.strip()
            ]

            sources.extend(filenames)

    # Remove duplicate filenames.
    sources = list(dict.fromkeys(sources))

    # Remove source metadata from the displayed answer.
    clean_response = re.sub(
        r"Source filename:\s*[^\n]+|Sources:\s*[^\n]+",
        "",
        response,
        flags=re.IGNORECASE
    )

    clean_response = clean_response.strip()

    return clean_response, sources

# --------------------------------------------------
# EXTRACT ASSISTANT RESPONSE
# --------------------------------------------------

def get_assistant_response(result):

    for message in reversed(result["messages"]):

        if (
            isinstance(message, AIMessage)
            and message.content
            and not message.tool_calls
        ):
            return str(message.content)

    return "The request was processed, but no response was returned."

def render_copy_button(text, key):

    safe_text = json.dumps(text)

    components.html(
        f"""
        <button id="copy-{key}" style="
            background: transparent;
            border: 1px solid #888888;
            border-radius: 8px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
        ">
            📋 Copy Response
        </button>

        <script>
            const button = document.getElementById("copy-{key}");
            const responseText = {safe_text};

            button.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText(responseText);
                    button.innerText = "✓ Copied!";
                }} catch (error) {{
                    button.innerText = "Copy failed";
                }}
            }});
        </script>
        """,
        height=45
    )

def save_feedback(message_index, feedback_type):

    feedback_file = Path("data/feedback.json")

    feedback_file.parent.mkdir(exist_ok=True)

    # Load existing feedback
    if feedback_file.exists():
        try:
            with open(feedback_file, "r", encoding="utf-8") as file:
                feedback_data = json.load(file)

            if not isinstance(feedback_data, list):
                feedback_data = []

        except (json.JSONDecodeError, OSError):
            feedback_data = []
    else:
        feedback_data = []

    # Prepare new feedback record
    feedback_record = {
        "thread_id": st.session_state.thread_id,
        "message_index": message_index,
        "feedback": feedback_type,
        "timestamp": datetime.now().isoformat()
    }

    feedback_data.append(feedback_record)

    # Save updated feedback
    with open(feedback_file, "w", encoding="utf-8") as file:
        json.dump(feedback_data, file, indent=4)

    logger.info("Feedback recorded: %s", feedback_type)


# --------------------------------------------------
# HANDLE LANGGRAPH RESULT
# --------------------------------------------------

def process_agent_result(result):

    # Check whether the agent requires ticket approval.
    if result.get("__interrupt__"):

        interrupt_data = result["__interrupt__"][0].value

        st.session_state.pending_approval = interrupt_data

        logger.info("Agent is waiting for ticket approval.")

    else:

        response = get_assistant_response(result)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.session_state.pending_approval = None


# --------------------------------------------------
# HANDLE TICKET APPROVAL
# --------------------------------------------------

def handle_ticket_approval(approval):

    try:

        result = agent_graph.invoke(
            Command(resume=approval),
            config=get_graph_config()
        )

        process_agent_result(result)

        logger.info(
            "Ticket approval processed: %s",
            approval
        )

    except Exception:

        logger.exception("Ticket approval failed.")

        st.session_state.pending_approval = None

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "An error occurred while processing your "
                "ticket approval. Please check the application logs."
            )
        })


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("IT Support")
    st.write("Powered by Qwen3 8B and LangGraph")

    st.divider()

    st.subheader("System Information")

    st.write("**LLM:** Qwen3 8B")
    st.write("**Provider:** Ollama")
    st.write("**Vector Database:** ChromaDB")
    st.write("**Agent Framework:** LangGraph")

    st.divider()

    st.subheader("Appearance")

    st.selectbox(
        "Choose theme",
        options=["Light", "Dark"],
        key="theme"
    )

    st.divider()

    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid4())
        st.session_state.pending_approval = None
        st.rerun()

    st.divider()

    # Download conversation
    transcript = ""

    for message in st.session_state.messages:

        role = (
            "USER"
            if message["role"] == "user"
            else "AI ASSISTANT"
        )

        transcript += (
            f"{role}:\n"
            f"{message['content']}\n\n"
            + "-" * 50 + "\n\n"
        )

    st.download_button(
        label="📥 Download Conversation",
        data=transcript,
        file_name="it_support_conversation.txt",
        mime="text/plain",
        use_container_width=True,
        disabled=len(st.session_state.messages) == 0
    )
    st.divider()

    # Clear chat history
    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True
    ):
        st.session_state.show_clear_confirmation = True

    # Confirmation interface
    if st.session_state.show_clear_confirmation:

        st.warning(
            "Are you sure you want to clear this conversation?"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "Yes, Clear",
                type="primary",
                use_container_width=True
            ):

                st.session_state.messages = []
                st.session_state.thread_id = str(uuid4())
                st.session_state.pending_approval = None
                st.session_state.show_clear_confirmation = False

                logger.info("Chat history cleared.")

                st.toast("Conversation cleared successfully!")
                st.rerun()

        with col2:
            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.show_clear_confirmation = False
                st.rerun()
# --------------------------------------------------
# DYNAMIC THEME STYLING
# --------------------------------------------------

if st.session_state.theme == "Dark":

    background = "#0E1117"
    sidebar_background = "#161B22"
    text_color = "#F0F2F6"
    secondary_text = "#AAB2BF"
    message_background = "#202938"
    border_color = "#303846"

else:

    background = "#FFFFFF"
    sidebar_background = "#F7F8FA"
    text_color = "#202124"
    secondary_text = "#6B7280"
    message_background = "#F1F3F6"
    border_color = "#DADDE3"




st.markdown(
    f"""
    <style>

    /* Main application */
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {{
        background-color: {background} !important;
        color: {text_color} !important;
    }}

    /* Header and bottom area */
    [data-testid="stHeader"],
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {{
        background-color: {background} !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_background} !important;
    }}

    /* General text */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {{
        color: {text_color} !important;
    }}

    /* Chat messages */
    [data-testid="stChatMessage"] {{
        background-color: {message_background} !important;
        border: 1px solid {border_color} !important;
        border-radius: 12px;
        padding: 12px;
    }}

    /* Theme dropdown */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
        background-color: {message_background} !important;
        border-color: {border_color} !important;
    }}

    [data-testid="stSelectbox"] input,
    [data-testid="stSelectbox"] [data-baseweb="select"] div {{
        color: {text_color} !important;
    }}

    [data-testid="stSelectbox"] svg {{
        fill: {text_color} !important;
    }}

    /* Dropdown options */
    [data-baseweb="popover"],
    [data-baseweb="menu"] {{
        background-color: {message_background} !important;
    }}

    [role="option"] {{
        background-color: {message_background} !important;
        color: {text_color} !important;
    }}

    /* Buttons */
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {{
        background-color: {message_background} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}

    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-primary"] p {{
        color: {text_color} !important;
    }}

    /* Chat input outer container */
    [data-testid="stChatInput"] > div {{
        background-color: {message_background} !important;
        border: 1px solid {border_color} !important;
    }}

    /* Chat input text area */
    [data-testid="stChatInput"] textarea,
    [data-baseweb="textarea"] textarea {{
        background-color: {message_background} !important;
        color: {text_color} !important;
        -webkit-text-fill-color: {text_color} !important;
    }}

    /* Placeholder */
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {secondary_text} !important;
        -webkit-text-fill-color: {secondary_text} !important;
    }}

    /* Dividers */
    hr {{
        border-color: {border_color} !important;
    }}

    /* Captions */
    [data-testid="stCaptionContainer"] {{
        color: {secondary_text} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# MAIN CHAT INTERFACE
# --------------------------------------------------

st.title("🤖 AI-Powered IT Support Assistant")

st.caption(
    "Your intelligent assistant for IT troubleshooting and support"
)

st.divider()

# --------------------------------------------------
# TICKET MANAGEMENT - TICKET STATUS LOOKUP
# --------------------------------------------------

st.subheader("🎫 Ticket Management")

st.write(
    "Track your support requests using your ticket ID."
)

with st.container(border=True):

    st.markdown("### Check Ticket Status")

    with st.form("ticket_lookup_form"):

        ticket_id_input = st.text_input(
            "Enter Ticket ID",
            placeholder="Example: TKT1002"
        )

        search_ticket = st.form_submit_button(
            "🔍 Check Status",
            use_container_width=True
        )

    if search_ticket:

        if not ticket_id_input.strip():

            st.warning("Please enter a ticket ID.")

        else:

            try:

                with st.spinner("Searching for ticket..."):

                    ticket = get_ticket_details(ticket_id_input)

                if ticket is None:

                    st.error(
                        f"No ticket found with ID: "
                        f"{ticket_id_input.strip().upper()}"
                    )

                else:

                    st.success("Ticket found successfully!")

                    st.divider()

                    # Ticket header
                    col1, col2 = st.columns([2, 1])

                    with col1:

                        st.markdown(
                            f"### {ticket['ticket_id']}"
                        )

                    with col2:

                        status = ticket["status"].strip().lower()

                        if status in ["resolved", "closed", "completed"]:

                            st.success(ticket["status"])

                        elif status in ["open", "pending"]:

                            st.warning(ticket["status"])

                        else:

                            st.info(ticket["status"])

                    # Issue description
                    st.markdown("**Issue Description**")

                    st.write(
                        ticket["issue_description"]
                    )

                    st.divider()

                    # Ticket information
                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.markdown("**Employee**")

                        st.write(
                            ticket.get(
                                "employee_name",
                                "Not provided"
                            )
                        )

                    with col2:

                        st.markdown("**Priority**")

                        priority = ticket.get(
                            "priority",
                            "Not specified"
                        )

                        if priority.lower() == "high":

                            st.error(priority)

                        elif priority.lower() == "medium":

                            st.warning(priority)

                        else:

                            st.info(priority)

                    with col3:

                        st.markdown("**Created At**")

                        st.write(
                            ticket.get(
                                "created_at",
                                "Not available"
                            )
                        )

            except ValueError as error:

                st.warning(str(error))

            except Exception:

                logger.exception(
                    "Ticket status lookup failed."
                )

                st.error(
                    "Unable to retrieve ticket details. "
                    "Please check the application logs."
                )

st.divider()


# --------------------------------------------------
# CREATE SUPPORT TICKET
# --------------------------------------------------

st.subheader("📝 Create Support Ticket")

st.write(
    "Describe your IT problem to raise a new support request."
)

with st.container(border=True):

    with st.form("create_ticket_form"):

        issue_description = st.text_area(
            "Describe your IT issue",
            placeholder=(
                "Example: My laptop is overheating "
                "and shutting down unexpectedly."
            ),
            height=120
        )

        submit_ticket = st.form_submit_button(
            "📩 Submit Support Request",
            use_container_width=True
        )

    if submit_ticket:

        if not issue_description.strip():

            st.warning("Please describe your IT issue.")

        else:

            request_message = (
                "I want to create a support ticket for this issue: "
                + issue_description.strip()
            )

            st.session_state.messages.append({
                "role": "user",
                "content": request_message
            })

            try:

                with st.spinner(
                    "Preparing your support ticket..."
                ):

                    result = agent_graph.invoke(
                        {
                            "messages": [
                                HumanMessage(content=request_message)
                            ]
                        },
                        config=get_graph_config()
                    )

                    process_agent_result(result)

            except Exception:

                logger.exception(
                    "Support ticket request failed."
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": (
                        "Unable to process your ticket request. "
                        "Please check the application logs."
                    )
                })

            st.rerun()

st.divider()

# --------------------------------------------------
# WELCOME SCREEN AND SUGGESTED QUESTIONS
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        "### 👋 Welcome to IT Support!"
    )

    st.write(
        "Select a common issue below or describe "
        "your problem in the chat box."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔑 Password reset",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "How do I reset my company password?"
            )
            st.rerun()

        if st.button(
            "🎫 Check ticket status",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "Check the status of ticket TKT1002."
            )
            st.rerun()

    with col2:

        if st.button(
            "🔒 VPN troubleshooting",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "I'm unable to connect to VPN. "
                "How can I troubleshoot it?"
            )
            st.rerun()

        if st.button(
            "💻 Laptop problems",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "My laptop is running slowly. "
                "How can I troubleshoot it?"
            )
            st.rerun()

# Display existing conversation history.



for index, message in enumerate(st.session_state.messages):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            render_copy_button(
                message["content"],
                key=f"response-{index}"
            )

            col1, col2, col3 = st.columns([1, 1, 8])

            with col1:
                if st.button(
                    "👍 Helpful",
                    key=f"helpful-{index}"
                ):
                    save_feedback(index, "helpful")
                    st.toast("Thank you for your feedback!")

            with col2:
                if st.button(
                    "👎 Not Helpful",
                    key=f"not-helpful-{index}"
                ):
                    save_feedback(index, "not_helpful")
                    st.toast("Thank you for your feedback!")



# --------------------------------------------------
# TICKET APPROVAL INTERFACE
# --------------------------------------------------

if st.session_state.pending_approval:

    approval_data = st.session_state.pending_approval

    st.warning("Ticket approval required")

    st.write("**Issue:**", approval_data["issue_description"])

    st.write(approval_data["question"])

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "YES - Create Ticket",
            type="primary",
            use_container_width=True
        ):

            with st.spinner("Creating support ticket..."):

                handle_ticket_approval("yes")

            st.rerun()

    with col2:

        if st.button(
            "NO - Cancel",
            use_container_width=True
        ):

            handle_ticket_approval("no")

            st.rerun()


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Describe your IT issue...",
    disabled=st.session_state.pending_approval is not None
)
# Use a suggested question if one was selected.
if st.session_state.get("suggested_prompt"):

    user_input = st.session_state.suggested_prompt

    del st.session_state.suggested_prompt

# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    logger.info("Received a user message.")

    try:

        with st.spinner("AI Assistant is thinking..."):

            result = agent_graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=get_graph_config()
            )

            process_agent_result(result)

    except Exception:

        logger.exception("Agent execution failed.")

        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Sorry, an error occurred while processing your "
                "request. Please check the application logs."
            )
        })

    st.rerun()
