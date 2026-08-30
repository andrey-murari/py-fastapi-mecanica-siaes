from pydantic import ValidationError


def value_error_from(exc: ValidationError) -> ValueError:
    """Surfaces the entity rule that failed so routers can answer 400."""
    first = exc.errors()[0]
    ctx_error = (first.get("ctx") or {}).get("error")
    if ctx_error is not None:
        return ValueError(str(ctx_error))
    return ValueError(first["msg"])
