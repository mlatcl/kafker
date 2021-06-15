# Kafker

A tiny Kafka-driven text publishing social network service.

## Getting Started
To run Kafker on your local machine, you will need

* A Kafka server listening on `localhost:9092`
* A reasonably new Python3 environment with `poetry` installed

### Kafka
For local usage, the repository contains a `docker-compose`-configuration which is an almost identical copy of an [example configuration](https://github.com/cloudhut/kowl/tree/master/docs/local) provided by the [Kowl](https://github.com/cloudhut/kowl) project.
Kowl is an easy to use webinterface for Kafka and very helpful to understand what's going on under the hood.

To run Kafka on your local machine, ensure that you have a working docker configuration and run
```shell
$ cd docker
$ docker-compose up
```
The compose file will expose kafka and the kowl webinterface on your local machine, reachable at [`http://localhost:8080`](http://localhost:8080).
You can easily delete the entire kafka state (that is, all messages and topics) by stopping the docker containers and deleting the `zk-single-kafka-single` folder.

### Installing Kafker
This repository uses [Python Poetry](https://python-poetry.org/) for dependency management. After cloning the repository, run
```shell
$ poetry install
```
to setup a development environment.
You can now run commands in the environment via `poetry run <stuff>` (such as `poetry run python -m kafker`) or spawn a shell which configures the environment automatically by running
```shell
$ poetry shell
```
The commands below assume that you are inside such a shell.

### Running Kafker
Kafker is a [Faust application](https://faust.readthedocs.io/en/latest/index.html).
To initialize and run Kafker, start at least one worker after ensuring that your Kafka server is reachable.
```shell
$ python -m kafker worker -l info
```
See the [Faust documentation](https://faust.readthedocs.io/en/latest/playbooks/quickstart.html#quickstart) for a few more details on how to run a Faust application. Note that using the `faust` executable is also possible: `faust -A kafker.app worker -l info`.

### Using Kafker
Kafker exposes a number of REST-APIs and CLIs.
They can be found in the `views.py` and `commands.py` modules respectively, so take a look at the code for all the details.
The commands can be discovered through the Faust CLI:
```shell
$ python -m kafker --help
```
For example, you can use
```shell
$ python -m kafker register -n markus
```
to register a new user or
```shell
$ python -m kafker post -a markus -t "Why not Zoidberg?"
```
to create a new post.

Timelines, follow relationships and a few other things are exposed via REST APIs.
They can be reached at [`http://localhost:6066/`](http://localhost:6066/).
For example, you can inspect a user's timeline at [`http://localhost:6066/timeline/markus/`](http;://localhost:6066/timeline/markus/).

### Adding test data
There is a small script called `generate_data.sh` that can be used to add some trivial data to the system.
To add a corpus of data to the Markov Chain, you can use the `ingest-data`-command:
```shell
$ python -m kafker ingest-data my-text.txt
```
The format is quite lenient, I recommend using files that contain lines of text with short-ish lines and not too many funky special characters.

You could, for example, use data from the [Trump tweet archive](https://www.thetrumparchive.com/) (see the FAQ) - or some [speech corpus](https://github.com/unendin/Trump_Campaign_Corpus) - to initialize the chain. Something like this for preprocessing:
```shell
$ jq '.[].text' trump_tweets.json | sed "s/\\n/ /g" | sed "s/ +/ /g" | tr -d "\"" > trump_tweets.txt
```
You could now either ingest the data:
```shell
$ python -m kafker ingest-text trump_tweets.txt
```
Or add some posts to the system:
```shell
$ python -m kafker register -n trump
$ shuf -n 23 trump_tweets.txt | tr "\n" "\0" | xargs -0 -P 10 -IX python -m kafker post -a trump -t X
```

## Developing
This repo uses [black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/) for code formatting and [pylint](https://pylint.org/) for linting.
To easily ensure that code changes conform to the style requirements, you can use `pre-commit` to automatically run checks before every commit.
You need to install the hooks from within a poetry shell and commit from within a poetry shell as well:
```shell
$ pre-commit install
```
You can manually run the checks on all changed files
```shell
$ pre-commit run
```
or on all files
```shell
$ pre-commit run -a
```
Your editor can probably be configured to at least run isort and black in regular intervals.
