from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin, SQLAlchemyAsyncConfig

from app.models.user import Base
from app.routes.user import user_routes
import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in .env file")

db_config = SQLAlchemyAsyncConfig(connection_string=database_url)#os.environ["DATABASE_URL"])
sqlalchemy_plugin = SQLAlchemyPlugin(config=db_config)

openapi_config = OpenAPIConfig(
    title="My Litestar API",
    version="1.0.0",
    description="API with Swagger documentation",
)


async def init_db():
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = Litestar(
    route_handlers=[user_routes],
    plugins=[sqlalchemy_plugin],
    openapi_config=openapi_config,
    on_startup=[init_db],
)

