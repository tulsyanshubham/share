from graph_old import invoke_graph
import asyncio

async def main():
    result = await invoke_graph("https://github.com/xsreality/spring-modulith-with-ddd.git", "./monolith_code")
    with (open("migration_summary.md", "w", encoding="utf-8")) as f:
        f.write(result)
        
if __name__ == "__main__":
    asyncio.run(main())