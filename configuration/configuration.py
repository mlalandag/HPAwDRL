import configuration
from numpy.core.einsumfunc import _compute_size_by_dict
from tensorflow.python.compat.compat import _update_forward_compatibility_date_number


NUM_EPISODES                = 50
NUM_TIMESTEPS               = 100

MAX_NUM_PODS                = 5
MIN_NUM_PODS                = 1

BATCH_SIZE                  = 10

PATH_MODEL                  = './models/model.' + str(MAX_NUM_PODS) + '.keras'

UPDATE_RATE                 = 10
SAVE_RATE                   = 25      

ALPHA                       = 1
GAMMA                       = 0.99

MIN_EPSILON                 = 0.05   
EPSILON                     = 0.99
EPSILON_DECAY               = 0.95