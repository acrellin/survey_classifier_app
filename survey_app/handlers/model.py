'''Handler for '/models' route.'''

from .base import BaseHandler
from baselayer.app.custom_exceptions import AccessError

import requests
import tornado.web


class ModelHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, model_id=None):
        if model_id is not None:
            model_info = requests.get(
                '{}/models/{}'.format(self.cfg['cesium_app:url'], model_id),
                cookies=self.get_cesium_auth_cookie()).json()['data']
        else:
            response = requests.get(
                '{}/models'.format(self.cfg['cesium_app:url']),
                cookies=self.get_cesium_auth_cookie())
            print('\n\nself.get_cesium_auth_cookie():', self.get_cesium_auth_cookie())
            print('\n\n ----- model response from cesium web:', response, '\n\n')
            print(response.content, '\n\n')
            model_info = [model for model in response.json()['data'] if
                          model['project_id'] ==
                          self.cfg['cesium_app:survey_classifier_project_id']]

        return self.success(model_info)
