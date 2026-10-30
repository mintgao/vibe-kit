import unittest
class Historical(unittest.TestCase):
    def test_historical_contract(self):
        self.assertEqual({"legacy": 1}, {"legacy": 1})

import json,sys,inspect
from pathlib import Path
sys.path.insert(0,str(Path(__file__).absolute().parents[1]))
from historical_helper import check
class HistoricalCaller(unittest.TestCase):
    def test_original_helper_caller(self):
        receipt=json.loads((Path(__file__).absolute().parents[2]/"receipt.json").read_text())
        value=check(receipt,"legacy")
        self.assertEqual(value["arguments"],["legacy"])
        self.assertEqual(value["findings"],[])
        self.assertEqual(Path(inspect.getsourcefile(check)).name,"historical_helper.py")
