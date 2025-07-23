from .generate_models import generate_models, get_shared_dir
from typing import Literal
from pathlib import Path
import os, sys

STATE: Literal["Imported", "Refused"] = "Refused"

def get_importer_path():
    # f_back è il frame chiamante
    frame = sys._getframe(1)
    path = frame.f_code.co_filename
    return os.path.abspath(path)

dir_path = Path.cwd()

try :
    shared_dir =get_shared_dir()
    out_dir =Path(rf"{dir_path}/generated_models")
    generate_models(shared_dir, out_dir)
    STATE = "Imported"
except Exception as e :
    print(e)

__ALL__ = [STATE]