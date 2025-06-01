import logging

logger = logging.getLogger(__name__)

async def fetch_request_with_error_handling(fetch_func, *args, fallback_msg=None, **kwargs):
    try:
        response = await fetch_func(*args, **kwargs)
        return {
            "status_code": 200,
            "data": response
        }
    except Exception as e:
        status_code = 503
        if hasattr(e, "response") and e.response is not None:  # type: ignore
            status_code = getattr(e.response, "status_code", status_code)  # type: ignore
        logger.error(f"API request failed: {e}")
        return {
            "status_code": status_code,
            "data": fallback_msg or "Sorry, we couldn't fetch the data right now. Please try again later."
        }
