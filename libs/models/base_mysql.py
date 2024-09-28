# Python's Libraries
from datetime import datetime
from decimal import Decimal
from datetime import date
import json

# sqlalchemy
from sqlalchemy.orm.collections import InstrumentedList


class MySQLModel(object):

    def backref_to_dic(self, _value, _signer=None):
        data = []
        for item in _value:
            item_dict = item.get_dict(
                _relations=False,
                _signer=_signer
            )
            data.append(item_dict)

        return data

    def get_dict(
        self,
        _nulls=True,
        _primaries=True,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):
        data = {}

        for attr, column in self.__mapper__.c.items():
            if _primaries is False and column.primary_key:
                continue

            column_value = getattr(self, attr)
            if _nulls is False and column_value is None:
                continue

            data[column.key] = column_value

        if _relations:
            for attr, relation in self.__mapper__.relationships.items():

                value = getattr(self, attr)

                if value is None and _nulls:
                    data[relation.key] = None
                    continue

                if relation.key in _except_rel:
                    continue

                if type(value) == InstrumentedList:
                    if _backref is False:
                        continue

                    if relation.key in _except_rel:
                        continue

                    if value:
                        data[relation.key] = self.backref_to_dic(
                            _value=value,
                            _signer=_signer
                        )

                    else:
                        data[relation.key] = value

                else:
                    data[relation.key] = value.get_dict(
                        _nulls=_nulls,
                        _primaries=_primaries,
                        _relations=_relations,
                        _backref=_backref,
                        _except_rel=_except_rel,
                        _signer=_signer
                    )

        return data

    def get_json(
        self,
        _relations=False,
        _backref=False,
        _except_rel=[],
        _signer=None
    ):

        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()

            if isinstance(x, Decimal):
                return str(x)

        return json.dumps(
            self.get_dict(
                _relations=_relations,
                _backref=_backref,
                _except_rel=_except_rel,
                _signer=_signer
            ),
            default=extended_encoder
        )


class MySQLModelCollection(list):

    def fill(self, _list):
        self.extend(_list)

    def extended_encoder(self, x):
        if isinstance(x, datetime):
            return x.isoformat()

        if isinstance(x, date):
            return x.isoformat()

    def get_json(self):
        data = []
        for item in self:
            data.append(item.get_dict())

        return json.dumps(data, default=self.extended_encoder)
