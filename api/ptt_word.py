import json
import falcon
import logging
import os

class AvailableBoardsResource(object):
    def on_get(self, req, resp):
        boards = [b.split('.json')[0] for b in os.listdir("/data")]
        resp.body = json.dumps(boards, ensure_ascii=False)

class PTTWordResource(object):
    def __init__(self):
        self.logger = logging.getLogger('x.' + __name__)

    def on_get(self, req, resp):
        
        lemma = req.get_param("lemma", required=True)
        pos = req.get_param("pos")
        board = req.get_param("board", required=True)
        year = req.get_param("year", required=True)

        # step 1: 檢查是否有該版資料
        if not os.path.isfile(f"/data/{board}.json"):
            result = {
                "result": 0,
                "error": f"no data for board: <{board}>"
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return

        with open(f"/data/{board}.json", "r") as f:
            d = json.load(f)
        
        # step 2: 確認有該版資料後，檢查是否有年份資料
        try:
            result = d[year]
        except KeyError:
            result = {
                "result": 0,
                "error": f"no data for year: <{year}> in board: <{board}>"
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return

        # step 3: 確認有該版與該年份資料後，檢查是否有該lemma資料
        try:
            result = result[lemma]
        except KeyError:
            result = {
                "result": 0,
                "error": f"no data for lemma: <{lemma}> in board: <{board}> in year <{year}>"
            }
            resp.body = json.dumps(result, ensure_ascii=False)
            return
        else:
            # 確認有該lemma資料後，檢查client是否有query特定pos
            if pos is None:  # client沒有輸入pos
                result = {
                    "result": 1,
                    "freq": {k: v / get_year_total_freq(year=year) for k, v in result.items()}
                }

                resp.body = json.dumps(result, ensure_ascii=False)
            else:   # cline有輸入pos
                try:    # 檢查該pos是否存在
                    result = {
                    "result": 1,
                    "freq": result[pos] / get_year_total_freq(year=year)
                    }
                except KeyError:
                    available_pos = [f"<{p}>" for p in result.keys()]
                    result = {
                        "result": 0,
                        "error": f"no data for lemma: <{lemma}> with pos: <{pos}>, please try pos: {', '.join(available_pos)}"
                    }
                finally:
                    resp.body = json.dumps(result, ensure_ascii=False)

def get_year_total_freq(year=None):
    with open(f"/data/sum_by_year.json", "r") as f:
            d = json.load(f)
    return d[year]
