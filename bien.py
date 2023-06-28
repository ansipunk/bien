__version__ = "1.0.2"

from html import escape
from typing import Iterable, Mapping, Optional

Children = Iterable["Element"]
Attributes = Mapping[str, Optional[str]]


class Element:
    def render(self) -> str:
        raise NotImplementedError


class Elements(Element):
    elements: Iterable[Element]

    def __init__(self, *elements: Element) -> None:
        self.elements = elements

    def render(self) -> str:
        rendered = (element.render() for element in self.elements)
        return "".join(rendered)


class HTMLElement(Element):
    name: str
    attributes: Mapping[str, Optional[str]]
    children: Iterable[Element]
    single_tag: bool

    def __init__(
        self,
        name: str,
        attributes: Optional[Attributes] = None,
        children: Optional[Children] = None,
        single_tag: bool = False,
    ) -> None:
        self.name = name

        if attributes:
            self.attributes = attributes
        else:
            self.attributes = {}

        if children:
            self.children = children
        else:
            self.children = []

        self.single_tag = single_tag

    def render(self) -> str:
        rendered = "<" + self.name

        for key, value in self.attributes.items():
            key = escape(key)

            if value is None:
                rendered += f" {key}"
            else:
                rendered += f' {key}="{escape(value)}"'

        if self.single_tag:
            return rendered + " />"

        rendered += ">"

        for child in self.children:
            rendered += child.render()

        return rendered + f"</{self.name}>"


class Text(Element):
    content: str
    safe: bool

    def __init__(self, content: str, safe: bool = False) -> None:
        self.content = content
        self.safe = safe

    def render(self) -> str:
        if self.safe:
            return self.content

        return escape(self.content)


class HTML5Doctype(Element):
    def render(self) -> str:
        return "<!DOCTYPE html>"
