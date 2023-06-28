# bien

Component based HTML rendering for HTTP servers.

You will need [PDM](https://pdm.fming.dev) and [just](https://just.systems) for development.

```bash
# Create a virtual environment, install all dependencies
# and configure the Python interpreter to collect coverage
# from called subprocesses:
just bootstrap

# Run ruff, mypy and pytest:
just

# See available recipes:
just help
```

## Usage

### Simple example

```python
import bien

link = bien.HTMLElement(
    name="a",
    attributes={"href": "https://example.com"},
    children=[bien.Text("Example")]
)

print(link.render())
# <a href="https://example.com">Example</a>
```

### Meta tags

```python
import bien

meta = bien.HTMLElement(
    name="meta",
    attributes={"encoding": "utf-8"},
    single_tag=True,
)

print(meta.render())
# <meta encoding="utf-8" />
```

### FastAPI with HTMX

```python
import datetime

import bien
import fastapi
import fastapi.responses


def view_server_time() -> bien.Element:
    return bien.HTMLElement("p", attributes={"id": "time"}, children=[
        bien.Text(datetime.datetime.now().isoformat())])


def view_page() -> bien.Element:
    return bien.HTMLElement("html", children=[
        bien.HTMLElement("body", children=[
            view_server_time(),
            bien.HTMLElement(
                name="button",
                attributes={
                    "hx-get": "/time",
                    "hx-target": "#time",
                    "hx-swap": "outerHTML",
                    "hx-trigger": "click",
                },
                children=[bien.Text("Get server time")]),
            bien.HTMLElement(
                name="script",
                attributes={"src": "https://unpkg.com/htmx.org"})])])


app = fastapi.FastAPI()


@app.get("/")
def root():
    return fastapi.responses.HTMLResponse(content=view_page().render())


@app.get("/time")
def time():
    return fastapi.responses.HTMLResponse(content=view_server_time().render())
```
