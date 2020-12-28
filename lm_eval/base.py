import abc
import random
import collections


class LM(abc.ABC):
    @abc.abstractmethod
    def loglikelihood(self, requests):
        """Compute log-likelihood of generating a continuation from a context

        :param requests: list
            A list of pairs (context, continuation)
            context: str
                Context string
            continuation: str
                The continuation over which log likelihood will be calculated. If 
                there is a word boundary, the space should be in the continuation. 
                For example, context="hello" continuation=" world" is correct.
        :return: list
            A list of pairs (logprob, isgreedy)
            logprob: float
                The log probability of `contination`
            isgreedy:
                Whether `contination` would be generated by greedy sampling from `context`
        """
        pass

    @abc.abstractmethod
    def greedy_until(self, requests):
        """Generate greedily until a stopping sequence

        :param requests: list
            A list of pairs (context, until)
            context: str
                Context string
            until: str
                The string sequence to generate until. This string sequence may 
                span across msultiple tokens, or may be part of one token.
        :return: list
            A list of strings continuation
            continuation: str
                The generated continuation.
        """
        pass

    @classmethod
    def create_from_arg_string(cls, arg_string):
        """Constructor method, in case models need additional arguments
        e.g. OpenAI API engine, paths for loading, other params

        :param arg_string: str
            Left up to individual model class to handle

        """
        return cls()


class Dataset(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.download()
        self._traindocs = None

    def download(self):
        """Downloads the task dataset if necessary"""
        pass

    @abc.abstractmethod
    def has_training_docs(self):
        """Whether the task has a training set"""
        pass
    
    @abc.abstractmethod
    def has_validation_docs(self):
        """Whether the task has a validation set"""
        pass

    @abc.abstractmethod
    def has_test_docs(self):
        """Whether the task has a test set"""
        pass

    @abc.abstractmethod
    def training_docs(self):
        """

        :return: Iterable[obj]
            A iterable of any object, that doc_to_text can handle
        """
        pass
    
    @abc.abstractmethod
    def validation_docs(self):
        pass
    
    @abc.abstractmethod
    def test_docs(self):
        pass
    
    def fewshot_examples(self, k):
        if self._traindocs is None:
            self._traindocs = list(self.training_docs())

        return random.sample(self._traindocs, k)

    @abc.abstractmethod
    def doc_to_text(self, doc):
        pass

    @abc.abstractmethod
    def doc_to_target(self, doc):
        pass

    @abc.abstractmethod
    def construct_requests(self, doc, nshot=0, prompt=False):
        pass
    
    @abc.abstractmethod
    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a 
        list of dicts, each with the following format:

        {
            "submetric": str,
            "value": float,
            "higher_is_better": bool,
            "aggregation": ([float] -> float),
        }

        * `submetric` should be the name of the metric
        * `value` should be the value of the metric
        * `higher_is_better` determines whether a higher metric is better
        * `aggregation` should be a function that takes a list of floats and 
            aggregates them into one float. This should be the same for all 
            submetrics of the same name; if it differs, an error should be 
            raised.
        """
        pass

    def fewshot_description(self):
        return ""

    def fewshot_context(self, doc, num_fewshot, provide_description):
        raw_description = self.fewshot_description()
        description = (raw_description + "\n===\n\n") if provide_description and raw_description else ""
        
        labeled_examples = "\n\n".join(
            [self.doc_to_text(doc) + self.doc_to_target(doc) for doc in self.fewshot_examples(k=num_fewshot)]
        ) + "\n\n"

        example = self.doc_to_text(doc).strip()
        return description + labeled_examples + example



def mean(arr):
    return sum(arr) / len(arr)

def median(arr):
    return arr[len(arr) // 2]


Request = collections.namedtuple('Request', ('type', 'args'))

class RequestFactory:
    def __getattr__(self, attr):
        def fn(*args):
            return Request(attr, args)
        return fn


rf = RequestFactory()
