from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Foo(_message.Message):
    __slots__ = ["bars", "baz", "mapping"]
    class MappingEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    BARS_FIELD_NUMBER: _ClassVar[int]
    BAZ_FIELD_NUMBER: _ClassVar[int]
    MAPPING_FIELD_NUMBER: _ClassVar[int]
    bars: _containers.RepeatedCompositeFieldContainer[Bar]
    baz: Baz
    mapping: _containers.ScalarMap[int, str]
    def __init__(self, bars: _Optional[_Iterable[_Union[Bar, _Mapping]]] = ..., baz: _Optional[_Union[Baz, _Mapping]] = ..., mapping: _Optional[_Mapping[int, str]] = ...) -> None: ...

class Bar(_message.Message):
    __slots__ = ["short_id", "long_id", "name", "description", "size", "progress", "precision", "checked", "notes"]
    SHORT_ID_FIELD_NUMBER: _ClassVar[int]
    LONG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    CHECKED_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    short_id: int
    long_id: int
    name: str
    description: str
    size: int
    progress: float
    precision: float
    checked: bool
    notes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, short_id: _Optional[int] = ..., long_id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., size: _Optional[int] = ..., progress: _Optional[float] = ..., precision: _Optional[float] = ..., checked: bool = ..., notes: _Optional[_Iterable[str]] = ...) -> None: ...

class Baz(_message.Message):
    __slots__ = ["status"]
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_UNSPECIFITED: _ClassVar[Baz.Status]
        OK: _ClassVar[Baz.Status]
        ERROR: _ClassVar[Baz.Status]
    STATUS_UNSPECIFITED: Baz.Status
    OK: Baz.Status
    ERROR: Baz.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Baz.Status
    def __init__(self, status: _Optional[_Union[Baz.Status, str]] = ...) -> None: ...
