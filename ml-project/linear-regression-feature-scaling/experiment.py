"""Compare batch gradient descent under a fixed feature-scale mismatch."""

from math import fsum
from typing import NamedTuple


def fixture(level: float) -> list[tuple[float, float, float]]:
    return [
        (x, z, 1 + 2 * x + 0.03 * z)
        for x in (-level, level)
        for z in (-100 * level, 100 * level)
    ]


TRAIN = fixture(1.0)
TEST = fixture(0.5)
STEPS = 200
DIVERGENCE_MSE = 1e12


class Result(NamedTuple):
    name: str
    updates: int
    train_mse: float
    test_mse: float
    diverged: bool


def mse(rows: list[tuple[float, float, float]], weights: tuple[float, float, float]) -> float:
    b, w1, w2 = weights
    return fsum((b + w1 * x + w2 * z - y) ** 2 for x, z, y in rows) / len(rows)


def fit(name: str, scale: float, rate: float) -> Result:
    train = [(x, z / scale, y) for x, z, y in TRAIN]
    test = [(x, z / scale, y) for x, z, y in TEST]
    weights = (0.0, 0.0, 0.0)
    for step in range(1, STEPS + 1):
        b, w1, w2 = weights
        errors = [b + w1 * x + w2 * z - y for x, z, y in train]
        factor = 2 * rate / len(train)
        weights = (
            b - factor * fsum(errors),
            w1 - factor * fsum(error * x for error, (x, _, _) in zip(errors, train)),
            w2 - factor * fsum(error * z for error, (_, z, _) in zip(errors, train)),
        )
        loss = mse(train, weights)
        if loss >= DIVERGENCE_MSE:
            return Result(name, step, loss, mse(test, weights), True)
    return Result(name, STEPS, mse(train, weights), mse(test, weights), False)


def run() -> list[Result]:
    # The centered feature columns are orthogonal. For each coefficient the
    # least-squares solution is sum(feature * target) / sum(feature ** 2).
    reference = (
        fsum(y for _, _, y in TRAIN) / len(TRAIN),
        fsum(x * y for x, _, y in TRAIN) / fsum(x * x for x, _, _ in TRAIN),
        fsum(z * y for _, z, y in TRAIN) / fsum(z * z for _, z, _ in TRAIN),
    )
    return [
        Result("closed-form OLS", 0, mse(TRAIN, reference), mse(TEST, reference), False),
        fit("raw, lr=0.05", 1.0, 0.05),
        fit("raw, lr=0.00005", 1.0, 0.00005),
        fit("scaled, lr=0.05", max(abs(z) for _, z, _ in TRAIN), 0.05),
    ]


if __name__ == "__main__":
    for result in run():
        print(
            f"{result.name:20} updates={result.updates:3}  "
            f"train_mse={result.train_mse:.6g}  test_mse={result.test_mse:.6g}  "
            f"diverged={result.diverged}"
        )
