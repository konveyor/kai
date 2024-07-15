from typing import Optional

from pydantic import BaseModel, validator


class Incident(BaseModel):
    ruleset_name: str
    violation_name: str
    uri: Optional[str] = ""
    incident_snip: Optional[str] = ""
    incident_variables: dict
    line_number: Optional[int]  # 0-indexed
    analysis_message: str

    @validator("line_number", pre=True)
    def convert_str_to_int(cls, value):
        if isinstance(value, str):
            if value == "":
                return None
            try:
                # Attempt to convert the string to an integer
                return int(value)
            except ValueError as err:
                # If conversion fails, raise an error
                raise ValueError("Quantity must be an integer") from err
        return value
