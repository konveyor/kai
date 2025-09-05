#!/usr/bin/env python
"""
Database management script for KAI MCP Solution Server.

This script provides database management commands that should be run manually,
such as dropping all tables or initializing the database schema.
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import server modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kai_mcp_solution_server.db.dao import Base, drop_everything, get_async_engine
from kai_mcp_solution_server.server import SolutionServerSettings


async def drop_all_tables(settings: SolutionServerSettings) -> None:
    """Drop all database tables."""
    print(f"Connecting to database: {settings.db_dsn}")

    # Confirm with user
    response = input(
        "⚠️  WARNING: This will DROP ALL TABLES in the database. Are you sure? (yes/N): "
    )
    if response.lower() != "yes":
        print("Aborted.")
        return

    engine = await get_async_engine(settings.db_dsn)

    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(drop_everything)
        print("✅ All tables dropped successfully.")

    await engine.dispose()


async def reset_database(settings: SolutionServerSettings) -> None:
    """Drop all tables and recreate them (full reset)."""
    print(f"Connecting to database: {settings.db_dsn}")

    # Confirm with user
    response = input(
        "⚠️  WARNING: This will RESET the entire database (drop and recreate all tables). Are you sure? (yes/N): "
    )
    if response.lower() != "yes":
        print("Aborted.")
        return

    engine = await get_async_engine(settings.db_dsn)

    async with engine.begin() as conn:
        print("Dropping all tables...")
        await conn.run_sync(drop_everything)
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database reset successfully.")

    await engine.dispose()


async def main():
    parser = argparse.ArgumentParser(
        description="Manage KAI MCP Solution Server database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Drop all tables (DANGEROUS - deletes all data)
  python scripts/manage_db.py drop
  
  # Reset database (drop and recreate all tables)
  python scripts/manage_db.py reset
  
  # Use a specific database
  KAI_DB_DSN="postgresql://user:pass@localhost/dbname" python scripts/manage_db.py reset
  
  # Skip confirmation prompts (use with caution!)
  python scripts/manage_db.py reset --force

Note: The server automatically creates tables on startup, so there's no need for
an 'init' command. Use 'reset' if you need fresh tables.
""",
    )

    parser.add_argument("command", choices=["drop", "reset"], help="Command to execute")

    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts (use with caution!)",
    )

    args = parser.parse_args()

    # Load settings from environment
    try:
        settings = SolutionServerSettings()
    except Exception as e:
        print(f"❌ Error loading settings: {e}")
        print("\nMake sure to set required environment variables:")
        print("  - KAI_DB_DSN: Database connection string")
        print('  - KAI_LLM_PARAMS: LLM configuration (can be \'{"model": "fake"}\')')
        sys.exit(1)

    # Override confirmation if --force is used
    if args.force:
        # Monkey-patch input to always return "yes"
        import builtins

        builtins.input = lambda _: "yes"

    try:
        if args.command == "drop":
            await drop_all_tables(settings)
        elif args.command == "reset":
            await reset_database(settings)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
