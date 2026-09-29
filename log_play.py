# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
# )

# logger = logging.getLogger("app.routers.post")

# logger.debug("this will NOT show")
# logger.info("post created id=%s by user=%s", 12, 3)
# logger.warning("login failed for %s", "someone@example.com")

import logging

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
console = logging.StreamHandler()
console.setFormatter(formatter)
file_handler = logging.FileHandler("play.log")
file_handler.setFormatter(formatter)

root = logging.getLogger()        # no argument = the root logger
root.setLevel(logging.DEBUG)
root.addHandler(console)
root.addHandler(file_handler)

logger = logging.getLogger("app.routers.post")
logger.info("goes to the console AND to play.log")
# print(console.setFormatter(formatter))

try:
    1 / 0
except ZeroDivisionError:
    logger.exception("something broke")