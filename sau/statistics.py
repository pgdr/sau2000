from collections import namedtuple
from io import StringIO

# BE CAREFUL WHAT YOU IMPORT ABOVE matplotlib.use('Agg')
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from sau.models import QUALITIES
from datetime import datetime as dt

stats = namedtuple(
    'stats',
    ['body_count', 'weight_min', 'weight_max', 'weight_avg', 'weight_std'])
plots = namedtuple('plots', ['quality', 'weight', 'lpy'])

_SVG_ARGS = """
viewBox="0 0 460 345"
preserveAspectRatio="xMidYMin slice"
style="max-width: 100%;"
"""


def __post_process_svg(svg):
    start = svg.index('<svg ')
    stop = svg.index('>', start)
    svg = svg[:start] + svg[stop:]
    svg = svg[:start] + '<svg %s' % _SVG_ARGS + svg[start:]
    return svg


def _svg(data, labels):
    arr = np.array(data)
    fig, ax = plt.subplots()

    plt.bar(np.arange(len(data)), data, tick_label=list(map(str, labels)))

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)  # rewind the data
    svg_data = imgdata.read()
    imgdata.close()
    plt.close(fig)
    del imgdata  # Before deleting these lines, recall
    del fig      # Chesterton's fence
    return __post_process_svg(svg_data)


def _lambs_per_year(sheeps):
    if not sheeps:
        return None
    current_year = dt.now().year
    start_year = min([s.birth_date_utc.year for s in sheeps])

    year_labels = list(range(start_year, current_year + 1))
    year_lst = [0] * len(year_labels)
    for s in sheeps:
        y = s.birth_date_utc.year
        idx = year_labels.index(y)
        year_lst[idx] += 1
    return _svg(year_lst, year_labels)


def _weights(sheeps):
    if not sheeps:
        return None
    weights = [s.weight for s in sheeps if s.weight]
    upper = max(weights)
    weight_labels = list(range(0, int(upper + 2), 200))
    weight_lst = [0] * len(weight_labels)
    for i, w in enumerate(weight_labels):
        for sw in weights:
            if w < sw <= w + 200:
                weight_lst[i] += 1
    return _svg(weight_lst, weight_labels)


def _qualities(sheeps):
    if not sheeps:
        return None
    qualities = [s.quality for s in sheeps if s.quality]
    quality_lst = []
    quality_labels = []
    for Q in QUALITIES:
        # Q = ('e', 'E')
        quality_lst.append(qualities.count(Q[0]))
        quality_labels.append(Q[1])
    return _svg(quality_lst, quality_labels)


def get_statplots(dead_sheeps, all_sheeps):
    """Return qualities_count/quality_labels, weight_count/weight_labels for use in
    barchart.

    """

    qsvg = _qualities(dead_sheeps)
    wsvg = _weights(dead_sheeps)
    lpysvg = _lambs_per_year(all_sheeps)

    return plots(quality=qsvg, weight=wsvg, lpy=lpysvg)


def get_statistics(dead_sheeps, all_sheeps):
    """Return qualities_count/quality_labels, weight_count/weight_labels for use in
    barchart.

    """
    stat = {
        'body_count': 0,
        'weight_min': 0,
        'weight_max': 0,
        'weight_avg': 0,
        'weight_std': 0,
    }

    to_whole = lambda x: '%d' % int(x)

    if dead_sheeps:
        arr = np.array([s.weight for s in dead_sheeps])
        stat['body_count'] = len(arr)
        stat['weight_min'] = to_whole(arr.min())
        stat['weight_max'] = to_whole(arr.max())
        stat['weight_avg'] = to_whole(arr.mean())
        stat['weight_std'] = to_whole(arr.std())
    return stats(**stat)
