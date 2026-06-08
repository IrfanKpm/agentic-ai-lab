import asyncio
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
import settings

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

SYSTEM_PROMPT = """You are a helpful data analyst with access to a SQLite database.

Today's date is {today}.

You have these tools:
- list_tables: see all tables
- describe_table(table_name): see columns and types of a table  
- execute_sql(query): run any SELECT query

STRICT RULES — follow in order every single time:
1. ALWAYS call list_tables first to see what tables exist
2. ALWAYS call describe_table on every relevant table before writing ANY query
3. Only THEN write execute_sql using the exact column names you saw — never guess
4. Give a clear, concise answer after you have the data
"""

async def main():
    client = MultiServerMCPClient(
        {
            "db": {
                "command": "python",
                "args": ["db_server.py"],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    print("TOOLS:")
    for t in tools:
        print(t.name)

    tool_map = {t.name: t for t in tools}
    agent = llm.bind_tools(tools)

    while True:
        prompt = input("\nenter query : ")
        if prompt.lower() in ["exit", "quit", "stop"]:
            print("Stopped...")
            break

        # Inject today's date fresh each query
        system = SystemMessage(content=SYSTEM_PROMPT.format(
            today=datetime.now().strftime("%Y-%m-%d")
        ))
        messages = [system, HumanMessage(content=prompt)]

        while True:
            response = await agent.ainvoke(messages)
            messages.append(response)

            if not response.tool_calls:
                print("\nAnswer:", response.content)
                break

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id   = tool_call["id"]

                print(f"  [calling tool: {tool_name}({tool_args})]")

                tool = tool_map[tool_name]
                tool_result = await tool.ainvoke(tool_args)

                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_id,
                    )
                )

asyncio.run(main())