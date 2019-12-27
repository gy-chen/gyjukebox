import collections


class CosineSimScorer:
    def score(self, bow1, mag1, bow2, mag2):
        dot_prod = 0
        for token, freq in bow1.items():
            dot_prod += freq * bow2.get(token, 0)

        return (dot_prod + 1) / ((mag1 * mag2) + 1)
