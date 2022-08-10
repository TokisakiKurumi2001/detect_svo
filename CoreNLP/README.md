# CoreNLP

**Step 1:** Make sure you have JDK installed

**Step 2:** Download and extract https://nlp.stanford.edu/software/stanford-corenlp-4.5.0.zip to this folder

**Step 3:** Start the server by running `python server.py start`

**Addition:**: To stop the server, follow the next steps:

```bash
chmod +x shutdown_server.sh # Run this only once
python server.py stop
```

## How to run the hard way (obviously correct way)

### `detect.py` file

To print the tree, please use TREE=True before `python detect.py`. For example,

- Print Tree

```bash
TREE=True python detect.py
```

- Not print tree

```bash
python detect.py
```

### `api.py` file

In this file, we add DEBUG_FLAG for printing debug statement and DEMO for demonstration

- To demo

```bash
DEMO=True python api.py
```

- To Debug

```bash
DEBUG_FLAG=True python api.py
```

### `massive_test.py` file

This call the `api.py`, `api.py` call `detect.py` so use the combination of the environment variable to get the best achievement
