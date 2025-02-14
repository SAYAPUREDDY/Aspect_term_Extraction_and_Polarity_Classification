"""
This script trains an Aspect Term Extraction model using the PyABSA framework. 
It configures the FAST_LCF_ATEPC model, sets training parameters, and loads the 
specified dataset for training. 
The training process is flexible, supporting checkpointing, auto device selection, and augmentation options.

Note: Replace 'integrated_datasets\atepc_datasets\13730.Berlin_dataset' with your actual dataset path.
Note: Please replace the number of Epochs in the pyabsa library
Note: Please change the custom dataset based on your dataset

Returns:
    if the training is successful u will get the checkpoints saved to your local filesystem.
    which can later be used while testing the model.
"""


from pyabsa import ModelSaveOption, DeviceTypeOption
from pyabsa import AspectTermExtraction as ATEPC
from pyabsa import DatasetItem
import warnings

warnings.filterwarnings("ignore")

# dataset_dir = 'integrated_datasets\atepc_datasets\13730.Berlin_dataset'
# my_dataset = DatasetItem("my_dataset", [dataset_dir])
# my_dataset = '100.CustomDataset'
my_dataset = '134.NKD_store'

# this config contains 'pretrained_bert', it is based on pretrained models 
config = (
    ATEPC.ATEPCConfigManager.get_atepc_config_english()
)   
# improved version of LCF-ATEPC
config.model = ATEPC.ATEPCModelList.FAST_LCF_ATEPC

config.batch_size = 16
config.patience = 2
config.log_step = -1
config.seed = [1]
config.verbose = False 
config.notice = (
    "This is an training example for aspect term extraction"  
)

trainer = ATEPC.ATEPCTrainer(
    config=config,
    dataset=my_dataset,
    from_checkpoint="english",  # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
    auto_device=DeviceTypeOption.AUTO,  # use cuda if available
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,  # save state dict only instead of the whole model
    load_aug=False,  # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
)

