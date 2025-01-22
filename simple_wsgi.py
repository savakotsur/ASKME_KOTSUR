def application(environ, start_response):
    params = environ.get('QUERY_STRING', '').split('&')
    response_body = '\n'.join(params)
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return [response_body.encode()]