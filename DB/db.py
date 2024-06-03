import tortoise
import os
from dotenv import load_dotenv

load_dotenv()


async def db_init():
    # Here we connect to DB.
    # also specify the app name of "models"
    # which contain models from "DB.models"
    await tortoise.Tortoise.init(
        db_url=os.getenv("DB_URL"),
        modules={'models': ['DB.models']}
    )
    # # Generate the schema
    await tortoise.Tortoise.generate_schemas()
