"""Starting point for our Flask Website"""
from homeserver.core.utility import debug_print
from homeserver import create_app
debug_print(__file__)
# from homeserver.apis.views import apis

if __name__ == 'main':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
debug_print(__file__)
