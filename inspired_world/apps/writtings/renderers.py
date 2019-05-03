import json

from rest_framework.renderers import JSONRenderer


class WrittingJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Render the articles in a structured manner for the end user.
        """
        if data is not None:
            if len(data) <= 1:
                return json.dumps({
                    'writting': data
                })
            return json.dumps({
                'writtings': data
            })
        return json.dumps({
            'writting': 'No writting found.'
        })
