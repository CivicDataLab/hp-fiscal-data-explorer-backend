from datetime import datetime
import falcon

class CORSMiddleware:
    '''
    Middleware for handling CORS.
    '''
    def process_request(self, req, resp):
        '''
        process request to set headers.
        '''
        resp.set_header('Access-Control-Allow-Origin', '*')
        
def validate_date(req, resp, resource, params):
    '''
    check for required parameters in query string and validate date format.
    '''
    params = req.params
    if 'start' not in params or 'end' not in params:
        resp.status = falcon.HTTP_400  #pylint: disable=no-member
        raise falcon.HTTPBadRequest('Incomplete Request', 'start and end date is required')  #pylint: disable=no-member
    try:
        datetime.strptime(params['start'], '%Y-%m-%d')
        datetime.strptime(params['end'], '%Y-%m-%d')
    except ValueError as err:
        resp.status = falcon.HTTP_400  #pylint: disable=no-member
        raise falcon.HTTPBadRequest('Invalid Params', str(err))  #pylint: disable=no-member