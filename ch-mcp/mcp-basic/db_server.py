import sqlite3
from fastmcp import FastMCP

mcp = FastMCP("SQLite Demo")

DB_PATH = "company.db"

@mcp.tool()
def list_tables():
    """Return all tables"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """).fetchall()
    conn.close()
    return [r[0] for r in rows]


@mcp.tool()
def describe_table(table_name: str):
    """Describe a table"""

    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    conn.close()

    return [
        {
            "name": r[1],
            "type": r[2]
        }
        for r in rows
    ]


@mcp.tool()
def execute_sql(query: str):
    """Execute SQL query"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    mcp.run()