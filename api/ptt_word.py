import json
import falcon
import logging
import os

class PTTWordResource(object):
    def __init__(self):
        self.logger = logging.getLogger('x.' + __name__)

    def on_get(self, req, resp):
        
        lemma = req.get_param("lemma", required=True)
        pos = req.get_param("pos")
        board = req.get_param("board", required=True)
        year = req.get_param("year", required=True)

        with open(f"/data/{board}.json", "r") as f:
            d = json.load(f)
        try:
            result = d[year]
        except KeyError:
            result = {
                "result": 0,
                "error": f"no data for year: {year}"
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return

        try:
            result = result[lemma]
            result = {
                "result": 1,
                "freq": result
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return
        except KeyError:
            result = {
                "result": 0,
                "error": f"no data for lemma: {lemma}"
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return

        