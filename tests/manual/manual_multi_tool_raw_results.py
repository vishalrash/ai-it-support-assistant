from langchain_tools import (
    knowledge_base_search,
    ticket_status_lookup
)

print("\n========== VPN KNOWLEDGE BASE RESULT ==========")

vpn_result = knowledge_base_search.invoke({
    "query": "My company VPN is not connecting. How can I troubleshoot it?"
})

print(vpn_result)

print("\n========== TICKET STATUS RESULT ==========")

ticket_result = ticket_status_lookup.invoke({
    "ticket_id": "TKT1002"
})

print(ticket_result)

print("\n========== TEST COMPLETED ==========")