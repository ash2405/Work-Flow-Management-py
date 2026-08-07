"""Middleware components."""


def auth_middleware(request, call_next):
    return call_next(request)
