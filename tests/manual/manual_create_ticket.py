from tools import create_support_ticket
print("\n========== CREATE SUPPORT TICKET TEST ==========")
issue = "My company laptop is overheating frequently."
print("\nIssue Description:")
print(issue)
result = create_support_ticket(issue)
print("\nTool Output:")
print(result)
print("\n========== TEST COMPLETED ==========")