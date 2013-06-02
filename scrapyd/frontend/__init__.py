import posixpath
import pkg_resources

from twisted.web import resource, static
from twisted.web.util import Redirect

class BaseFrontEnd(resource.Resource):
    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root

    def render(self, request, **kwargs):
        request.setResponseCode(404)
        return """<html><head><title>No frontend</title><h1>No frontend</h1>
        </body>
        </html>
        """

class FrontEnd(resource.Resource):
    document_index = "index.html"
    
    def __init__(self, root, path=None, **kwargs):
        self.root = root
        htdocs_dir = self.root.config.get("htdocs_dir")
        if htdocs_dir:
            if htdocs_dir.strip() == "":
                htdocs_dir = None
            else:
                htdocs_dir = posixpath.expanduser(htdocs_dir)
        print htdocs_dir
        self.path = (path or htdocs_dir or 
            pkg_resources.resource_filename("scrapyd", "frontend/site"))
        print self.path
        resource.Resource.__init__(self, **kwargs)

    def render(self, request, **kwargs):
        if not posixpath.exists(self.path):
            request.setResponseCode(404)
            return "Path not found"
    
        path = ("/%s" % self.document_index if request.path == "/" 
                    else request.path)
        r = posixpath.join(self.path, 
            path[1:] if path.startswith("/") else path)
        return static.File(r).render(request, **kwargs)
