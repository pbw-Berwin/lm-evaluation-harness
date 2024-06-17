HARNESS_DIR=/dccstor/mit_fm/bpan/Granite-Math/lm-evaluation-harness

export HF_DATASETS_CACHE=/dccstor/mit_fm/bpan/Granite-Math/.cache
export TRANSFORMERS_CACHE=/dccstor/mit_fm/bpan/Granite-Math/.cache


### begin configure eval parameters
MODEL="ibm-granite/granite-3b-code-base"
NAME="granite-3b-code-base"

# TASKS=minerva_math_*,gsm8k,ocw_courses,minerva-hendrycksTest*,math_sat_cot,sympy_math*,python_gsm8k
# TASKS=python_gsm8k
# TASKS=minerva-hendrycksTest*
TASKS=sympy_math*

OUT=${HARNESS_DIR}/output/${NAME}_${TASKS}.json

# uncomment line below to run a subset of tasks, useful for testing.
# TASKS=minerva_math_prealgebra,gsm8k,ocw_courses,minerva-hendrycksTest-abstract_algebra,math_sat_cot,sympy_math_prealgebra,python_gsm8k

cd ${HARNESS_DIR}
mkdir -p ${HARNESS_DIR}/output
### end configure eval parameters

### begin configure environment
TP_DEGREE=1

### end configure environment

# if testing, uncomment --limit for testing
python main.py --no_cache --model vllm --model_args pretrained=${MODEL} --tasks $TASKS --output_path ${OUT} --tp_degree ${TP_DEGREE} # --limit 10
