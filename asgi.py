import os
from pathlib import Path

import click
import uvicorn
from app.api.server import app


def load_env_file(env: str) -> None:
    """
    Load environment variables from .env file based on env parameter.
    
    Args:
        env: Environment name (local, dev, prod)
    """
    env_file = Path(f"{env}.env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value


@click.command("run_server", help="Run the server")
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)


def main(env: str, debug: bool) -> None:
    """
    Main function to run the FastAPI server.
    
    Args:
        env: Environment name (local, dev, prod)
        debug: Enable debug mode
    """
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    
    load_env_file(env=env)
    
    host = str(os.environ.get("SERVER_HOST", "localhost"))
    port = int(os.environ.get("SERVER_PORT", 8008))
    
    # Reload should be True for local/dev, False for prod
    # Workers can only be used when reload is False
    use_reload = env in ["local", "dev"] or debug
    workers = None if use_reload else os.cpu_count()
    
    # When reload is enabled, uvicorn requires app as import string
    # When reload is disabled, we can pass the app object directly
    app_reference = "app.api.server:app" if use_reload else app
    
    uvicorn.run(
        app=app_reference,
        host=host,
        port=port,
        reload=use_reload,
        workers=workers,
    )


if __name__ == "__main__":
    main()
