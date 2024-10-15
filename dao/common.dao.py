# utils
from libs.utils.decorators import step


class CommonDao(object):

    def __init__(self, _db=None) -> None:
        self.db = _db

    @step("[DAO] execute_query_dao ...", 2)
    def execute_query_dao(self, _sql_query):
        self.db.execute_query(_sql_query)
        return True
