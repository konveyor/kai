import logging
import sys
from datetime import datetime
from typing import Any

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kai_mcp_server.log"),
        logging.StreamHandler(sys.stderr),
    ],
)

logger = logging.getLogger("kai_mcp_solution_server")

# Keep the original log function for compatibility but enhance it
log_file = open("stderr.log", "a+")
log_file.close()


def log(*args: Any, **kwargs: Any) -> None:
    """Legacy log function - enhanced with timestamp and logging level"""
    timestamp = datetime.now().isoformat()
    message = " ".join(str(arg) for arg in args)
    logger.info(message)
    print(
        f"[{timestamp}] {message}",
        file=log_file if not log_file.closed else sys.stderr,
        **kwargs,
    )
