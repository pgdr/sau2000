from sau.models import QUALITIES
from datetime import datetime as dt

def _lambs_per_year(sheeps):
    if not sheeps:
        return [], []
    current_year = dt.now().year
    start_year = min([s.birth_date_utc.year for s in sheeps])

    year_labels = list(range(start_year, current_year+1))
    year_lst = [0] * len(year_labels)
    for s in sheeps:
        y = s.birth_date_utc.year
        idx = year_labels.index(y)
        year_lst[idx] += 1
    return year_lst, year_labels


def _weights(sheeps):
    if not sheeps:
        return [], []
    weights = [s.weight for s in sheeps if s.weight]
    upper = max(weights)
    weight_labels = list(range(0, int(upper + 2), 200))
    weight_lst = [0] * len(weight_labels)
    for i, w in enumerate(weight_labels):
        for sw in weights:
            if w < sw <= w + 200:
                weight_lst[i] += 1
    return weight_lst, weight_labels


def _qualities(sheeps):
    if not sheeps:
        return [], []
    qualities = [s.quality for s in sheeps if s.quality]
    quality_lst = []
    quality_labels = []
    for Q in QUALITIES:
        # Q = ('e', 'E')
        quality_lst.append(qualities.count(Q[0]))
        quality_labels.append(Q[1])
    return quality_lst, quality_labels


def get_statistics(dead_sheeps, all_sheeps):
    """Return qualities_count/quality_labels, weight_count/weight_labels for use in
    barchart.

    """

    quality_lst, quality_labels = _qualities(dead_sheeps)
    weight_lst, weight_labels = _weights(dead_sheeps)
    lambyear_lst, lambyear_labels = _lambs_per_year(all_sheeps)

    return (quality_lst, quality_labels, weight_lst, weight_labels,
            lambyear_lst, lambyear_labels)
