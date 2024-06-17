import json
from lm_eval import tasks, evaluator
import argparse


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--results_json", type=str, default='./llemma_7b_maj1.json')
args = parser.parse_args()

with open(args.results_json, 'r') as f:
   results = json.load(f) 

import pdb; pdb.set_trace()

print(evaluator.make_table(results))
