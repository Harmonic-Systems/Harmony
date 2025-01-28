# Harmony

[![Follow](https://img.shields.io/badge/Follow_on_X-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/harmonicsystems)

## Make AI Agents Collaborate: Drag, Drop, and Orchestrate with Harmony

![Overview](docs/static/images/overview.webp)

```mermaid
%%{init: {'sequence': {'actorSpacing': 10, 'width': 150}}}%%
sequenceDiagram
    participant customer_engagement_agent as User
    participant customer_proxy as User Proxy
    participant topic_preference_agent as Topic Preference Agent
    participant personal_information_agent as Personal Information Agent
    personal_information_agent->>customer_proxy: Hello, I'm here to help you get started with our account. Could you tell me your name and location?
    customer_proxy->>personal_information_agent: 
    note over personal_information_agent: Content: Hi, I'm Stella from Athens
    topic_preference_agent->>customer_proxy: Great! Could you tell me what topics you are interested in reading about?<br/>Context: <br/>{'name':...
    customer_proxy->>topic_preference_agent: 
    note over topic_preference_agent: Content: Software agents
    customer_proxy->>customer_engagement_agent: Let's find something fun to read.<br/>Context: <br/>{'name': 'Stella', 'location': 'Athens'}<br/>{"t...
    customer_engagement_agent->>customer_proxy: Hey Stella from Athens! Did you know that software agents are like little digital helpers that can p...
```

## Installation

On PyPI:

```bash
python -m pip install harmony
```

## Usage

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

## License

This project is licensed under the [Apache License, Version 2.0 (Apache-2.0)](https://github.com/harmonic-systems/harmony/blob/main/LICENSE).
