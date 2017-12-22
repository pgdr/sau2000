from sau.models import QUALITIES


def _weights(sheeps):
    weights = [s.weight for s in sheeps]
    upper = max(weights)
    weight_labels = list(range(0, int(upper + 2), 200))
    weight_lst = [0 for _ in weight_labels]
    for i, w in enumerate(weight_labels):
        for sw in weights:
            if w < sw <= w + 200:
                weight_lst[i] += 1
    return weight_lst, weight_labels


def _qualities(sheeps):
    qualities = [s.quality for s in sheeps]
    quality_lst = []
    quality_labels = []
    for Q in QUALITIES:
        # Q = ('e', 'E')
        quality_lst.append(qualities.count(Q[0]))
        quality_labels.append(Q[1])
    return quality_lst, quality_labels


def get_statistics(sheeps):
    """Return qualities_count/quality_labels, weight_count/weight_labels for use in
    barchart.

    """

    quality_lst, quality_labels = _qualities(sheeps)
    weight_lst, weight_labels = _weights(sheeps)

    return quality_lst, quality_labels, weight_lst, weight_labels
