import inspect,os
from loader_probe import SNAPSHOT
from new_helper import check as current, module
from historical_helper import check as historical
def observe(receipt):
    helper=historical if os.environ.get("EXTENSION_ORIGIN")=="old" else current
    arguments=("receipt",os.environ.get("EXTENSION_ARGUMENT","default"))
    result=helper(receipt,*arguments)
    result["helper_origin"]=inspect.getsourcefile(helper)
    result["helper_module"]=helper.__module__
    result["loader_start"]=SNAPSHOT
    return result
