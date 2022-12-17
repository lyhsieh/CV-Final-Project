python scripts/inference.py \
--exp_dir=output_source1 \
--checkpoint_path=pretrained_models/psp_ffhq_encode.pt \
--data_path=input_source1 \
--test_batch_size=2 \
--test_workers=2 \
--interpolation