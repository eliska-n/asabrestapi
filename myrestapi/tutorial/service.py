import asab
import asab.storage.exceptions


# We want to start logging here
import logging

#

L = logging.getLogger(__name__)

#

class CRUDService(asab.Service):

# Using inheritance from the asab.Service allows us to register the service as 'crud.CRUDService',
# which would in turn enable us to call it by this name from elsewhere within the application.
# We do not use this functionality for this service, but look around the code and we will find,
# that it was silently used several times already for different ASAB services.
    def __init__(self, app, service_name='crud.CRUDService'):
        super().__init__(app, service_name)
        # And here we do it again, we use the "app.get_service()" to locate a service registered within
        # our app by its service name.
        self.MongoDBStorageService = app.get_service("asab.StorageService")


    # Below, we define class methods, that our handler will use to provide the desired functionality,
    # requested by our microservice users. These may not be limited to the methods tied to the handler's
    # CRUD functionality directly (e.g. the create, read, update and delete methods), but also any other
    # logical extensions of these, that are desirable. Bear in mind however, that we should always
    # strive for the "simplest code possible that works".


    async def create(self, collection, json_data):
        obj_id = json_data.pop("_id")

        cre = self.MongoDBStorageService.upsertor(collection, obj_id)
        for key, value in zip(json_data.keys(), json_data.values()):
            cre.set(key, value)

        try:
            await cre.execute()
            return "OK"
        except asab.storage.exceptions.DuplicateError as e:
            L.warning("Document you are trying to create already exists.")
            return None


    async def read_one(self, collection, key):
        response = await self.MongoDBStorageService.get_by(collection, "_id", key)
        return response


    async def update(self, collection, obj_id, document):
        original = await self.read_one(collection, obj_id)
        cre = self.MongoDBStorageService.upsertor(collection, original["_id"], original["_v"])
        for key, value in zip(document.keys(), document.values()):
            cre.set(key, value)

        try:
            await cre.execute()
            return "OK"

        except KeyError:
            return None


    async def delete(self, collection, key):
        try:
            await self.MongoDBStorageService.delete(collection, key)
            return True
        except KeyError:
            return False
