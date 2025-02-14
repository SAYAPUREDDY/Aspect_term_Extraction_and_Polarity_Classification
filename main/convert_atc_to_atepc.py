"""
This scripts works as a function to convert the apc format to atepc format

You will need to provide the path to the apc file as an argument to the function.

"""

from pyabsa.utils.absa_utils.absa_utils import convert_apc_set_to_atepc_set

convert_apc_set_to_atepc_set(
    "C:/Users/91965/SSST/1.My_Git_Clones/Aspect_term_Extraction_and_Polarity_Classification/segmented_data/valid.csv.apc"
)