from typing import Any


class Wrapper:
    """
    Wrapper class to intercept and log all attribute access and method calls on
    an object.
    """

    def __init__(self, obj: Any):
        self.obj: Any = obj
        self.callable_results: list = []

    def __getattr__(self, attr: Any):
        print(f"Getting {type(self.obj).__name__}.{attr}")

        result = getattr(self.obj, attr)
        if callable(result):
            return self.CallableWrapper(self, result)

        return result

    class CallableWrapper:
        def __init__(self, parent: "Wrapper", callable: Any):
            self.parent = parent
            self.callable = callable

        def __call__(self, *args, **kwargs):
            print(f"Calling {type(self.parent.obj).__name__}.{self.callable.__name__}")

            for i, arg in enumerate(args):
                print(f"  arg {i}: {arg}")
            for key, value in kwargs.items():
                print(f"  {key}: {value}")

            result = self.callable(*args, **kwargs)
            self.parent.callable_results.append(result)
            return result
