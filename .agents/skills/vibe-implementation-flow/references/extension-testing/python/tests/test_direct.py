import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).absolute().parents[1]))
from new_helper import check
class Direct(unittest.TestCase):
    def test_direct_current_helper(self):
        receipt=json.loads((Path(__file__).absolute().parents[2]/"receipt.json").read_text())
        value=check(receipt,"receipt","default")
        self.assertEqual(value["findings"],[])
        self.assertEqual(value["arguments"],["receipt","default"])
