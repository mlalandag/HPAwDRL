import configuration
from numpy.core.einsumfunc import _compute_size_by_dict
from tensorflow.python.compat.compat import _update_forward_compatibility_date_number


NUM_EPISODES                = 20
NUM_TIMESTEPS               = 300

MAX_NUM_PODS                = 5
MIN_NUM_PODS                = 1

BATCH_SIZE                  = 25

PATH_MODEL                  = './models/model.' + str(MAX_NUM_PODS) + '.keras'

UPDATE_RATE                 = 15
SAVE_RATE                   = 50      

ALPHA                       = 1
GAMMA                       = 0.99

MIN_EPSILON                 = 0.05   
EPSILON                     = 1
EPSILON_DECAY               = 0.99