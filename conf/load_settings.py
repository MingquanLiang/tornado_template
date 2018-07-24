import yaml


class LazyObject(object):

    def __init__(self):
        pass

settings = LazyObject()

with open("settings.yaml", mode="r", encoding="utf-8") as f:
    data = yaml.load(f)

for key, value in data.items():
    setattr(settings, key, value)
