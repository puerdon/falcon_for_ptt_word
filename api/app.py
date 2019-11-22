import falcon
from ptt_word import PTTWordResource

api = application = falcon.API()

ptt_word_resource = PTTWordResource()
api.add_route('/query', ptt_word_resource)