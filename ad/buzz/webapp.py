from flask import Blueprint, render_template, request
from ad.model import Buzz, BuzzType, session

buzz = Blueprint(
    'buzz', __name__,
    template_folder='templates',
    static_folder='static')


@buzz.route('/')
def index():
    # Removing the port from host info. This will be used to bind
    # socket.io client API to our server.
    host = request.host.split(':')[0]
    return render_template('buzz/index.html', host=host)

@buzz.route('/post', methods=('POST',))
def post():
    buzz = Buzz()
    buzz.type_ = get_or_create(BuzzType, name=u'twitter')
    session.save()
