from flask import Blueprint as oBlueprint
from flask.ext.principal import PermissionDenied

class Blueprint(oBlueprint):
    def __init__(self, name, import_name, **kwargs):
        self.required_permission = None

        if 'required_permission' in kwargs:
            self.required_permission = kwargs['required_permission']
            del(kwargs['required_permission'])

        oBlueprint.__init__(self, name, import_name, **kwargs)

    def route(self, rule, **options):
        if self.required_permission is None:
            return oBlueprint.route(self, rule, **options)

        route = oBlueprint.route(self, rule, **options)

        def decorator(f):
            f = self.required_permission.require()(f)
            return route(f)
        return decorator