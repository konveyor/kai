#!/usr/bin/env python3
"""
SSL Utilities for MCP Client

This module provides utilities for bypassing SSL certificate verification
when the --insecure flag is used. This is needed because fastmcp doesn't
currently support SSL verification configuration options.
"""

import logging
import os
import ssl
import warnings
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Store the original SSL context creator to restore it later
_original_ssl_create_default_context: Optional[Callable[..., ssl.SSLContext]] = None


class SSLMonkeyPatch:
    """
    Context manager that applies and cleans up SSL monkey patches
    for bypassing certificate verification.
    """

    def __init__(self):
        self.original_ssl_create_default_context = ssl.create_default_context
        self.original_httpx_client_init = None
        self.original_httpx_async_client_init = None
        self.env_vars_to_cleanup = []
        self.httpx_patched = False

    def __enter__(self):
        """Apply SSL monkey patches."""
        return self.apply_ssl_bypass()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up SSL monkey patches."""
        self.restore_ssl_settings()

    def apply_ssl_bypass(self) -> "SSLMonkeyPatch":
        """
        Apply SSL monkey patches to bypass certificate verification.

        This patches:
        1. ssl.create_default_context to disable verification
        2. httpx.Client and httpx.AsyncClient (if available) to pass verify=False
        3. Environment variables as fallback options
        """
        logger.debug("Applying SSL monkey patches to bypass certificate verification")

        # Disable SSL verification warnings
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        warnings.filterwarnings("ignore", category=Warning)

        # Patch SSL module's default context creator to disable verification
        def unverified_context(*args, **kwargs):
            context = self.original_ssl_create_default_context(*args, **kwargs)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            return context

        # Apply the SSL patch
        ssl.create_default_context = unverified_context
        logger.debug("Successfully patched ssl.create_default_context")

        # Try to patch httpx if it's available
        self._patch_httpx()

        # Set environment variables as backup
        self._set_ssl_env_vars()

        return self

    def _patch_httpx(self):
        """Patch httpx Client classes if httpx is available."""
        try:
            import httpx

            # Store original methods
            self.original_httpx_client_init = httpx.Client.__init__
            self.original_httpx_async_client_init = httpx.AsyncClient.__init__

            def patched_client_init(client_self, *args, **kwargs):
                kwargs["verify"] = False
                self.original_httpx_client_init(client_self, *args, **kwargs)

            def patched_async_client_init(client_self, *args, **kwargs):
                kwargs["verify"] = False
                self.original_httpx_async_client_init(client_self, *args, **kwargs)

            httpx.Client.__init__ = patched_client_init
            httpx.AsyncClient.__init__ = patched_async_client_init

            self.httpx_patched = True
            logger.debug("Successfully patched httpx Client classes")

        except ImportError:
            logger.debug("httpx not available, skipping httpx patches")
        except Exception as e:
            logger.warning("Failed to patch httpx: %s", e)

    def _set_ssl_env_vars(self):
        """Set environment variables to disable SSL verification."""
        ssl_env_vars = {
            "SSL_CERT_VERIFY": "false",
            "HTTPX_SSL_VERIFY": "false",
            "HTTPX_NO_VERIFY": "true",
            "PYTHONHTTPSVERIFY": "0",
        }

        for env_var, value in ssl_env_vars.items():
            if env_var not in os.environ:
                os.environ[env_var] = value
                self.env_vars_to_cleanup.append(env_var)

        logger.debug("Set SSL environment variables: %s", list(ssl_env_vars.keys()))

    def restore_ssl_settings(self):
        """Restore original SSL settings and clean up patches."""
        logger.debug("Restoring original SSL settings")

        # Restore original SSL context creator
        ssl.create_default_context = self.original_ssl_create_default_context
        logger.debug("Restored original ssl.create_default_context")

        # Restore httpx patches if they were applied
        if self.httpx_patched:
            try:
                import httpx

                if self.original_httpx_client_init:
                    httpx.Client.__init__ = self.original_httpx_client_init
                if self.original_httpx_async_client_init:
                    httpx.AsyncClient.__init__ = self.original_httpx_async_client_init
                logger.debug("Restored original httpx Client classes")
            except Exception as e:
                logger.warning("Failed to restore httpx patches: %s", e)

        # Clean up environment variables we set
        for env_var in self.env_vars_to_cleanup:
            if env_var in os.environ:
                del os.environ[env_var]

        logger.debug(
            "Cleaned up SSL environment variables: %s", self.env_vars_to_cleanup
        )


def apply_ssl_bypass() -> SSLMonkeyPatch:
    """
    Apply SSL monkey patches to bypass certificate verification.

    Returns:
        SSLMonkeyPatch instance that can be used to restore settings

    Example:
        # Context manager (recommended)
        with apply_ssl_bypass():
            # SSL verification is bypassed here
            client = Client(transport="https://self-signed.example.com")
            async with client:
                pass
        # SSL settings automatically restored

        # Manual management
        patch = apply_ssl_bypass()
        try:
            # SSL verification is bypassed here
            pass
        finally:
            patch.restore_ssl_settings()
    """
    return SSLMonkeyPatch().apply_ssl_bypass()
