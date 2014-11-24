from pyramid.view import view_config
import sumlib
import urllib.parse

@view_config(route_name='home', renderer='json')
def my_view(request):
    body = urllib.parse.unquote_plus(request.body.decode('utf-8'))
    print('body len', len(body))
    (keywords, summary) = sumlib.run(body)
    return {'keywords': keywords, 'summary': summary}
