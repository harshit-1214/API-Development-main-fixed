from app.logger import setup_logging

setup_logging()

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import model
from app.database import  connect_database,async_engine
from app.routers import post, user, auth

logger = logging.getLogger(__name__)

# model.Base.metadata.create_all(bind = engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application starting")
    await connect_database()
    yield
    logger.info("application shutting down")
    await async_engine.dispose()

app = FastAPI(lifespan=lifespan,title="Post") 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
# @app.get("/check")
# async def make_tea(name):
#     print("kettle on")

# c = make_tea("A")
# print(c)  

# import time

# def make_tea(name):
#     print(f"{name}: kettle on")
#     time.sleep(2)                  # thread stands still for 2 s
#     print(f"{name}: tea ready")

# start = time.time()
# make_tea("A")
# make_tea("B")
# make_tea("C")
# print(f"Total:{time.time() }, {time.time() - start:.1f} ,{start:.1f}s")


# import time
# import asyncio

# async def make_tea(name):
#     print(f"{name}: kettle on")
#     await asyncio.sleep(2)# time.sleep(2)                  # thread stands still for 2 s
#     print(f"{name}: tea ready")

# async def main():
#     start = time.time()
#     # await make_tea("A")
#     # await make_tea("B")
#     # await make_tea("C")
#     # await asyncio.gather(make_tea('A'),make_tea('B'),make_tea('C'))
#     print(f"Total : {time.time() - start:.1f} s")
# asyncio.run(main())

