class PluginError(Exception):
    "Base plugin exception."



class PluginExecutionError(PluginError):
   "Raised when plugin execution fails."


class PluginConfigError(PluginError):
   "Raised when plugin configuration is invalid."
