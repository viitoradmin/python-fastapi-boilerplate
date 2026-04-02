import os

import click
import uvicorn

from apps.server import create_app, create_socket_app
from config.env_config import load_dotenv
from core.utils import constant_variable
from config import LoggingConfig


load_dotenv()

# Combined ASGI app: Socket.IO at SOCKETIO_PATH, all other routes to FastAPI
app = create_socket_app(create_app())


@click.command()
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
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="asgi:app",
        host=str(os.environ.get("SERVER_HOST", "localhost")),
        port=int(os.environ.get("SERVER_PORT", 8000)),
        reload=bool(os.environ.get("SERVER_DEBUG", constant_variable.STATUS_FALSE)),
        workers=1,
        log_config=LoggingConfig().get_config(),
    )


if __name__ == "__main__":
    main()
