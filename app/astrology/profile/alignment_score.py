class AlignmentScoreCalculator:

    @classmethod
    def calculate(
        cls,
        gifts,
        potential,
        edges,
        drains
    ):

        score = 50

        score += len(gifts) * 5

        score += len(potential) * 3

        score -= len(edges) * 2

        score -= len(drains) * 2

        score = max(
            0,
            min(score, 100)
        )

        return score