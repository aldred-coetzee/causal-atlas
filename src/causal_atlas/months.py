"""Reading by month: the season step, the month members, the whole-year draw and the settings counted in months, so that the finders and the referee as counted on yearly tables can read a monthly table at its own step. docs/reading/reading-by-month.md; nothing here changes a yearly read.

A monthly table is read on its months with the season out (each value less the mean of the same calendar month in earlier years, from earlier dates alone); the finders' members look one to six months back, over windows of months, and at tail events three and six months back; the referee's settings counted in years are made months, and its bar draws whole years of months again, not single months. Month 0 of a table is a January."""
import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

YEAR = 12
MONTHLY = {"MIN_PAST": 24, "WARM": 24, "SPAN": 36, "OWN": 120.0, "YEARS": 120}  # the referee's settings counted in years, made two, three or ten years of months
READ = {**MONTHLY, "LAZY": True}  # and, for a read, the referee's errors made again when asked for rather than kept a scored step at a time: the same numbers; one linked world of 120 places by 600 months peaked at 0.5 GB read so, 4.9 to 5.3 GB with the errors kept, most of it in the labels, where each input of a passed mode is made an outcome
QUIET = 12  # the finders' other alignments start a year of months from the true one
LAGS = (1, 2, 3, 4, 5, 6)  # months before, each a member of the slope family
WINDOWS = ((1, 2, 3), (4, 5, 6), (1, 2, 3, 4, 5, 6))  # a series over several months before, as one term
TAIL_LAGS = (3, 6)  # months before, for the two tail members beyond the counted one month


def _before(a):
    c = np.cumsum(a, axis=-1)
    return np.concatenate([np.zeros_like(c[..., :1]), c[..., :-1]], axis=-1)


def season_out(values, least=2):
    """Each value less the mean of the same calendar month in all earlier years; nothing where fewer than `least` earlier years have that month. Only earlier dates go in, so a value may be used at its own date."""
    v = np.asarray(values, float)
    out = np.full(v.shape, np.nan)
    for m in range(YEAR):
        x = v[..., m::YEAR]
        ok = np.isfinite(x)
        n, s = _before(ok * 1.0), _before(np.where(ok, x, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            out[..., m::YEAR] = np.where(n >= least, x - s / n, np.nan)
    return out


def whole_years(first, block=YEAR):
    """A draw for the referee (rf.judge's `draw`): groups drawn as the referee draws them, and the scored months drawn a whole year at a time, every month of a drawn year taken together and as often as its year. `first`: the first scored month."""

    def draws(groups, steps, n, seed):
        rng = np.random.default_rng(seed)
        year = (first + np.arange(steps)) // block
        year = year - year[0]
        k = int(year[-1]) + 1
        cg = rng.multinomial(groups, np.full(groups, 1 / groups), n).astype(float)
        return cg, rng.multinomial(k, np.full(k, 1 / k), n).astype(float)[:, year]

    return draws


def window(v, o, board, lags):
    """A series over several months before, as one term: the sum of it at each of `lags`, scaled."""
    z = sum(fd.lagged(v, "slope", k) for k in lags) / np.sqrt(len(lags))
    return fd._post(v, o, z, fd._single(v), lambda i, way, a: {"inputs": [(i, k) for k in lags], "form": "mode"}, "slope", f"months {lags[0]} to {lags[-1]}", 1)


def tail_at(v, o, board, q, lag):
    """A tail event in a series `lag` months before."""
    z = fd.lagged(v, "tail", 1, q)
    z = np.concatenate([np.zeros(z.shape[:2] + (lag - 1,)), z[:, :, : z.shape[2] - (lag - 1)]], axis=2)
    return fd._post(v, o, z, fd._single(v), lambda i, way, a: {"inputs": [(i, lag)], "form": "tail", "level": q}, "extremes", f"tail {q} month {lag}", 1)


def members(lags=LAGS, windows=WINDOWS, tails=TAIL_LAGS):
    """The members as counted, with the plain line at each of `lags` months before in place of one and two, the windows, and the two tail members at `tails` months before as well."""
    first = [(lambda v, o, b, k=k: fd.slope(v, o, b, k)) for k in lags] + [(lambda v, o, b, w=w: window(v, o, b, w)) for w in windows]
    extra = [(lambda v, o, b, q=q, k=k: tail_at(v, o, b, q, k)) for q in fd.TAILS for k in tails]
    return first + fd.MEMBERS[2:12] + extra + fd.MEMBERS[12:]


def read(values, group, first, outcomes, allowed=None, seed=0, labels=True, members_=None):
    """A monthly table read: the season step on every series, the finders on the months before `first` with the month members and settings, the steward as counted, and the referee on the rest with the month settings and the whole-year draw. `first` a whole number of years. Returns the board, the rows sent and the judgement."""
    assert first % YEAR == 0, "the scored part begins in a January"
    d = season_out(values)
    v = fd.view(d, group, first, outcomes, allowed, settings=READ, quiet=QUIET)
    board = fd.swarm(v, members() if members_ is None else members_)
    rows = fd.steward(board)
    del v  # the finders' stores are not needed by the referee
    res = rf.judge(d, group, first, [fd.proposal(r) for r in rows], seed=seed, labels=labels, draw=whole_years(first), settings=READ, level_fn=fd.level)
    return board, rows, res
