# filters
from libs.filters.filters_mysql_dao import FiltersDao

# sources
from libs.sources.mysql_source import JoinType

# utils
from libs.utils.decorators import step

# models
from models.menu_item_model import MenuItemModel
from models.menu_item_model import MenuItemCollection


class MenuItemDao(object):

    def __init__(self, _db=None) -> None:
        self.db = _db

    @step("[DAO] insert_menu_item_dao ...", 2)
    def insert_menu_item_dao(self, _model:MenuItemModel) -> MenuItemModel:
        model = self.db.insert(_model, True)
        return model
    
    @step("[DAO] get_menu_item_dao ...", 2)
    def get_menu_item_dao(self, _model:MenuItemModel) -> MenuItemModel:
        record = self.db.select_one(_model)
        return record
    
    @step("[DAO] delete_menu_item_dao ...", 2)
    def delete_menu_item_dao(self, _model:MenuItemModel):
        self.db.delete(_model)
        return True
    
    @step("[DAO] update_menu_item_dao ...", 2)
    def update_menu_item_dao(self, _model:MenuItemModel):
        self.db.update(_model)
        return True
    
    @step("[DAO] search_menu_items ...", 2)
    def search_menu_items(
        self,
        _model:MenuItemModel,
        _filters=None,
        _ordering=None,
        _sorting=None,
        _limit=None,
        _page=None
    ):
        filters = MenuItemFiltersDao(_model, _filters)
        filters.check_thatfiltersarenotnull()
        custom_filters = filters.build_filters()

        # others model 
        join_models = []
        join_type = JoinType.JOIN

        model_list, next_page = self.db.select_many_with_joins(
            _model,
            _join_models=join_models,
            _join_type=join_type,
            _custom_filters=custom_filters,
            _order_column=_ordering,
            _arrange=_sorting,
            _limit=_limit,
            _page=_page
        )

        collection = MenuItemCollection()
        collection.fill(model_list)

        count = self.db.count_many_with_joins(
            _model,
            _join_models=join_models,
            _join_type=join_type,
            _custom_filters=custom_filters
        )

        return collection, next_page, count


class MenuItemFiltersDao(FiltersDao):

    def build_filters(self):
        model_filters_list = self.get_modelfilterslist()

        custom_filters_list = []

        if self.filters_dto is None or len(self.filters_dto) == 0:
            return custom_filters_list

        for filter in self.filters_dto:
            custom_filters_list.append(
                self.get_filter(
                    self.model,
                    filter.field_name,
                    filter.operator,
                    filter.value
                )
            )

        filters_list = model_filters_list + custom_filters_list

        return filters_list