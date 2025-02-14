from pyabsa import ModelSaveOption, DeviceTypeOption
from pyabsa import AspectPolarityClassification as APC


# config = APC.APCConfigManager.get_apc_config_glove()  # get pre-defined configuration for GloVe model, the default embed_dim=300
# config = APC.APCConfigManager.get_apc_config_multilingual()  # this config contains 'pretrained_bert', it is based on pretrained models
config = APC.APCConfigManager.get_apc_config_english()


config.num_epoch = 1
config.model = APC.APCModelList.FAST_LSA_T_V2
dataset='107.store'
trainer = APC.APCTrainer(
    config=config,
    dataset=dataset,
    from_checkpoint="english",
    # if you want to resume training from our pretrained checkpoints, you can pass the checkpoint name here
    auto_device=DeviceTypeOption.AUTO,
    path_to_save=None,  # set a path to save checkpoints, if it is None, save checkpoints at 'checkpoints' folder
    checkpoint_save_mode=ModelSaveOption.SAVE_MODEL_STATE_DICT,
    load_aug=False,
    # there are some augmentation dataset for integrated datasets, you use them by setting load_aug=True to improve performance
)