import falcon
from ptt_word import PTTWordResource, AvailableBoardsResource

api = application = falcon.API()

ptt_word_resource = PTTWordResource()
api.add_route('/query', ptt_word_resource)

available_boards_resource = AvailableBoardsResource()
api.add_route('/available_boards', available_boards_resource)