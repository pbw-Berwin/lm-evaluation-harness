HARNESS_DIR=/dccstor/mit_fm/bpan/Granite-Math/lm-eval-dev/lm-evaluation-harness

export HF_DATASETS_CACHE=/dccstor/mit_fm/bpan/Granite-Math/.cache
export HF_HOME=/dccstor/mit_fm/bpan/Granite-Math/.cache


### begin configure eval parameters
MODEL="ibm-granite/granite-3b-code-instruct"
NAME="granite-3b-code-instruct"

TASKS=minerva_math_*,gsm8k,ocw_courses,minerva-hendrycksTest*,math_sat_cot,sympy_math*,python_gsm8k

OUT=${HARNESS_DIR}/output/${NAME}_${TASKS}.json

cd ${HARNESS_DIR}
mkdir -p ${HARNESS_DIR}/output
### end configure eval parameters

### begin configure environment
TP_DEGREE=1

### end configure environment

# if testing, uncomment --limit for testing
python main.py --no_cache --model vllm --model_args pretrained=${MODEL},trust_remote_code=True --tasks $TASKS --output_path ${OUT} --tp_degree ${TP_DEGREE} # --limit 10
