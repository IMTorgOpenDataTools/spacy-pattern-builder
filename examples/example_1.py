# Import a SpaCy model, parse a string to create a Doc object
import en_core_web_sm

text = 'We introduce efficient methods for fitting Boolean models to molecular data.'
nlp = en_core_web_sm.load()
doc = nlp(text)

from spacy_pattern_builder import build_dependency_pattern

# Provide a list of tokens we want to match.
match_example = [doc[i] for i in [0, 1, 3]]  # [We, introduce, methods]

''' Note that these tokens must be constitute a fully connected graph.
Otherwise, spacy-pattern-builder will raise a TokensNotFullyConnectedError.
You can get the smallest connected subgraph that includes your tokens like: '''
from spacy_pattern_builder import util
connected_tokens = util.smallest_connected_subgraph(match_example, doc)
assert match_example == connected_tokens

# Specify the token attributes / features to use
feature_dict = {  # This is equal to the default feature_dict
    'DEP': 'dep_',
    'TAG': 'tag_'
}

# Build the pattern
pattern = build_dependency_pattern(doc, match_example, feature_dict=feature_dict)

from pprint import pprint
pprint(pattern)  # A pattern in the format consumed by SpaCy's DependencyTreeMatcher:
'''
[{'PATTERN': {'DEP': 'ROOT', 'TAG': 'VBP'}, 'SPEC': {'NODE_NAME': 'node1'}},
 {'PATTERN': {'DEP': 'nsubj', 'TAG': 'PRP'},
  'SPEC': {'NBOR_NAME': 'node1', 'NBOR_RELOP': '>', 'NODE_NAME': 'node0'}},
 {'PATTERN': {'DEP': 'dobj', 'TAG': 'NNS'},
  'SPEC': {'NBOR_NAME': 'node1', 'NBOR_RELOP': '>', 'NODE_NAME': 'node3'}}]
'''

# Create a matcher and add the newly generated pattern
from spacy.matcher import DependencyTreeMatcher

matcher = DependencyTreeMatcher(doc.vocab)
matcher.add('pattern', None, pattern)

# And match away
matches = matcher(doc)
for match_id, token_idxs in matches:
    tokens = [doc[i] for i in token_idxs]
    tokens = sorted(tokens, key=lambda w: w.i)
    print(tokens)  # [We, introduce, methods]