python scripts/inference.py \
--exp_dir=. \
--checkpoint_path=pretrained_models/psp_ffhq_encode.pt \
--data_path=input_EuropeanFace \
--test_batch_size=2 \
--test_workers=2 \
--interpolation