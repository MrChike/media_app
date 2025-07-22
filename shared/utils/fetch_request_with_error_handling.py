import logging

logger = logging.getLogger(__name__)


async def fetch_request_with_error_handling(
    func, *args, status_code=200,
    custom_user_success_response=None,
    custom_user_error_response="Sorry, something went wrong. \
        Please try again shortly.",
    **kwargs
):
    try:
        response = await func(*args, **kwargs)
        return {
            "status_code": status_code,
            "data": (
                response
                if response is not None
                else custom_user_success_response
            )
        }
    except Exception as e:
        # Default to 503, override if there's a response with a status_code
        status_code = 503
        if hasattr(e, "response") and e.response is not None:  # type: ignore
            status_code = getattr(e.response,  # type: ignore
                                  "status_code", status_code)

        # Log internal details
        log_details = f"Error during execution of {func.__name__}: {str(e)}"

        logger.error("============== ERROR =================")
        logger.error(log_details)
        logger.error("============== ERROR =================")

        return {
            "status_code": status_code,
            "data": custom_user_error_response
        }
