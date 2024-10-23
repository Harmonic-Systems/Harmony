# Harmony

[![Flow](./flow.png)](./flow.png)

To a python script or a jupyter notebook with the corresponding [autogen](https://github.com/microsoft/autogen/) agents and chats.

## Features

- Export .harmony flows to .py or .ipynb
- Run a .harmony flow
- Include a `logs` folder with the logs of the flow in csv format
- Provide a custom [IOSStream](https://autogen-ai.github.io/autogen/docs/reference/io/base#iostream) to handle input and output.

## Installation

<!-- 
On PyPI:

```bash
python -m pip install harmony
``` -->

From this repository:

```bash
python -m pip install git+https://github.com/harmony/py.git
```

## Usage

### CLI

```bash
# Export a Harmony flow to a python script or a jupyter notebook
harmony --export /path/to/a/flow.harmony --output /path/to/an/output[.py|.ipynb]
# Export and run the script, optionally force generation if the output file already exists
harmony /path/to/a/flow.harmony --output /path/to/an/output[.py] [--force]
```

### As a library

#### Export a flow

```python
# Export a Harmony flow to a python script or a jupyter notebook
from harmony import HarmonyExporter
flow_path = "/path/to/a/flow.harmony"
output_path = "/path/to/an/output.py"  # or .ipynb
exporter = HarmonyExporter.load(flow_path)
exporter.export(output_path)
```
  
#### Run a flow

```python
# Run a flow
from harmony import HarmonyRunner
flow_path = "/path/to/a/flow.harmony"
output_path = "/path/to/an/output.py"
runner = HarmonyRunner.load(flow_path)
runner.run(output_path=output_path)
```

#### Run a flow with a custom IOStream

```python
# Run the flow with a custom IOStream
from harmony import HarmonyIOStream, HarmonyRunner

flow_path = "/path/to/a/flow.harmony"
output_path = "/path/to/an/output.py"

def print_function(*values, **args) -> None:
    """A custom print function."""
    print(values)

def on_prompt_input(prompt: str) -> str:
    """A custom input function."""
    return input(prompt)

io_stream = HarmonyIOStream(
    print_function=print_function,
    on_prompt_input=on_prompt_input,
    input_timeout=30,
)
with HarmonyIOStream.set_default(io_stream):
    runner = HarmonyRunner.load(flow_path)
    runner.run(stream=io_stream, output_path=output_path)

io_stream.close()

```

### Tools

- [autogen](https://github.com/microsoft/autogen/)
- [juptytext](https://github.com/mwouts/jupytext)
- [twisted](https://github.com/twisted/twisted)
- [pydantic](https://github.com/pydantic/pydantic)
