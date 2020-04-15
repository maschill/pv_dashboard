import sys
import os

# add this path to python include path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "src"))

# activate virtual env
activate_venv_file = os.path.join(os.path.dirname(__file__), "solarfoo_venv", "bin", "activate_this.py")
exec(open(activate_venv_file).read(), {'__file__': activate_venv_file})

from src.hello_world import app, server
