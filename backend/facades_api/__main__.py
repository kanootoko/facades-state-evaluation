# pylint: disable=too-many-arguments, no-value-for-parameter
"""
Facades evaluation backend service startup module
"""
import itertools
import os
import sys
import traceback
import typing as tp

import click
import uvicorn
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from facades_api import __version__
from facades_api.config import AppSettings
from facades_api.config.app_settings_global import app_settings
from facades_api.db.connection.session import SessionManager
from facades_api.endpoints import list_of_routes
from facades_api.utils.exceptions import FacadesApiError

LAST_UPDATE = "2022-12-28"


def bind_routes(application: FastAPI, prefix: str) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=(prefix if "/" not in {r.path for r in route.routes} else ""))


def get_app(prefix: str = "/api") -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "API for manipulations on user data on the facades state evaluation application"

    application = FastAPI(
        title="Facades evaluation service",
        description=description,
        docs_url="/docs",
        openapi_url="/openapi",
        version=f"{__version__} ({LAST_UPDATE})",
    )
    bind_routes(application, prefix)

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = get_app()


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Function that handles exceptions to become http response code 500 - Internal Server Error

    If debug is activated in app configuration, then stack trace is returned, otherwise only a generic error message.
    Message is sent to logger error stream anyway.
    """
    if isinstance(exc, FacadesApiError):
        return await http_exception_handler(request, exc.get_http_exception(exc))
    logger.opt(colors=True).error(
        "<cyan>{} {}</cyan> - '<red>{}</red>': {!r}",
        (f"{request.client.host}:{request.client.port}" if request.client is not None else "<unknown user>"),
        request.method,
        exc,
        exc,
    )
    logger.debug("{!r} Traceback:\n{}", exc, "".join(traceback.format_tb(exc.__traceback__)))
    if app_settings.debug:
        return JSONResponse(
            {
                "error": str(exc),
                "error_type": str(type(exc)),
                "path": request.url.path,
                "params": request.url.query,
                "trace": list(
                    itertools.chain.from_iterable(map(lambda x: x.split("\n"), traceback.format_tb(exc.__traceback__)))
                ),
            },
            status_code=500,
        )
    return JSONResponse({"code": 500, "message": "exception occured"}, status_code=500)


@app.on_event("startup")
async def startup_event():
    """
    Function that runs on an application startup. Database connection pool is initialized here.
    """
    await SessionManager().refresh()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Function that runs on an application shutdown. Database connection pool is destructed here.
    """
    await SessionManager().shutdown()


LogLevel = tp.Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR"]


def logger_from_str(logger_text: str) -> list[tuple[LogLevel, str]]:
    """
    Helper function to deconstruct string input argument(s) to logger configuration.

    Examples:
        logger_from_str("ERROR,errors.log") -> [("ERROR", "errors.log)]
        logger_from_str("ERROR,errors.log;INFO,info.log") -> [("ERROR", "errors.log), ("INFO", "info.log")]
    """
    res = []
    for item in logger_text.split(";"):
        assert "," in item, f'logger text must be in format "LEVEL,filename" - current value is {logger_text}'
        level, filename = item.split(",", 1)
        level = level.upper()
        res.append((level, filename))  # type: ignore
    return res


@click.command("Run facades evaluation backend service")
@click.option(
    "--db_addr",
    "-H",
    envvar="DB_ADDR",
    default="localhost",
    show_default=True,
    show_envvar=True,
    help="Postgres DBMS address",
)
@click.option(
    "--db_port",
    "-P",
    envvar="DB_PORT",
    type=int,
    default=5432,
    show_default=True,
    show_envvar=True,
    help="Postgres DBMS port",
)
@click.option(
    "--db_name",
    "-D",
    envvar="DB_NAME",
    default="facades_db",
    show_default=True,
    show_envvar=True,
    help="Postgres database name",
)
@click.option(
    "--db_user",
    "-U",
    envvar="DB_USER",
    default="postgres",
    show_default=True,
    show_envvar=True,
    help="Postgres database user",
)
@click.option(
    "--db_pass",
    "-W",
    envvar="DB_PASS",
    default="postgres",
    show_default=True,
    show_envvar=True,
    help="Postgres user password",
)
@click.option(
    "--db_pool_size",
    "-s",
    envvar="DB_POOL_SIZE",
    type=int,
    default=15,
    show_default=True,
    show_envvar=True,
    help="asyncpg database pool maximum size",
)
@click.option(
    "--logger_verbosity",
    "-v",
    type=click.Choice(("TRACE", "DEBUG", "INFO", "WARNING", "ERROR")),
    envvar="LOGGER_VERBOSITY",
    default="DEBUG",
    show_default=True,
    show_envvar=True,
    help="Logger verbosity",
)
@click.option(
    "--add_logger",
    "-l",
    "additional_loggers",
    type=logger_from_str,
    envvar="ADDITIONAL_LOGGERS",
    multiple=True,
    default=[],
    show_default="[]",
    show_envvar=True,
    help="Add logger in format LEVEL,path/to/logfile",
)
@click.option(
    "--port",
    "-p",
    envvar="PORT",
    type=int,
    default=8080,
    show_default=True,
    show_envvar=True,
    help="Service port number",
)
@click.option(
    "--host",
    envvar="HOST",
    default="0.0.0.0",
    show_default=True,
    show_envvar=True,
    help="Service HOST address (0.0.0.0 to accept requests from everywhere)",
)
@click.option(
    "--debug",
    envvar="DEBUG",
    is_flag=True,
    help="Enable debug mode (auto-reload on change, traceback returned to user, etc.)",
)
def main(
    db_addr: str,
    db_port: int,
    db_name: str,
    db_user: str,
    db_pass: str,
    db_pool_size: int,
    port: int,
    host: str,
    logger_verbosity: LogLevel,
    additional_loggers: list[tuple[LogLevel, str]],
    debug: bool,
):
    """
    Facades evaluation backend service main function, performs configuration
        via command line parameters and environment variables.
    """
    additional_loggers = list(itertools.chain.from_iterable(additional_loggers))
    settings = AppSettings(
        host=host,
        port=port,
        db_addr=db_addr,
        db_port=db_port,
        db_name=db_name,
        db_user=db_user,
        db_pass=db_pass,
        db_pool_size=db_pool_size,
        debug=debug,
    )
    app_settings.update(settings)
    if logger_verbosity != "DEBUG":
        logger.remove()
        logger.add(sys.stderr, level=logger_verbosity)
    for log_level, filename in additional_loggers:
        logger.add(filename, level=log_level)
    if debug:
        uvicorn.run(
            "facades_api.__main__:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=["facades_api"],
            log_level=logger_verbosity.lower(),
        )
    else:
        uvicorn.run("facades_api.__main__:app", host=host, port=port, log_level=logger_verbosity.lower())


if __name__ == "__main__":
    if os.path.isfile(".env"):
        with open(".env", "rt", encoding="utf-8") as f:
            for name, value in (
                tuple((line[len("export ") :] if line.startswith("export ") else line).strip().split("="))
                for line in f.readlines()
                if not line.startswith("#") and line != ""
            ):
                if name not in os.environ:
                    os.environ[name] = value
    main()
