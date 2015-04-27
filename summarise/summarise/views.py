from pyramid.view import view_config
import sumlib
import urllib.parse
from json import loads

# @view_config(route_name='home2', renderer='json')
# def my_view(request):
#     body = urllib.parse.unquote_plus(request.body.decode('utf-8'))
#     print(body)
#     print('body len', len(body))
#     (keywords, summary) = sumlib.run(body)
#     print(keywords)
#     print()
#     return {'keywords': keywords, 'summary': summary}

@view_config(route_name='home', renderer='json')
def posts_summary(request):
    # body = request.body.decode('utf-8')
    body = loads(request.body.decode('utf-8'))
    keywords, posts = sumlib.posts_run(body)

    # (keywords, summary) = sumlib.run(body)
    # print(keywords)
    # print()
    return {'keywords': keywords, 'posts': posts}
