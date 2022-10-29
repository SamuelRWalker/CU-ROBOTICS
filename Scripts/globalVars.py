import os

####################
# GLOBAL VARIABLES #
####################
# OUTPUT
OUTPUT_ROOT = "OutputData/"
OUTPUT_BLURRY = OUTPUT_ROOT + "Blurry/"
OUTPUT_SHARP = OUTPUT_ROOT + "Sharp/"

EXAMPLE_OUTPUT_ROOT = "ExampleOutputData/"
EXAMPLE_OUTPUT_BLURRY = EXAMPLE_OUTPUT_ROOT + "Blurry/"
EXAMPLE_OUTPUT_SHARP = EXAMPLE_OUTPUT_ROOT + "Sharp/"

# INPUT
DATA_ROOT = "RawData/"
IMAGE_ROOT = DATA_ROOT + "images/"
BACKGROUND_ROOT = DATA_ROOT + "background/"
IMAGE_BASE = "Image"
BACKGROUND_BASE = "Background"
FILE_TYPE = ".jpg"

# CONST GLOBALS
IMAGE_SIZE = 512
NUM_IMAGES = len([entry for entry in os.listdir(IMAGE_ROOT) if os.path.isfile(os.path.join(IMAGE_ROOT, entry))])
NUM_BACKGROUNDS= len([entry for entry in os.listdir(BACKGROUND_ROOT) if os.path.isfile(os.path.join(BACKGROUND_ROOT, entry))])