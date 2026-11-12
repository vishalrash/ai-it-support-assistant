
import json
from pathlib import Path

ticket_file = Path("data/tickets.json")

with ticket_file.open("r", encoding="utf-8") as file:
    tickets = json.load(file)

print("\n========== TICKET DATABASE VERIFICATION ==========")

print("Total tickets:", len(tickets))

print("\nSaved tickets:")

for ticket in tickets:
    print(
        ticket["ticket_id"],
        "|",
        ticket["issue_description"],
        "|",
        ticket["status"]
    )

created_ticket = next(
    (
        ticket for ticket in tickets
        if ticket["ticket_id"] == "TKTEF32F2DB"
    ),
    None
)

assert created_ticket is not None, (
    "Approved ticket was not found!"
)

print("\nApproved ticket exists in JSON: YES")

cancelled_ticket = any(
    ticket["issue_description"] == "My office printer is not working."
    and ticket["ticket_id"] != "TKTEF32F2DB"
    for ticket in tickets
)

print("Unexpected duplicate ticket:", cancelled_ticket)

print("\n========== VERIFICATION COMPLETED ==========")
