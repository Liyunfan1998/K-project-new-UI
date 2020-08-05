import os
import sys

rootpath = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(rootpath)
from stacked_hourglass.model import hg1, hg2, hg8
from stacked_hourglass.predictor import HumanPosePredictor

# import stacked_hourglass.utils as utils
# import stacked_hourglass.res as res
# import stacked_hourglass.datasets as datasets
