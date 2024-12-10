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

    #def set_element(self, context: Context, array_element: ArrayElement, value: Any, element = None, depth: int = 0) -> None:
        #if element == None:
            #element = self.elements
        #i: int = context.evaluate(context, array_element.indices[depth])
        #if depth < len(array_element.indices):
            #self.set_element(context, array_element, value, element[i], depth + 1)
        #else:
            #if isinstance(value, Array):
                #element = value.elements
            #elif isinstance(value, Expressible):
                #element = context.evaluate(context, value)