# Harmony

Translate a Harmony flow:

<img fetchpriority="high" alt="Harmony flow" src="static/images/overview.webp#only-light" />
<img fetchpriority="high" alt="Harmony flow" src="static/images/overview_dark.webp#only-dark" />

To a python script or a jupyter notebook with the corresponding [ag2](https://github.com/ag2ai/ag2/) agents and chats.

## Features

- Convert .harmony flows to .py or .ipynb
- Run a .harmony flow
- Store the runtime logs of a flow to csv for further analysis

## Installation

On PyPI:

```bash
python -m pip install harmony
```

From the repository:

```bash
python -m pip install git+https://github.com/harmony/harmony.git
```

!!! note
    `autogen-agentchat` package conflicts with `ag2` / `pyautogen`. Ensure that `autogen-agentchat` is uninstalled before installing `harmony`. If you have already installed `autogen-agentchat`, you can uninstall it with the following command:

    ```shell
    pip uninstall autogen-agentchat -y
    ```

    If already installed harmony you might need to reinstall it after uninstalling `autogen-agentchat`:
    
      ```shell
      pip install --force --no-cache harmony pyautogen
      ```

## Usage

### CLI

```bash
# Convert a Harmony flow to a python script or a jupyter notebook
harmony convert --file /path/to/a/flow.harmony --output /path/to/an/output/flow[.py|.ipynb]
# Convert and run the script, optionally force generation if the output file already exists
harmony run --file /path/to/a/flow.harmony --output /path/to/an/output/flow[.py] [--force]
```

### Using docker/podman

```shell
CONTAINER_COMMAND=docker # or podman
# pull the image
$CONTAINER_COMMAND pull harmony/harmony
# Convert a Harmony flow to a python script or a jupyter notebook
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.harmony:/flow.harmony \
  -v /path/to/an/output:/output \
  harmony/harmony convert --file /flow.harmony --output /output/flow[.py|.ipynb] [--force]

# with selinux and/or podman, you might get permission (or file not found) errors, so you can try:
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.harmony:/flow.harmony \
  -v /path/to/an/output:/output \
  --userns=keep-id \
  --security-opt label=disable \
  harmony/harmony convert --file /flow.harmony --output /output/flow[.py|.ipynb] [--force]
```

```shell
# Convert and run the script
$CONTAINER_COMMAND run \
  --rm \
  -v /path/to/a/flow.harmony:/flow.harmony \
  -v /path/to/an/output:/output \
  harmony/harmony run --file /flow.harmony --output /output/output[.py]
```

### UI

For creating-only (no exporting or running) harmony flows, you can use the playground at <https://harmony.github.io>.  
The repo for the js library is [here](https://github.com/harmony/react).  
We are currently working on harmony-studio to provide a visual interface for creating and running Harmony flows (you can find more [here](https://github.com/harmony/studio)).  
Until then, you can use our [Jupyter](https://github.com/harmony/jupyter) or the [VSCode](https://github.com/harmony/vscode) extension to create and run Harmony flows.

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

### Tools

- [ag2 (formerly AutoGen)](https://github.com/ag2ai/ag2)
- [juptytext](https://github.com/mwouts/jupytext)
- [pydantic](https://github.com/pydantic/pydantic)
- [typer](https://github.com/fastapi/typer)
