import asab
import asab.web
import asab.web.rest

asab.Config.add_defaults(
{
	'asab:storage': {
		'type': 'mongodb',
		#'mongodb_uri': 'mongodb://mongouser:mongopassword@mongoipaddress:27017',
        'mongodb_uri': 'mongodb://eliska:secreteliska@localhost:27017',
		'mongodb_database': 'mongodatabase'
	},
})

class TutorialApp(asab.Application):

    def __init__(self):
        super().__init__()
        # Alternative for command-line flag -w
        import asab.storage
        self.add_module(asab.web.Module)
        self.add_module(asab.storage.Module)

        # Locate the web service
        self.WebService = self.get_service("asab.WebService")
        self.WebContainer = asab.web.WebContainer(self.WebService, "web")
        self.WebContainer.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

        # Initialize services, we can initialize one, or several API handlers/services here
        from .tutorial.handler import CRUDWebHandler
        from .tutorial.service import CRUDService
        self.CRUDService = CRUDService(self)
        # We need to pass the CRUDService as an argument, when instantiating the class
        self.CRUDWebHandler = CRUDWebHandler(self, self.CRUDService)
