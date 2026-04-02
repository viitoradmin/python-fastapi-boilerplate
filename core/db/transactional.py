from functools import wraps

from config import db_config


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await db_config.session.commit()
            except Exception as e:
                await db_config.session.rollback()
                raise e

            return result

        return _transactional
