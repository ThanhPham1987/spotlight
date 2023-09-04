from datetime import datetime
from typing import Any, Dict, List, Optional, Union
import numpy as np


from renumics.spotlight.dtypes import (
    Audio,
    Category,
    Embedding,
    Image,
    Mesh,
    Sequence1D,
    Video,
    Window,
)


class DType:
    _name: str

    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._name


class CategoryDType(DType):
    _categories: Optional[Dict[str, int]]

    def __init__(self, categories: Optional[Union[List[str], Dict[str, int]]] = None):
        super().__init__("Category")
        if isinstance(categories, list):
            self._categories = {
                category: code for code, category in enumerate(categories)
            }
        else:
            self._categories = categories

    @property
    def categories(self) -> Optional[Dict[str, int]]:
        return self._categories


class Sequence1DDType(DType):
    x_label: str
    y_label: str

    def __init__(self, x_label: str = "x", y_label: str = "y"):
        super().__init__("Sequence1D")
        self.x_label = x_label
        self.y_label = y_label


ALIASES: Dict[Any, DType] = {}


def register_dtype(dtype: DType, aliases: list) -> None:
    for alias in aliases:
        assert dtype.name.lower() not in ALIASES
        ALIASES[dtype.name.lower()] = dtype
        assert alias not in ALIASES
        ALIASES[alias] = dtype


bool_dtype = DType("bool")
register_dtype(bool_dtype, [bool])
int_dtype = DType("int")
register_dtype(int_dtype, [int])
float_dtype = DType("float")
register_dtype(float_dtype, [float])
bytes_dtype = DType("bytes")
register_dtype(bytes_dtype, [bytes])
str_dtype = DType("str")
register_dtype(str_dtype, [str])
datetime_dtype = DType("datetime")
register_dtype(datetime_dtype, [datetime])
category_dtype = CategoryDType()
register_dtype(category_dtype, [Category])
window_dtype = DType("Window")
register_dtype(window_dtype, [Window])
embedding_dtype = DType("Embedding")
register_dtype(embedding_dtype, [Embedding])
array_dtype = DType("array")
register_dtype(array_dtype, [np.ndarray])
image_dtype = DType("Image")
register_dtype(image_dtype, [Image])
audio_dtype = DType("Audio")
register_dtype(audio_dtype, [Audio])
mesh_dtype = DType("Mesh")
register_dtype(mesh_dtype, [Mesh])
sequence_1d_dtype = Sequence1DDType()
register_dtype(sequence_1d_dtype, [Sequence1D])
video_dtype = DType("Video")
register_dtype(video_dtype, [Video])
mixed_dtype = DType("mixed")


DTypeMap = Dict[str, DType]


def create_dtype(x: Any) -> DType:
    if isinstance(x, DType):
        return x
    if isinstance(x, str):
        return ALIASES[x.lower()]
    return ALIASES[x]
