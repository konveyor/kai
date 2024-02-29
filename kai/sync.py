from functools import singledispatch, wraps
import asyncio
import inspect
import types
import threading
from typing import Any, Callable, Generator, TypeVar
T = TypeVar('T')

def _start_background_loop(loop: asyncio.AbstractEventLoop):
  asyncio.set_event_loop(loop)
  loop.run_forever()

_LOOP = asyncio.new_event_loop()
_LOOP_THREAD = threading.Thread(
  target=_start_background_loop, args=(_LOOP,), daemon=True
)
_LOOP_THREAD.start()


@singledispatch
def sync(co: Any):
  raise TypeError('Called with unsupported argument: {}'.format(co))


@sync.register(asyncio.Future)
@sync.register(types.GeneratorType)
def sync_co(co: Generator[Any, None, Any]) -> Any:
  if not inspect.isawaitable(co):
    raise TypeError('Called with unsupported argument: {}'.format(co))
  return asyncio.run_coroutine_threadsafe(co, _LOOP).result()


@sync.register(types.FunctionType)
@sync.register(types.MethodType)
def sync_fu(f: Callable[..., Any]) -> Callable[..., Any]:
  if not asyncio.iscoroutinefunction(f):
    raise TypeError('Called with unsupported argument: {}'.format(f))

  @wraps(f)
  def run(*args, **kwargs):
    return asyncio.run_coroutine_threadsafe(f(*args, **kwargs), _LOOP).result()
  return run


sync.register(types.CoroutineType)(sync_co)