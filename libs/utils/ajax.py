from flask import jsonify, make_response


def ajax_data(response_code, data=None, error=None, next=None, message=None):
    """if the response_code is true, then the data is set in 'data',
    if the response_code is false, then the data is set in 'error'
    """
    r = dict(response='ok', data=data, error='', next='', message='')
    if response_code is True or response_code.lower() in ('ok', 'yes', 'true'):
        r['response'] = 'ok'
    else:
        r['response'] = 'fail'
    if data is not None:
        r['data'] = data
    if error:
        r['error'] = error
    if next:
        r['next'] = next
    if message:
        r['message'] = message
    return jsonify(r)


def json_ok(data='', next=None, message=None):
    """
    return a success response
    """
    r = ajax_data('ok', data=data, next=next, message=message)
    return make_response(r)


def json_fail(error='', data=None, next=None, message=None):
    """
    return an error response
    """
    r = ajax_data('fail', data=data, next=next, message=message)
    return make_response(r)
