import functools
import inspect
from collections.abc import Callable
from typing import Protocol, TypeVar

from typing_extensions import Concatenate, ParamSpec

from pymino.ext import entities

__all__ = ("authenticated",)

A = TypeVar("A", bound="AuthCheckable")
R = TypeVar("R")
P = ParamSpec("P")


class AuthCheckable(Protocol):
    @property
    def is_authenticated(self) -> bool: ...

def authenticated(func: Callable[Concatenate[A, P], R]) -> Callable[Concatenate[A, P], R]:
    """A decorator that checks if the client is authenticated.

    :param func: The function to decorate.
    :type func: F
    :return: The decorated function.
    :rtype: F

    This decorator is used to check if the client is authenticated.
    If the client is not authenticated, a `LoginRequired` exception
    will be raised.
    """
    @functools.wraps(func)
    def wrapper(self: A, *args: P.args, **kwargs: P.kwargs) -> R:
        if not self.is_authenticated:
            raise entities.LoginRequired
        return func(self, *args, **kwargs)
    wrapper.__signature__ = inspect.signature(func)  # pyright: ignore[reportAttributeAccessIssue]
    return wrapper
