# python libraries
import copy
import logging
from enum import Enum

# sqlalchemy
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import StatementError
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy_pagination import paginate

# utils
from libs.utils.decorators import step

# errors
from libs.errors.source_error import SourceError
from libs.errors.source_error import NoRecordFoundError
from libs.errors.source_error import NoRecordsFoundError
from libs.errors.source_error import DuplicateRecordError
from libs.errors.source_error import MultipleRecordsFoundError


class JoinType(Enum):
    JOIN = "join"
    OUTER = "outerjoin"


class MySQLSource(object):

    def __init__(self, _credential_obj, _logger=None):
        self.engine = None
        self.credential_obj = _credential_obj
        self.session = None
        self.records_per_page = 20
        self.logger = _logger or logging.getLogger(__name__)

    def close_connection(self):
        if self.session:
            self.session.rollback()
            self.session.close()

        if self.engine:
            self.engine.dispose()

    def set_engine(self, ):
        if self.engine:
            return True

        try:
            URL_CONNECTION = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                self.credential_obj.user,
                self.credential_obj.password,
                self.credential_obj.host,
                self.credential_obj.port,
                self.credential_obj.db_name
            )
            self.engine = create_engine(URL_CONNECTION)

            session_mysql = sessionmaker(bind=self.engine, expire_on_commit=False)
            self.session = session_mysql()

        except Exception as e:
            msg = str(e)
            self.logger.info(msg)
            self.close_connection()
            raise SourceError(_message=msg)

    @step("[Source] get_tables ...", 3)
    def get_tables(self):
        self.set_engine()
        try:
            metadata_obj = MetaData()
            metadata_obj.reflect(self.engine)
            return list(metadata_obj.tables.keys())

        except Exception as e:
            msg = str(e)
            self.logger.info(msg)
            raise SourceError(_message=msg)

    @step("[Source] create_table ...", 3)
    def create_table(self, _model):
        self.logger.info(f"Creating table...: {_model.__tablename__}")
        self.set_engine()

        try:
            _model.__table__.create(self.engine)

        except Exception as e:
            msg = str(e)
            self.logger.info(msg)
            raise SourceError(_message=msg)

    @step("[Source] select_one ...", 3)
    def select_one(self, _model):
        self.set_engine()

        filters = _model.get_dict(_nulls=False)

        if bool(filters) is False:
            raise SourceError("No value was specified in any attribute.")

        try:
            query = self.session.query(_model.__class__)
            for key in filters.keys():
                query = query.filter(
                    getattr(_model.__class__, key) == filters[key]
                )

            record = query.one()
            return record

        except NoResultFound:
            msg = "Record not found"
            raise NoRecordFoundError(
                _message=msg,
                _error=msg,
            )

        except MultipleResultsFound:
            msg = "There is more than one record"
            raise MultipleRecordsFoundError(
                _message=msg,
                _error=msg,
            )

        except StatementError as e:
            raise SourceError(e.args[0])

        except Exception as e:
            msg = str(e)
            self.logger.info(msg)
            raise SourceError(
                _message=msg,
                _error=msg,
            )

    @step("[Source] select_many ...", 3)
    def select_many(
        self,
        _model,
        _custom_filters=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.logger.info(f'Searching in table...: {_model.__table__}')
        self.set_engine()

        try:
            if _custom_filters is not None:
                query = self.session.query(_model.__class__)
                query = query.filter(_custom_filters)

            else:
                filters = _model.get_dict(_nulls=False)

                if bool(filters) is False:
                    query = self.session.query(_model.__class__)

                else:
                    query = self.session.query(_model.__class__)
                    for key in filters.keys():
                        query = query.filter(
                            getattr(_model.__class__, key) == filters[key]
                        )

            records = None
            self.records_per_page = _limit
            if _order_column:
                if _arrange == "asc":
                    page = paginate(
                        query.order_by(asc(_order_column)),
                        _page,
                        self.records_per_page
                    )
                else:
                    page = paginate(
                        query.order_by(desc(_order_column)),
                        _page,
                        self.records_per_page
                    )

            else:
                page = paginate(
                    query,
                    _page,
                    self.records_per_page
                )

            records = page.items
            next_page = page.next_page

        except StatementError as e:
            msg = str(e)
            self.logger.info(msg)
            self.close_connection()
            raise SourceError(e.args[0])

        except Exception as e:
            msg = str(e)
            self.logger.info(msg)
            self.close_connection()
            raise SourceError(
                _message=msg,
                _source="select_many"
            )

        qty_records = len(records)
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="select_many"
            )

        self.logger.info(f'{qty_records} records found')
        return records, next_page

    @step("[Source] select_many_by_query ...", 3)
    def select_many_by_query(self, _model, _query):
        self.set_engine()

        if _query is None:
            raise SourceError(f"_query:{_query} param is None")

        filters = _model.get_dict(_nulls=False)

        try:
            query = self.session.execute(_query, filters)
            records = query.fetchall()

            qty_records = len(records)

            if qty_records == 0:
                raise NoRecordFoundError('Records not found')

            record_list = []

            for record in records:
                index = 0
                model_item = copy.deepcopy(_model)
                for column_name in query.keys():
                    setattr(model_item, column_name, record[index])
                    index += 1

                record_list.append(model_item)

            return record_list

        except StatementError as e:
            msg = str(e)
            self.close_connection()
            self.logger.info(msg)
            raise SourceError(e.args[0])

        except Exception as e:
            msg = str(e)
            self.session.rollback()
            self.logger.info(msg)
            raise SourceError(msg)

    @step("[Source] truncate_table ...", 3)
    def truncate_table(self, _table):
        self.set_engine()
        try:
            query = f"TRUNCATE TABLE {_table}"
            self.session.execute(query)
            self.logger.info(f'succsessful on table: {_table}')

            return True

        except StatementError as e:
            msg = str(e)
            self.close_connection()
            self.logger.info(msg)
            raise SourceError(e.args[0])

        except Exception as e:
            msg = str(e)
            self.session.rollback()
            self.logger.info(msg)
            raise SourceError(msg)

    @step("[Source] tinsert ...", 3)
    def insert(self, _model, _refresh_model=None, _commit=None):
        self.logger.info(f'Inserting in table: {_model.__tablename__}')
        self.set_engine()

        try:
            self.session.add(_model)
            self.session.flush()
            self.logger.info('Success: record has been added to db')

        except IntegrityError as e:
            self.close_connection()
            msg = str(e)
            self.logger.error(msg)
            if 'Duplicate' in msg:
                msg = 'Duplicate'
                raise DuplicateRecordError(msg)
            raise SourceError(msg)

        except StatementError as e:
            self.close_connection()
            self.session.rollback()
            msg = str(e)
            self.logger.error(msg)
            if 'Duplicate' in msg:
                raise DuplicateRecordError(msg)
            raise SourceError(e.args[0])

        except Exception as e:
            self.close_connection()
            msg = str(e)
            self.logger.error(msg)
            raise SourceError(msg)

        else:
            if _commit:
                self.session.commit()
            if _refresh_model:
                self.session.commit()
                self.session.refresh(_model)
                return _model
            return True

    @step("[Source] update ...", 3)
    def update(self, _model):
        self.logger.info(f'Updating in table: {_model.__table__}')
        self.set_engine()

        if _model not in self.session:
            msg = "The model has not an active session."
            
            raise SourceError(msg)

        try:
            self.session.commit()
            self.logger.info('Record updated succesfully.')

        except IntegrityError as e:
            self.session.rollback()
            msg = e._message()
            self.logger.info(msg)
            raise SourceError(msg)

        except StatementError as e:
            self.close_connection()
            self.session.rollback()
            msg = str(e)
            self.logger.error(msg)
            # raise DuplicateRecordError(msg)
            raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            msg = str(e)
            self.logger.error(msg)
            raise SourceError(msg)

        else:
            self.session.commit()
            return True

    @step("[SOURCE] __get_query_object ...", 3)
    def __get_query_object(self, _model_name, _join_models, _join_type):
        if _join_models is None:
            query = self.session.query(_model_name)
            return query

        recover_models = _join_models.copy()
        recover_models.insert(0, _model_name)

        query = self.session.query(*recover_models)
        for entity in _join_models:
            query = getattr(query, _join_type.value)(entity)

        return query

    @step("[SOURCE] __set_filters ...", 3)
    def __set_filters(self, _model_name, _query, _filters, _custom_filters=None):
        if _custom_filters:
            for filter in _custom_filters:
                _query = _query.filter(filter)

        if bool(_filters):
            for key in _filters.keys():
                _query = _query.filter(getattr(_model_name, key) == _filters[key])

        return _query

    @step("[SOURCE] get_count ...", 3)
    def get_count(
        self,
        _model,
        _join_models=None,
        _join_type=JoinType.JOIN,
        _custom_filters=None
    ):
        self.set_engine()

        try:
            model_name = _model.__class__
            query = self.__get_query_object(model_name, _join_models, _join_type)

            query = self.__set_filters(
                model_name,
                query,
                _model.get_dict(_nulls=False),
                _custom_filters
            )

            rows = query.count()
            self.logger.info(f"Total num of rows: {rows}")

            return rows

        except StatementError as e:
            raise SourceError(e.args[0])

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _source="get_count"
            )

    @step("[SOURCE] select_many_with_joins ...", 3)
    def select_many_with_joins(
        self,
        _model,
        _join_models=None,
        _join_type=JoinType.JOIN,
        _custom_filters=None,
        _order_column=None,
        _arrange="asc",
        _limit=10,
        _page=1
    ):
        self.set_engine()

        try:
            model_name = _model.__class__
            query = self.__get_query_object(model_name, _join_models, _join_type)

            query = self.__set_filters(
                model_name,
                query,
                _model.get_dict(_nulls=False),
                _custom_filters
            )

            if _page:
                page = self.__get_page(query, _limit, _order_column, _arrange, _page)

                records = page.items
                next_page = page.next_page

                self.logger.info(f"Qty pages: {page.pages}")
                self.logger.info(f"Next page: {page.next_page}")

            else:
                records = query.all()
                next_page = None

        except StatementError as e:
            raise SourceError(e.args[0])

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _source=f"select_many_with_joins _model:{_model}-{type(_model)}, _limit:{_limit}-{type(_limit)}, _page:{_page}-{type(_page)}"
            )

        qty_records = len(records)
        self.logger.info(f"Qty of records found: {qty_records}")
        if qty_records == 0:
            msg = 'No records found'
            raise NoRecordsFoundError(
                _message=msg,
                _error=msg,
                _source="select_many_with_joins"
            )

        return records, next_page

    @step("[SOURCE] __get_page ...", 3)
    def __get_page(self, _query, _limit, _order_column, _arrange, _page):
        self.records_per_page = int(_limit)
        page = int(_page)

        page_obj = None

        if _order_column:
            if _arrange == "ASC":
                page_obj = paginate(
                    _query.order_by(asc(_order_column)),
                    page,
                    self.records_per_page
                )
            else:
                page_obj = paginate(
                    _query.order_by(desc(_order_column)),
                    page,
                    self.records_per_page
                )

        else:
            page_obj = paginate(
                _query,
                page,
                self.records_per_page
            )

        return page_obj

    @step("[SOURCE] count_many_with_joins ...", 3)
    def count_many_with_joins(
        self,
        _model,
        _join_models=None,
        _join_type=JoinType.JOIN,
        _custom_filters=None
    ):
        self.set_engine()

        try:
            model_name = _model.__class__
            query = self.__get_query_object(model_name, _join_models, _join_type)

            query = self.__set_filters(
                model_name,
                query,
                _model.get_dict(_nulls=False),
                _custom_filters
            )

            records = query.count()

        except StatementError as e:
            raise SourceError(e.args[0])

        except Exception as e:
            raise SourceError(
                _message=str(e),
                _source="count_many_with_joins"
            )

        return records

    @step("[Source] delete ...", 3)
    def delete(self, _model):
        self.set_engine()

        try:
            filters = _model.get_dict(_nulls=False)

            if bool(filters) is False:
                raise SourceError("No value was specified in any attribute.")

            query = self.session.query(_model.__class__)
            for key in filters.keys():
                query = query.filter(
                    getattr(_model.__class__, key) == filters[key]
                )
            query.delete()
            self.logger.info('Record deleted succesfully.')

        except IntegrityError as e:
            self.session.rollback()
            msg = e._message()
            self.logger.error(msg)
            raise SourceError(msg)

        except StatementError as e:
            self.logger.error(e._message())
            raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            msg = str(e)
            self.logger.error(msg)
            raise SourceError(msg)

        else:
            self.session.commit()
            return True

    @step("[Source] select_many_by_query_sql ...", 3)
    def select_many_by_query_sql(self, _model, _query):
        self.set_engine()

        if _query is None:
            raise SourceError("_query param is None")

        filters = _model.get_dict(_nulls=False)

        try:
            query = self.session.execute(_query, filters)
            records = query.fetchall()

        except StatementError as e:
            self.close_connection()
            raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            raise SourceError(str(e))

        qty_records = len(records)

        if qty_records == 0:
            raise NoRecordsFoundError('Records not found')

        record_list = []
        for record in records:
            index = 0
            model_item = copy.deepcopy(_model)
            for column_name in query.keys():
                setattr(model_item, column_name, record[index])
                index += 1
            record_list.append(model_item)

        self.logger.info(f'{qty_records} Records found')

        return record_list

    @step("[Source] select_by_querysql ...", 3)
    def select_by_querysql(self, _query):
        self.set_engine()

        if _query is None:
            raise SourceError("_query param is None")

        try:
            filters = None
            query = self.session.execute(_query, filters)
            records = query.fetchall()

        except StatementError as e:
            self.close_connection()
            raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            raise SourceError(str(e))

        qty_records = len(records)

        if qty_records == 0:
            raise NoRecordsFoundError('Records not found')

        record_list = []
        for record in records:
            diccionario = dict(zip(query.keys(), record.values()))
            record_list.append(diccionario)    
            
        self.logger.info(f'{qty_records} Records found')

        return record_list

    @step("[Source] execute_query ...", 3)
    def execute_query(self, _sql_query):
        try:
            self.set_engine()
            
            self.session.execute(_sql_query)
            self.session.commit()
            return True
        
        except StatementError as e:
            self.close_connection()
            raise SourceError(e.args[0])

        except Exception as e:
            self.session.rollback()
            raise SourceError(str(e))