from tools import get_ticket_status

print("\n========== TICKET STATUS TOOL TEST ==========")

ticket_id = "TKT1002"

print("\nInput Ticket ID:")
print(ticket_id)

result = get_ticket_status(ticket_id)

print("\nTool Output:")
print(result)

print("\n========== TEST COMPLETED ==========")