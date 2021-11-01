import logging


def conditional_action(condition: bool, action: callable, **kw_args) -> None:
    if condition:
        logger.debug(f'{condition} >> calling {action}')
        action(**kw_args)
    else:
        logger.debug(f'{condition} >> noting to do.')


logger = logging.getLogger(__name__)
