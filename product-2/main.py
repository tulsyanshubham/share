from graph import invoke_graph

result = invoke_graph("https://github.com/sivaprasadreddy/spring-modular-monolith.git", "./monolith_code")
with (open("migration_summary.md", "w", encoding="utf-8")) as f:
    f.write(result)