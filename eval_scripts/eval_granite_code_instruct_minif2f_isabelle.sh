HARNESS_DIR=/dccstor/mit_fm/bpan/Granite-Math/lm-eval-dev/lm-evaluation-harness

export HF_DATASETS_CACHE=/dccstor/mit_fm/bpan/Granite-Math/.cache
export HF_HOME=/dccstor/mit_fm/bpan/Granite-Math/.cache

TASKS="minif2f_isabelle_informal2formal"
MODEL="ibm-granite/granite-3b-code-instruct"
NAME="granite-3b-code-instruct"

OUT=${HARNESS_DIR}/output/${NAME}_${TASKS}.json
mkdir -p ${HARNESS_DIR}/output

FEWSHOT=0
BATCH_SIZE=1

python ${HARNESS_DIR}/main.py \
	--model_args pretrained=${MODEL},trust_remote_code=True \
	--num_fewshot 0 \
	--model vllm \
	--tasks ${TASKS} \
	--batch_size ${BATCH_SIZE} \
	--output_path ${OUT}