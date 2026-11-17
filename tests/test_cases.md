


**LLM:** Qwen3 8B  
**LLM Runtime:** Ollama  
**Framework:** LangChain and LangGraph  
**Vector Database:** ChromaDB  
**Embedding Model:** all-MiniLM-L6-v2

---



The AI-Powered IT Support Assistant was tested to verify knowledge retrieval, ticket management, multi-tool execution, conversation memory, and response reliability.

The objective was to ensure that the assistant provides answers grounded in the available IT documents, retrieves ticket information correctly, and obtains explicit user approval before creating support tickets.





**Input:**
`My VPN is not connecting. How can I fix it?`

**Expected Result:**
The assistant should retrieve VPN troubleshooting instructions from the knowledge base and identify the source document.

**Actual Output:**
The assistant returned nine troubleshooting steps, including verifying credentials, checking password expiry, completing MFA, checking internet connectivity, restarting the VPN application, and contacting IT support if the issue continued.

**Source:** `vpn_setup.md`

**Status:** PASS

---



**Input:**
`How do I reset my password?`

**Expected Result:**
The assistant should retrieve the documented password reset procedure.

**Actual Output:**
The assistant provided password reset instructions from the password reset documentation.

**Source:** `password_reset.md`

**Status:** PASS

---



**Input:**
`Check ticket TKT1002.`

**Expected Result:**
The assistant should retrieve the correct ticket details from the JSON database.

**Actual Output:**
- Ticket ID: TKT1002
- Issue: Company email is not syncing
- Status: In Progress
- Priority: Medium
- Created At: 2026-11-10 10:15:00

**Status:** PASS

---



**Input:**
`Create a support ticket for my laptop overheating.`

**Expected Result:**
The application should request approval before creating the ticket. After YES, the ticket should be saved in the JSON database.

**Actual Output:**
The application requested approval and successfully created a ticket after YES was provided.

- Ticket ID: TKTD5A63BD3
- Issue: Laptop overheating
- Status: Open
- Priority: Medium

**Status:** PASS

---



**Input:**
`Create a support ticket for my laptop overheating.`

**Approval:** NO

**Expected Result:**
The application should cancel ticket creation and avoid saving a new ticket.

**Actual Output:**
`Ticket creation cancelled. No ticket was created.`

**Status:** PASS

---



**Input:**
`What is the company's annual revenue and who is its CEO?`

**Expected Result:**
The assistant should not invent company information that is unavailable in the IT knowledge base.

**Actual Output:**
`I couldn't find this information in the available IT knowledge base. Please contact your IT support team or check official company financial reports for this information.`

**Status:** PASS

---



**Input:**
`My VPN is not connecting. Also, check ticket TKT1002.`

**Expected Result:**
The agent should execute both the knowledge-base search and ticket-status lookup tools.

**Actual Output:**
The assistant returned VPN troubleshooting instructions from `vpn_setup.md` and the correct ticket details for TKT1002.

**Tools Used:**
- `knowledge_base_search`
- `ticket_status_lookup`

**Status:** PASS

---



**Input:**
`Check the status of ticket TKT9999.`

**Expected Result:**
The assistant should report that the ticket does not exist.

**Actual Output:**
`The ticket ID TKT9999 could not be found in the system. Please verify the ticket number and try again, or contact your IT support team for further assistance.`

**Status:** PASS

---



**Input:**
`What is our company's internal VPN server address?`

**Expected Result:**
The assistant should not invent an internal VPN server address.

**Actual Output:**
`The internal VPN server address must be obtained from the company's IT department. This information is not provided in the documents.`

**Source:** `vpn_setup.md`

**Status:** PASS

---



**Initial Input:**
`My laptop is running very slowly.`

**Follow-Up Input:**
`Can you summarize the solution you gave me?`

**Expected Result:**
The assistant should preserve the original troubleshooting information without introducing unsupported steps or explanations.

**Actual Output:**
The assistant reused the original grounded RAG result instead of generating a new explanation.

**Additional Follow-Up:**
`What was the source document?`

**Actual Output:**
`Source document: laptop_configuration.md`

**Status:** PASS

---



| Test ID | Test Scenario | Result |
|---|---|---|
| TC01 | VPN configuration | PASS |
| TC02 | Password reset | PASS |
| TC03 | Ticket status retrieval | PASS |
| TC04 | Ticket creation with YES | PASS |
| TC05 | Ticket cancellation with NO | PASS |
| TC06 | Unknown questions | PASS |
| TC07 | Multi-tool workflow | PASS |
| TC08 | Incorrect ticket ID | PASS |
| TC09 | Hallucination prevention | PASS |
| TC10 | Follow-up conversation memory | PASS |

**Total Test Cases:** 10  
**Passed:** 10  
**Failed:** 0



The testing process verified the main functionality of the AI-Powered IT Support Assistant.

The assistant successfully retrieved information from internal IT documents, handled ticket-related requests, executed multiple tools in a single workflow, and maintained conversation context.

The ticket approval mechanism ensured that a support ticket was created only after explicit user approval.

The tests also demonstrated that the assistant could respond appropriately when requested information was not available in the knowledge base.

These results validate the implemented functionality for the tested scenarios. Further testing with additional documents, queries, and edge cases can improve reliability.