"""The search-wide gate on pure noise: the unshifted value drawn exactly like the shifts, so the rate should be about 1/33. No world and no project seed. See results/r2-screen.md, Result."""
import numpy as np

COLUMNS, SHIFTS, TRIES = 320, 32, 400


def rate(rng, draw, together):
    hits = 0
    for _ in range(TRIES):
        t = draw(rng, (COLUMNS, SHIFTS + 1))
        ref = t if together else t[:, 1:]
        z = (t - ref.mean(axis=1, keepdims=True)) / ref.std(axis=1, ddof=1, keepdims=True)
        hits += z[:, 0].max() > z[:, 1:].max()
    return hits / TRIES


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for name, draw in (("normal", lambda r, s: r.normal(size=s)), ("chi2 1 df", lambda r, s: r.chisquare(1, s)), ("chi2 5 df", lambda r, s: r.chisquare(5, s))):
        print(name, "as coded", rate(rng, draw, False), "over all 33", rate(rng, draw, True), "nominal", round(1 / 33, 3))
