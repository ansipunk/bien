import pytest

import bien


def test_text():
    text = "3 < 2"

    unsafe = bien.Text(text)
    assert unsafe.render() == "3 &lt; 2"

    safe = bien.Text(text, True)
    assert safe.render() == text


def test_element():
    element = bien.Element()

    with pytest.raises(NotImplementedError):
        element.render()


def test_elements():
    first = "first"
    second = "second"

    elements = bien.Elements(bien.Text(first), bien.Text(second))
    assert elements.render() == first + second


def test_html_element():
    div = bien.HTMLElement(name="div")
    assert div.render() == "<div></div>"


def test_html_element_with_children():
    p = bien.HTMLElement(name="p", children=[bien.Text("Hello world!")])
    assert p.render() == "<p>Hello world!</p>"


def test_html_element_with_attributes():
    a = bien.HTMLElement(
        name="a",
        attributes={"href": "/favicon.ico", "download": None},
        children=[bien.Text("Download favicon")])
    assert a.render() == '<a href="/favicon.ico" download>Download favicon</a>'


def test_html_element_single_tag():
    meta = bien.HTMLElement(
        name="meta", attributes={"encoding": "utf-8"}, single_tag=True)
    assert meta.render() == '<meta encoding="utf-8" />'
