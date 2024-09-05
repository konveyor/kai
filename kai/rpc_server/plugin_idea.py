import abc
import copy
from abc import abstractmethod
from typing import Any

import yaml

# --- Plugin definitions --- 

class BaseMetaPlugin(type):
    def __new__(cls, name, bases, dct):
        if "__kai_requires__" not in dct:
            raise TypeError("Plugin must define __kai_requires__")
        if "__kai_provides__" not in dct:
            raise TypeError("Plugin must define __kai_provides__")
        
        return super().__new__(cls, name, bases, dct)
    
    def __call__(self, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        if not hasattr(instance, "config"):
            raise Exception("Plugin must have a config attribute")
        
        if not hasattr(instance, "kwargs"):
            raise Exception("Plugin must have a kwargs attribute")
        
        return instance
    
class MetaPlugin(BaseMetaPlugin, abc.ABCMeta):
    """
    Metaclass for plugins that enforces the presence of __kai_requires__,
    __kai_provides__, config, and kwargs attributes. Is also an ABCMeta.
    """
    pass


class Plugin(metaclass=MetaPlugin):
    __kai_requires__: dict[str, type] = {}
    __kai_provides__: dict[str, type] = {}

    @abstractmethod
    def __init__(self, config: dict):
        self.kwargs: dict[str, Any] = {}
        self.config: dict = config

    def is_ready(self):
        """
        Returns true if all required fields are provided and are of the correct
        type.
        """
        for field in self.__kai_requires__:
            if field not in self.kwargs:
                return False

            if not isinstance(self.kwargs[field], self.__kai_requires__[field]):
                return False
            
        return True

    def supply_kwarg(self, key: str, value: Any):
        """
        Supplies the required field if it is of the correct type.
        """
        if key in self.__kai_requires__ and isinstance(value, self.__kai_requires__[key]):
            self.kwargs[key] = value

        return self.is_ready()

    def run(self):
        """
        Runs the plugin if all requirements are met.
        """
        if not self.is_ready():
            raise Exception("Requirements not met!")

        result = self._run()
        self.kwargs = {} # consume the kwargs
        
        return result

    @abstractmethod
    def _run(self):
        pass


def my_import(name: str):
    """
    Helper method to locate and import a module or class by name.
    """
    components = name.split('.')
    if len(components) == 1:
        return globals()[components[0]]
    else:
        mod = __import__(components[0])
    
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


# --- Example Plugin implementation ---

class ExamplePlugin(Plugin):
    __kai_requires__ = {
        "field_a": int,
        "field_b": int,
    }

    __kai_provides__ = {
        "field_c": int,
        "field_d": int,
    }

    def __init__(self, config: dict):
        self.config = config
        self.kwargs = {}

        self.some_config_a = config.get("args").get("some_config_a")
        self.some_config_b = config.get("args").get("some_config_b")

    def _run(self):
        return {
            "field_c": self.some_config_a * (self.kwargs["field_a"] + self.kwargs["field_b"]),
            "field_d": self.some_config_b * (self.kwargs["field_a"] - self.kwargs["field_b"]),
        }


# --- Example usage ---

# The main idea is that we trigger the first plugin, and then as soon as another
# plugin is ready to run, we add it to the queue to run. We keep running plugins
# until there are no more plugins to run.

# First, provide a configuration saying how everything will be hooked together

example_config_yaml = """
defaults:
  # Default configuration for all plugins, will be overridden by plugin specific
  # configuration.
  llm:
    provider: blah
    connection_string: blah

plugins:
  - name: example_plugin_a  # Name of the instance of the plugin
    id: ExamplePlugin  # Name of the class of the plugin
    args:
      # Specific configuration for this instance of the plugin
      some_config_a: 3
      some_config_b: 4
    sends:
      # If not specified
      #   Option 1: Send all results to next plugin, discard any not immediately 
      #             consumed.
      #   Option 2: Send all results to next plugin, any results not immediately
      #             consumed are stored in state.

      # TODO: Partially sent errors?
      - field: field_c
        plugin: example_plugin_b
        # If not specified field is used
        renamed_field: field_a
      - field: field_d
        plugin: example_plugin_b
        renamed_field: field_b

  - name: example_plugin_b
    id: ExamplePlugin
    args: 
      some_config_a: 5
      some_config_b: 6
    some_config_a: 5
    some_config_b: 6
"""

config_yaml = yaml.safe_load(example_config_yaml)
plugins: dict[str, Plugin] = {}
final_state = {} # Final state. Any unsent variables are stored here.

for plugin_config in config_yaml["plugins"]:
    plugin_config = copy.deepcopy(plugin_config)
    
    cls = my_import(plugin_config["id"])

    print(f"Loading plugin {plugin_config['name']} with class {cls}")

    if not issubclass(cls, Plugin):
        raise Exception(f"Class {cls} is not a subclass of Plugin")
    
    defaults = config_yaml.get("defaults", {})
    plugin_config["args"] = {**defaults, **plugin_config.get("args", {})}

    instance = cls(plugin_config)
    plugins[plugin_config["name"]] = instance

# Initialize the plugin queue with the first plugin in the list
plugin_queue = [plugins[config_yaml["plugins"][0]["name"]]]


# Supply the required fields, this would be state in the real implementation
plugin_queue[0].supply_kwarg("field_a", 3)
plugin_queue[0].supply_kwarg("field_b", 4)

while len(plugin_queue) > 0:
    plugin = plugin_queue.pop(0)

    print(f"Running plugin {plugin.config.get("name")}")

    result = plugin.run()

    unsent_variables = set(plugin.__kai_provides__)

    for send in plugin.config.get("sends", []):
        next_plugin = plugins[send["plugin"]]

        src_field = send.get("field")
        dst_field = send.get("renamed_field", src_field)

        next_plugin.supply_kwarg(dst_field, result[src_field])

        if next_plugin.is_ready() and next_plugin not in plugin_queue:
            plugin_queue.append(next_plugin)

        unsent_variables.remove(src_field)

    for unsent in unsent_variables:
        final_state[unsent] = result[unsent]

print(final_state)