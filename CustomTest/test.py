from core.generate_models import generate_from_func_models as gm
from pathlib import Path
from Models import U

shared_str = r"C:\Users\user\Desktop\SharedJson"
destination_str = r"C:\Users\user\source\repos\NeoNix-Lab\qtpy-dispatch-sharp-core\socket_dispatcher_python\Models"

def gen():
    shared = Path(shared_str)
    destination = Path(destination_str)
    return  gm(shared, destination)