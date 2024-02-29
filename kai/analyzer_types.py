from dataclasses import dataclass
from enum import Enum
from typing import Any

# TODO: Rip comments from analyzer-lsp and paste here


class Category(Enum):
  potential = "potential"
  optional = "optional"
  mandatory = "mandatory" 
  

@dataclass
class Incident:
  uri: str
  message: str
  code_snip: str
  line_number: int | None
  variables: dict[str, Any]


@dataclass
class Link:
  url: str
  title: str
  

@dataclass
class Violation:
  # // Description text description about the violation
  # // TODO: we don't have this in the rule as of today.
  # Description string `yaml:"description" json:"description"`
  description: str

  # // Category category of the violation
  # // TODO: add this to rules
  # Category *Category `yaml:"category,omitempty" json:"category,omitempty"`
  category: Category | None

  # Labels []string `yaml:"labels,omitempty" json:"labels,omitempty"`
  labels: list[str]

  # // Incidents list of instances of violation found
  # Incidents []Incident `yaml:"incidents" json:"incidents"`
  incidents: list[Incident]

  # // ExternalLinks hyperlinks to external sources of docs, fixes
  # Links []Link `yaml:"links,omitempty" json:"links,omitempty"`
  links: list[Link]

  # // Extras reserved for additional data
  # Extras json.RawMessage `yaml:"extras,omitempty" json:"extras,omitempty"`
  extras: str

  # // Effort defines expected story points for this incident
  # Effort *int `yaml:"effort,omitempty" json:"effort,omitempty"`
  effort: int | None


@dataclass
class RuleSet:
  name: str
  description: str
  tags: list[str]
  violations: dict[str, Violation]
  errors: dict[str, str]
  unmatched: list[str]
  skipped: list[str]