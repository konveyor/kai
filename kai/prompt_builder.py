import string
from enum import Enum

# TODO: Unify the model selection criteria across PromptBuilder, IncidentStore
# embeddings and the actual llm call itself


class PromptBuilderModels(Enum):
  pass


class PromptBuilder:
  def __init__(self, template_path: str):
    with open(template_path, "r+") as f:
      self.template = f.read()
      
    itr = string.Formatter().parse(self.template)
    template_vars = [v[1] for v in itr if v[1] is not None]
    self.template_dict = {k: "" for k in template_vars}


  def get_formatted_template(self):
    return self.template.format(**self.template_dict)


  def get_template_keys(self):
    return self.template_dict.keys()


  def get_template_value(self, key: str):
    return self.template_dict[key]


  def set_template_value(self, key: str, val: str):
    self.template_dict[key] = val