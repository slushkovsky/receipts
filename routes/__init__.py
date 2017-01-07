from .. import app 

from . import users
from . import recognize

app.register_blueprint(users    .bp) 
app.register_blueprint(recognize.bp) 
