activate_this = '/home/ubuntu/eb-virt/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/ubuntu/UnityFinalBackend/flaskapp')
#test
from flaskapp import app as application