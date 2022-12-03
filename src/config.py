import os


class BaseConfig:
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    STAGE = os.getenv("STAGE")


class Local(BaseConfig):
    STAGE = "local"


class Development(BaseConfig):
    STAGE = "dev"
    pass


class Staging(BaseConfig):
    pass


class Production(BaseConfig):
    pass


class Test(BaseConfig):
    pass
