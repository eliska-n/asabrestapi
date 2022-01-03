import asab
import asab.web.rest

class CRUDWebHandler(object):
    def __init__(self, app, mongo_svc):
        self.CRUDService = mongo_svc

        web_app = app.WebContainer.WebApp

        web_app.router.add_put('/crud-myrestapi/{collection}', self.create)  # Create endpoint url
        web_app.router.add_get('/crud-myrestapi/{collection}/{id}', self.read_one)  # Read endpoint url
        web_app.router.add_put('/crud-myrestapi/{collection}/{id}', self.update)  # Update endpoint url
        web_app.router.add_delete('/crud-myrestapi/{collection}/{id}', self.delete)  # Delete endpoint url

    # Usually we will need to validate the body of incomming request and verify if it contains all the
    # desired fields and also their types.
    @asab.web.rest.json_schema_handler({
        'type': 'object',
        'properties': {
            '_id': {'type': 'string'},
            'field1': {'type': 'string'},
            'field2': {'type': 'number'},
            'field3': {'type': 'number'}
        }})
    async def create(self, request, *, json_data):
        collection = request.match_info['collection']

        result = await self.CRUDService.create(collection, json_data)
        if result:
            return asab.web.rest.json_response(request, {"result": "OK"})
        else:
            asab.web.rest.json_response(request, {"result": "FAIL"})


    async def read_one(self, request):
        collection = request.match_info['collection']
        key = request.match_info['id']
        response = await self.CRUDService.read_one(collection, key)
        return asab.web.rest.json_response(request, response)


    @asab.web.rest.json_schema_handler({
        'type': 'object',
        'properties': {
            'field1': {'type': 'string'},
            'field2': {'type': 'number'},
            'field3': {'type': 'number'}
        }})
    async def update(self, request, *, json_data):
        collection = request.match_info['collection']
        key = request.match_info["id"]

        result = await self.CRUDService.update(collection, key, json_data)
        if result:
            return asab.web.rest.json_response(request, {"result": "OK"})
        else:
            asab.web.rest.json_response(request, {"result": "FAIL"})

    async def delete(self, request):
        collection = request.match_info['collection']
        key = request.match_info["id"]
        result = await self.CRUDService.delete(collection, key)

        if result:
            return asab.web.rest.json_response(request, {"result": "OK"})
        else:
            asab.web.rest.json_response(request, {"result": "FAIL"})