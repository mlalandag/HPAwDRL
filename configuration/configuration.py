import configuration
from numpy.core.einsumfunc import _compute_size_by_dict
from tensorflow.python.compat.compat import _update_forward_compatibility_date_number


NUM_EPISODES                = 10
NUM_TIMESTEPS               = 100

NUM_OF_ACTIONS              = 3

MAX_NUM_PODS                = 5
MIN_NUM_PODS                = 1

BATCH_SIZE                  = 10

PATH_MODEL                  = 'model.' + str(MAX_NUM_PODS) + '.keras'

CPUS                        = 1
MEMORY                      = 2048

UPDATE_RATE                 = 15
SAVE_RATE                   = 50      