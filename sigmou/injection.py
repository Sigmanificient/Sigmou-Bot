from functools import wraps


def client_injection(client):
    """Take a client instance to inject into future events."""
    def client_setter(func):
        return wrapped_event(client, func)

    return client_setter


def wrapped_event(client, func):
    """Create a modified event that with client arg invisible to dpy."""
    @wraps(func)
    async def event(*args):
        await func(client, *args)

    return event
