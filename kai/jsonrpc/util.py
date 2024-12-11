import logging
import os
from pathlib import Path
from typing import Annotated, Any

from pydantic import AfterValidator, AliasChoices, AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


def log_record_to_dict(record: logging.LogRecord) -> dict[str, Any]:
    return {
        "name": record.name,
        "levelno": record.levelno,
        "levelname": record.levelname,
        "pathname": record.pathname,
        "filename": record.filename,
        "module": record.module,
        "lineno": record.lineno,
        "funcName": record.funcName,
        "created": record.created,
        "asctime": record.asctime,
        "msecs": record.msecs,
        "relativeCreated": record.relativeCreated,
        "thread": record.thread,
        "threadName": record.threadName,
        "process": record.process,
        "msg": record.msg,
        "args": record.args,
        "message": record.getMessage(),
    }


AutoAbsPath = Annotated[Path, AfterValidator(lambda x: Path(os.path.abspath(x)))]
"""
`AutoAbsPath` is a type that can be used with Pydantic models to automatically
convert an inputted relative path to an absolute path. This is different than
`.resolve()` because it will resolve relative paths, but not symlinks. For
example:

```python
class TheModel(BaseModel):
    the_path: AutoAbsPath

the_model = TheModel(the_path="build/build.spec")
print(the_model.the_path)  #/path/to/build/build.spec
```
"""

AutoUpperStr = Annotated[str, AfterValidator(lambda x: x.upper())]
"""
`AutoUpperStr` is a type that can be used with Pydantic models to automatically
convert an inputted string to uppercase.
"""


class CamelCaseBaseModel(BaseModel):
    """
    This class will accept both camelCase and snake_case keys when creating an
    instance of the model. When serializing, it will produce camelCase keys.
    For example:

    ```python
    class TheModel(CamelCaseBaseModel):
        the_thing: str

    a = TheModel.model_validate({"theThing": "hello"})  # Works!
    b = TheModel.model_validate({"the_thing": "hello"})  # Works!
    c = TheModel(the_thing="hello").model_dump()  # {"theThing": "hello"}
    ```
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=lambda field_name: AliasChoices(
                field_name,
                to_camel(field_name),
            ),
            serialization_alias=to_camel,
        ),
        populate_by_name=True,
    )

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        return super().model_dump(by_alias=True, **kwargs)
