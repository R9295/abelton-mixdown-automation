from main import Mixdown
from log import clear_log

def create_instance(c_instance):
    clear_log()
    return Mixdown(c_instance)
