#!/usr/bin/env python
#
import webapp2
import logging
from webapp2 import Route
from controller import mainh

routes = [
    Route('/', handler='controller.mainh.PageHandler:index', name='page-index'),
    Route('/gamerules', handler='controller.mainh.PageHandler:gamerules', name='page-gamerules'),
    Route('/joinus', handler='controller.mainh.PageHandler:joinus', name='page-joinus'),
    Route('/dataup', handler='controller.uploader.QUploader:upload', name='quotations-upload'),
    Route('/ajax/addDistance', handler='controller.ajax.Request:addDistance', name='ajax-addDistance'),
    Route('/ajax/getWeeklyList', handler='controller.ajax.Request:getWeeklyList', name='ajax-getWeeklyList'),
    Route('/ajax/deleteDistance', handler='controller.ajax.Request:deleteDistance', name='ajax-deleteDistance'),
    Route('/ajax/getMonthSummary', handler='controller.ajax.Request:getMonthSummary', name='ajax-getMonthSummary')
]

config = {
    'webapp2_extras.jinja2': {
        'template_path': 'view',
    },
}

#  TODO: Set debug=False on production
app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    
def handle_404(request, response, exception):
    logging.exception(exception)
    ph = mainh.PageHandler()
    ph.render_template(request, 'error/404.html', {})
    response.set_status(404)
    
app.error_handlers[404] = handle_404