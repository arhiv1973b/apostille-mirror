import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def run_test():
    server_params = StdioServerParameters(
        command="python", 
        args=["H:\\ACTOR_DEV_ENV\\mcp_server.py"]
    )
    
    print("--- Запуск теста MCP-сервера ---")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Тест: вызов функции
            print("--- Вызов get_audit_events ---")
            result = await session.call_tool("get_audit_events", arguments={})
            print("Результат:", result)

if __name__ == "__main__":
    asyncio.run(run_test())
