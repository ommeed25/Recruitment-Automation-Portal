from importlib import import_module

_real_main = import_module("linkedin_integration.app.main")

app = _real_main.app
