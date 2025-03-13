from sqlalchemy.orm import DeclarativeBase
import importlib
import pkgutil


class Base(DeclarativeBase):
    pass


# Dynamically import all models inside `app.db.models`
models_package = "app.db.models"
for _, module_name, _ in pkgutil.iter_modules([models_package.replace(".", "/")]):
    importlib.import_module(f"{models_package}.{module_name}")
