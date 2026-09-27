"""MCP server for Case A expense claim context lookup tools."""

from mcp.server.fastmcp import FastMCP

from expense.tools import get_claim, get_employee, get_policy_limits, record_decision
from expense.review import review_claim


server = FastMCP("expense", log_level="WARNING")

server.tool()(get_claim)
server.tool()(get_employee)
server.tool()(get_policy_limits)
server.tool()(record_decision)
server.tool()(review_claim)


if __name__ == "__main__":
    server.run()
