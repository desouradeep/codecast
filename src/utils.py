import random
import string


def id_generator():
    '''
    Generates random strings, meant to assign as ids for pagelets
    '''
    return ''.join(random.choice(string.hexdigits) for _ in range(6))


def pagelet_generator(views):
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
