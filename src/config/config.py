from dynaconf import Dynaconf

settings: dict = Dynaconf(
    settings_files=['settings.yaml'],
)