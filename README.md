# Heroku-Alexa

## Development

Install the locked dependencies with uv:

```sh
uv sync --locked
```

Run the application locally:

```sh
uv run gunicorn main:app --log-file -
```

Dependencies are declared in `pyproject.toml` and resolved in `uv.lock`.

## AWS Lambda

The Lambda entry point is `main.lambda_handler`. Upload the project files and
the installed dependencies as a ZIP package, then configure these environment
variables:

- `AMBIDATA_READ_KEY`: AmbiData channel read key
- `AMBIDATA_CHANNEL_ID`: AmbiData channel ID (optional, defaults to `10905`)
- `ALEXA_SKILL_ID`: Alexa Skill ID (recommended)

For a ZIP deployment, install the locked dependencies into the package
directory and copy `main.py`, `templates.yaml`, and `lightVegiClass.csv` into
that directory. Set the Alexa endpoint type to **AWS Lambda ARN** and select
the Lambda function's ARN. The handler must be `main.lambda_handler`.

The Lambda deployment does not use the Flask `app`; the Flask entry point is
kept for local and Heroku-compatible execution.
