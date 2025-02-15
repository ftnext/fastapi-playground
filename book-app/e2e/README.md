# Instructions

## Setup

### e2e environment

```sh
$ python3.12 -m venv .venv --upgrade-deps
$ .venv/bin/python -m pip install -r requirements.txt
```

### sut

In other terminal

```sh
$ git clone git@github.com:iktakahiro/dddpy.git
$ make sync  # Needs Rye
$ make dev
```

## Run E2E

In e2e environment terminal

```sh
$ source .venv/bin/activate
(.venv) $ gauge run specs
```
