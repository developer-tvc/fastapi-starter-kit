from contextvars import ContextVar

current_ip: ContextVar[str | None] = ContextVar("current_ip", default=None)