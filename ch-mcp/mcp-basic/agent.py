import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
import settings

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

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

    agent = llm.bind_tools(tools)

    while(True):
      prompt = input("enter query : ")
      if prompt.lower() in ["exit", "quit", "stop"]:
         print("Stopped...")
         break
      result = await agent.ainvoke(prompt)
      print(result)

asyncio.run(main())