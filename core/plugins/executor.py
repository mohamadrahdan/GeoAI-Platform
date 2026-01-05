# Plugin execution engine (sync execution with a clean contract)

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type
from core.plugins.errors import PluginExecutionError
from core.plugins.interface import BasePlugin
from core.plugins.registry import PluginRegistry
from core.logging.logger import Logger

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from core.plugins.errors import PluginExecutionError, PluginTimeoutError

@dataclass
class PluginExecutor:
    """
    Responsible for instantiating and executing plugins.
    Notes:
    - Keeps "execution" separated from "discovery/registration"
    - Can be extended later for async execution, resource limits, etc.
    """
    registry: PluginRegistry
    logger: Logger
    default_timeout_seconds: float = 10.0

    def _create_instance(self, plugin_cls: Type[BasePlugin]) -> BasePlugin:
        # Plugins can receive config later; for now we pass empty config
        try:
            return plugin_cls(config={})
        except Exception as exc:
            raise PluginExecutionError(f"Failed to initialize plugin '{plugin_cls.__name__}': {exc}") from exc

    def run(self, plugin_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        " Run plugin by name with payload and return raw result dict"
        plugin_cls = self.registry.get(plugin_name)
        plugin = self._create_instance(plugin_cls)

        self.logger.info("Running plugin: %s (%s)", plugin_name, getattr(plugin, "version", "unknown"))
        try:
            result = plugin.run(payload)
        except Exception as exc:
            self.logger.error("Plugin '%s' execution failed: %s", plugin_name, exc)
            raise PluginExecutionError(f"Plugin '{plugin_name}' failed during run(): {exc}") from exc
        finally:
            # Best-effort shutdown hook
            try:
                plugin.shutdown()
            except Exception:
                self.logger.warning("Plugin '%s' shutdown hook failed (ignored).", plugin_name)

        return result
    
    def run_with_timeout(
        self,
        plugin_name: str,
        payload: Dict[str, Any],
        timeout_seconds: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Run plugin with a timeout (best-effort).
        Uses a thread pool to enforce time limits for sync plugin code.
        """
        timeout = timeout_seconds if timeout_seconds is not None else self.default_timeout_seconds

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(self.run, plugin_name, payload)
            try:
                return future.result(timeout=timeout)
            except FuturesTimeoutError as exc:
                self.logger.error("Plugin '%s' timed out after %s seconds", plugin_name, timeout)
                raise PluginTimeoutError(f"Plugin '{plugin_name}' timed out after {timeout} seconds") from exc