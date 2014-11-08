import random
import string
import json


def id_generator():
    '''
    Generates random strings, meant to assign as ids for pagelets
    '''
    return ''.join(random.choice(string.hexdigits) for _ in range(6))


def pagelet_dict_generator(views):
    '''
    Bind urls with pagelet ids
    '''
    pagelets = []
    ids = {}

    for key, value in views.iteritems():
        id = id_generator()
        pagelets.append({
            'id': id,
            'url': value,
        })
        ids['ID_%s' % key] = id

    return pagelets, ids


def validate_consumer_payload(payload):
    '''
    Validates the parameters passed in via payload.
    To be used before pushing on to queue.
    '''
    payload = json.loads(payload)
    if 'broadcast' in payload:
        broadcast = payload['broadcast']
    else:
        broadcast = False

    if 'data' in payload:
        data = payload['data']
    else:
        data = None

    return data, broadcast
