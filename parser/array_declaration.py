from typing import Any, override
from interpreter.context import Context
from parser.array_datatype import ArrayDatatype
from parser.array_element import ArrayElement
from parser.expressible import Expressible

class Array:
    def __init__(self, elements: list, datatype: ArrayDatatype):
        self.elements: list[Any] = elements
        self.datatype = datatype 

    def __str__(self) -> str:
        return f'{self.datatype} @ {self.format_array(self.elements)}'

    def format_array(self, element):
        if isinstance(element, list):
            return '[' + ', '.join(self.format_array(item) for item in element) + ']'
        elif hasattr(element, '__str__'):
            return str(element)
        else:
            return repr(element)