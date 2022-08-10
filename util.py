import json
import re
from typing import Dict
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from xml.dom import ValidationErr

"""
TODO: Write whatever class or function you may need
but, don't use any third party library
feel free to make any changes in the given class and its methods' arguments or implementation as you see fit
"""

BASE_URL = 'https://intern-test-server.herokuapp.com'

def get_result_from_request(req):
    result = {}
    try:
        with urlopen(req) as res:
            body = res.read().decode('utf-8')
            result['body'] = json.loads(body)
            result['code'] = res.status

            return result
    except HTTPError:
        result['code'] = 401
        return result
    except Exception as e:
        print(e)
        return result
    


class NetworkRequest:
    @staticmethod
    def get(endpoint, headers = {}):
        url = BASE_URL + endpoint

        req = Request(url=url, method='GET')
        for key, value in headers.items():
            req.add_header(key, value)
        
        return get_result_from_request(req)
    
    @staticmethod
    def post(endpoint, data, headers = {}):
        url = BASE_URL + endpoint
        data = json.dumps(data).encode('utf-8')

        req = Request(url=url, data=data)
        for key, value in headers.items():
            req.add_header(key, value)
        
        return get_result_from_request(req)
       

    @staticmethod
    def put():
        pass

    @staticmethod
    def delete():
        pass



