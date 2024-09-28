# MySQL
class MySQLCredential(object):

    def __init__(
        self,
        _db_name,
        _user=None,
        _password=None,
        _host=None,
        _port=None,
        _cluster_arn=None,
        _secret_arn=None,
    ):
        self.db_name = _db_name
        self.user = _user
        self.password = _password
        self.host = _host if _host else "localhost"
        self.port = _port if _port else 3306
        self.cluster_arn = _cluster_arn
        self.secret_arn = _secret_arn

