from sqlalchemy.types import TypeDecorator, JSON
from pydantic import BaseModel


class ModelJsonMapper(TypeDecorator):
    impl = JSON

    def __init__(self, model_class: BaseModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class

    def process_bind_param(self, value: BaseModel, dialect):
        if value is not None:
            return value.model_dump_json()

    def process_result_value(self, value: JSON, dialect):
        if value is not None:
            return self.model_class.model_validate_json(value)
