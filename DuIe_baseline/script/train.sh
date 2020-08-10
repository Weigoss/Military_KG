set -eux

export BATCH_SIZE=16
export LR=2e-5
export EPOCH=80
export SAVE_STEPS=5000

export SAVE_PATH=./
export TASK_DATA_PATH=./data/
export MODEL_PATH=./pretrained_model/
export TRAIN_FILE=military_train.json
export DEV_FILE=military_dev.json

export FLAGS_sync_nccl_allreduce=1
export PYTHONPATH=./ernie:${PYTHONPATH:-}

python -u ./ernie/run_duie.py \
                   --use_cuda true \
                   --do_train true \
                   --do_val true \
                   --do_test false \
                   --batch_size ${BATCH_SIZE} \
                   --init_checkpoint ${MODEL_PATH}params \
                   --num_labels 8 \
                   --chunk_scheme "IOB" \
                   --label_map_config ${TASK_DATA_PATH}relation2label.json \
                   --spo_label_map_config ${TASK_DATA_PATH}label2relation.json \
                   --train_set ${TASK_DATA_PATH}${TRAIN_FILE} \
                   --dev_set ${TASK_DATA_PATH}${DEV_FILE} \
                   --vocab_path ${MODEL_PATH}vocab.txt \
                   --ernie_config_path ${MODEL_PATH}ernie_config.json \
                   --checkpoints ${SAVE_PATH}checkpoints \
                   --save_steps ${SAVE_STEPS} \
                   --validation_steps ${SAVE_STEPS} \
                   --weight_decay 0.01 \
                   --warmup_proportion 0.0 \
                   --use_fp16 false \
                   --epoch ${EPOCH} \
                   --max_seq_len 128 \
                   --learning_rate ${LR} \
                   --skip_steps 10 \
                   --num_iteration_per_drop_scope 1 \
                   --random_seed 1
