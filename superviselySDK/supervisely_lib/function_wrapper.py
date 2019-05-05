# coding: utf-8

import os
import traceback
from supervisely_lib.sly_logger import logger, EventType


SLY_DEBUG = 'SLY_DEBUG'


def main_wrapper(main_name, main_func, *args, **kwargs):
    try:
        logger.debug('Main started.', extra={'main_name': main_name})
        main_func(*args, **kwargs)
    except Exception as e:
        logger.critical('Unexpected exception in main.', exc_info=True, extra={
            'main_name': main_name,
            'event_type': EventType.TASK_CRASHED,
            'exc_str': str(e),
        })
        logger.debug('Main finished: BAD.', extra={'main_name': main_name})

        if os.environ.get(SLY_DEBUG):
            raise
        else:
            os._exit(1)
    else:
        logger.debug('Main finished: OK.', extra={'main_name': main_name})


def function_wrapper(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except Exception as e:
        logger.error(traceback.format_exc(), exc_info=True, extra={'exc_str': str(e)})
        raise e


def catch_silently(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception:
        return None


def function_wrapper_nofail(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except Exception as e:
        logger.error(traceback.format_exc(), exc_info=True, extra={'exc_str': str(e)})