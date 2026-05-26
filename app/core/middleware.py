"""
middleware.py

Middleware ghi log request.
"""

import time

from fastapi import Request


async def logging_middleware(
    request: Request,
    call_next
):
    """
    Ghi log request.
    """

    start_time = time.time()

    try:

        response = await call_next(
            request
        )

    except Exception as e:

        print(
            f"[ERROR] {str(e)}"
        )

        raise

    process_time = (
        time.time()
        - start_time
    )

    print(
        f"[{response.status_code}] "
        f"{request.method} "
        f"{request.url.path} "
        f"({process_time:.3f}s)"
    )

    return response