import abc
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, validator

from ...models import Category, CategoryType
from ...models import Label as LabelModel
from ...models import Project, Span, SpanType
from ...models import TextLabel as TL


class Label(BaseModel, abc.ABC):

    @abc.abstractmethod
    def has_name(self) -> bool:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def parse(cls, obj: Any):
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, project: Project) -> Optional[LabelModel]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_annotation(self, user, example, mapping):
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.dict()))


class CategoryLabel(Label):
    label: str

    @validator('label')
    def label_is_not_empty(cls, value: str):
        if value:
            return value
        else:
            raise ValueError('is not empty.')

    def has_name(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.label

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, str):
            return cls(label=obj)
        elif isinstance(obj, int):
            return cls(label=str(obj))
        else:
            raise TypeError(f'{obj} is not str.')

    def create(self, project: Project) -> Optional[LabelModel]:
        return CategoryType(text=self.label, project=project)

    def create_annotation(self, user, example, mapping: Dict[str, LabelModel]):
        return Category(
            user=user,
            example=example,
            label=mapping[self.label]
        )


class SpanLabel(Label):
    label: Union[str, int]
    start_offset: int
    end_offset: int

    def has_name(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self.label

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, list) or isinstance(obj, tuple):
            columns = ['start_offset', 'end_offset', 'label']
            obj = zip(columns, obj)
            return cls.parse_obj(obj)
        elif isinstance(obj, dict):
            return cls.parse_obj(obj)
        else:
            raise TypeError(f'{obj} is invalid type.')

    def create(self, project: Project) -> Optional[LabelModel]:
        return SpanType(text=self.label, project=project)

    def create_annotation(self, user, example, mapping: Dict[str, LabelModel]):
        return Span(
            user=user,
            example=example,
            start_offset=self.start_offset,
            end_offset=self.end_offset,
            label=mapping[self.label]
        )


class TextLabel(Label):
    text: str

    def has_name(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self.text

    @classmethod
    def parse(cls, obj: Any):
        if isinstance(obj, str) and obj:
            return cls(text=obj)
        else:
            raise TypeError(f'{obj} is not str or empty.')

    def create(self, project: Project) -> Optional[LabelModel]:
        return None

    def create_annotation(self, user, example, mapping):
        return TL(
            user=user,
            example=example,
            text=self.text
        )
