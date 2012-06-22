"""Social auth models"""
# TODO define protocol for implementing modules...


from social_auth import conf


models_module = conf.get_models_module()

this_module = globals()
for key in dir(models_module):
    this_module[key] = getattr(models_module, key)
