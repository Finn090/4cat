# original by William Leif Hamilton, https://github.com/williamleif/histwords
# See 'license' in the 'histwords' folder
# File changed for Py3 compatibility and to make import paths work for 4CAT

from backend.lib.histwords.representations import sparse_io

from collections import Counter
import numpy as np
import pyximport

def run(word_gen, index, window_size, out_file):
    context = []
    pair_counts = Counter()
    for word in word_gen:
        context.append(index[word])
        if len(context) > window_size * 2 + 1:
            context.pop(0)
        pair_counts = _process_context(context, pair_counts, window_size)
    pyximport.install(setup_args={"include_dirs": np.get_include()})
    sparse_io.export_mat_from_dict(pair_counts, out_file)

def _process_context(context, pair_counts, window_size):
    if len(context) < window_size + 1:
        return pair_counts
    target = context[window_size]
    indices = list(range(0, window_size))
    indices.extend(list(range(window_size + 1, 2 * window_size + 1)))
    for i in indices:
        if i >= len(context):
            break
        pair_counts[(target, context[i])] += 1
    return pair_counts
