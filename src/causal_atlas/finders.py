"""The finders: a swarm of small plain-code members, each holding one kind of judgement, that read the early years of a table and post proposals to one board; and the steward that chooses which rows go to the referee. docs/plan-finders-and-referee.md, Stage A2; decision 0057: no model calls.
Finding is free and nothing here is a test. A member ranks what it found by its lift: how far a proposal stands, in the places where it stands best, above the best the member finds with the outcome moved round to other years. The whole search is repeated at every other alignment, so a member that chooses more (places, signs, which series to gather) or tries more is not ranked higher for it. A member whose proposal names a second series (two together, a sign that turns on a state) ranks what that adds beyond the plain line through the first, so that a series with no part in a link is not carried in on the back of one that has. The referee alone says what holds, on years no member saw."""
import warnings
from itertools import combinations

import numpy as np

from causal_atlas import referee as rf

SENT = 40  # rows a world sends to the referee
QUIET = 3  # other alignments start this many years from the true one: an input's memory reaches a year or two
MOST = 12  # rows a member posts for an outcome
LEVELS = (0.8, 0.2)  # the share of an input's own past below a hinge
TAILS = (0.9, 0.1)  # and below a tail event, in an input or an outcome
SEEDS = 12  # the series a board-reading pair member starts from, an outcome
GATHER = (5, 10, 20)  # how many weak series a mode is gathered from
MODES = 3  # shared components of the block of series that differ by place
ORDER = ("slope", "shape", "extremes", "pairs", "modes")  # the families, in the order they take turns
SHARE = SENT // len(ORDER)  # rows each family may send by turn; what is left goes by agreement, then lift
FLOOR = 3.0  # the lift a row needs to be sent at all: three of its own spreads above the best the member finds at other alignments (decision 0062). Fewer rows sent lower the referee's bar
FORM = "mean"  # the comparable form the members read


def view(values, group, first, outcomes, allowed=None):
    """What a member may see: the years before `first`, each series in its comparable form, the groups of places, and which series are outcomes. `allowed`, where given, is a yes or no for each outcome (row) and series (column): the series a row for that outcome may name (decision 0063: only series outside the outcome's own data set)."""
    v = np.array(values[:, :, :first], float)
    group = np.asarray(group)
    groups = np.unique(group)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        common = ~(np.nanmax(np.nanstd(v, axis=1), axis=1) > 1e-9 * np.nanstd(v, axis=(1, 2)))  # the same in every place
    member = np.array([group == g for g in groups]) * 1.0
    return {"values": v, "comp": rf.comparable(v, FORM), "group": group, "groups": groups, "member": member, "size": member.sum(axis=1), "first": first,
            "outcomes": [int(o) for o in outcomes], "common": common, "shifts": tuple(range(QUIET, first - rf.WARM - QUIET + 1)), "cache": {}, "allowed": None if allowed is None else np.asarray(allowed, bool)}


def residual(v, o, event=None):
    """What an outcome's own history leaves, in the years the members see: the referee's own baselines and errors, run on those years alone."""
    key = ("residual", o, event)
    if key not in v["cache"]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)  # a place with no past yet
            v["cache"][key] = np.nan_to_num(rf.outcome(v["values"][o], v["group"], v["first"] - 1, event)["past"][0][0])
    return v["cache"][key]


def level(c, q):
    """rf._level, the same numbers, by one sort a year in place of a search a series: for each year, the level that the share q of the series' own earlier values lie below."""
    out = np.full(c.shape, np.nan)
    for t in range(2 * rf.MIN_PAST, c.shape[-1]):
        s = np.sort(c[..., :t], axis=-1)  # what is missing goes last
        n = np.isfinite(s).sum(axis=-1)
        at = q * (np.maximum(n, 1) - 1)
        lo = np.floor(at).astype(int)
        hi = np.minimum(lo + 1, np.maximum(n, 1) - 1)
        a, b = np.take_along_axis(s, lo[..., None], -1)[..., 0], np.take_along_axis(s, hi[..., None], -1)[..., 0]
        out[..., t] = np.where(n > 0, a + (b - a) * (at - lo), np.nan)
    return out


def lagged(v, form="slope", lag=1, q=None):
    """Every series as a term of one form, built as the referee builds it, over the years a residual has: series by places by years. Zero where a term has nothing to say."""
    key = (form, lag, q)
    if key not in v["cache"]:
        comp = v["comp"]
        if form == "slope":
            z = rf._lag(comp, lag)
        else:
            lv = level(comp, q)
            hit = np.where(np.isfinite(comp) & np.isfinite(lv), (comp > lv) if q >= 0.5 else (comp < lv), False)
            side = 1.0 if q >= 0.5 else -1.0
            z = rf._lag(np.where(hit, side * (comp - lv) if form == "hinge" else 1.0, np.where(np.isfinite(lv) & np.isfinite(comp), 0.0, np.nan)), lag)
        v["cache"][key] = np.nan_to_num(z[:, :, rf.WARM:])
    return v["cache"][key]


def beyond(z, parts):
    """What a term says beyond its parts: in each place, the term less its best fit on one or two plainer terms."""
    x = parts[0]
    sxx, sxz = (x * x).sum(axis=2), (x * z).sum(axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        one = np.nan_to_num(sxz / sxx, posinf=0.0, neginf=0.0)
        if len(parts) == 1:
            return z - one[..., None] * x
        y = parts[1]
        syy, sxy, syz = (y * y).sum(axis=2), (x * y).sum(axis=2), (y * z).sum(axis=2)
        det = sxx * syy - sxy * sxy
        two = det > 1e-9 * sxx * syy
        bx = np.where(two, (syy * sxz - sxy * syz) / det, one)
        by = np.where(two, (sxx * syz - sxy * sxz) / det, 0.0)
    return z - np.nan_to_num(bx)[..., None] * x - np.nan_to_num(by)[..., None] * y


def sums(z, r, shifts):
    """For each term, each alignment (the true one first, then the outcome moved round by each of `shifts` years) and each place: the sum of term times residual. And each term's and the residual's sums of squares by place."""
    rs = np.stack([r] + [np.roll(r, k, axis=1) for k in shifts])
    a = np.matmul(z.transpose(1, 0, 2), rs.transpose(1, 2, 0)).transpose(1, 2, 0)
    return a, (z * z).sum(axis=2), (r * r).sum(axis=1)


def _run(ag, cg, bg, size):
    least = min(rf.GROUPS, ag.shape[2])
    with np.errstate(divide="ignore", invalid="ignore"):
        each = np.nan_to_num(ag / np.sqrt(bg * cg)[:, None, :], nan=-np.inf, posinf=-np.inf)
        order = np.argsort(-each, axis=2, kind="stable")
        under = np.cumsum(bg[order], axis=2) * np.cumsum(np.take_along_axis(np.broadcast_to(cg[:, None, :], ag.shape), order, 2), axis=2)
        stand = np.cumsum(np.take_along_axis(ag, order, 2), axis=2) / np.sqrt(under) * np.sqrt(np.cumsum(size[order], axis=2))
    stand[~np.isfinite(stand)] = -np.inf
    stand[:, :, : least - 1] = -np.inf
    k = np.argmax(stand, axis=2)
    return np.take_along_axis(stand, k[..., None], 2)[..., 0], order, k


def scan(ag, cg, bg, size, both=True):
    """Where a term goes with the residual. `ag` is, for each term, alignment and group of places, how far the term goes with the residual there. The groups are put in order, and the run of them from the top, of at least rf.GROUPS, is taken that stands furthest above nothing: its correlation times the root of its places. With `both` the same is done the other way up and the better kept.
    Returns that standing for each term and alignment; and for each term at the true alignment the order of the groups, how many are taken, and which way up."""
    stand, order, k = _run(ag, cg, bg, size)
    way = np.ones(stand.shape)
    if both:
        down = _run(-ag, cg, bg, size)
        pick = down[0] > stand
        stand, order, k, way = np.where(pick, down[0], stand), np.where(pick[..., None], down[1], order), np.where(pick, down[2], k), np.where(pick, -1.0, 1.0)
    return stand, order[:, 0], k[:, 0], way[:, 0]


def lift(stand):
    """How far each term stands at the true alignment above the best of the member's terms at a typical other alignment. Each term is first put in units of its own spread over the other alignments (for an other alignment, the spread over the rest), so that a series with a long memory does not set the scale for all."""
    true, other = stand[:, 0], stand[:, 1:]
    n = other.shape[1]
    if n < 3 or not np.isfinite(stand).any():
        return np.full(len(stand), -np.inf)
    s, ss = other.sum(axis=1, keepdims=True), (other * other).sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (true - s[:, 0] / n) / np.sqrt(np.maximum(ss[:, 0] / n - (s[:, 0] / n) ** 2, 0))
        m = (s - other) / (n - 1)
        rest = (other - m) / np.sqrt(np.maximum((ss - other * other) / (n - 1) - m * m, 0))
    ok = np.isfinite(z) & np.isfinite(rest).all(axis=1)
    if not ok.any():
        return np.full(len(stand), -np.inf)
    return np.where(ok, z - rest[ok].max(axis=0).mean(), -np.inf)


def _where(v, order, k):
    """The places of the groups a scan took; all places when it took every group."""
    chosen = order[: k + 1]
    return "all" if len(chosen) == len(v["groups"]) else np.isin(v["group"], v["groups"][chosen])


def _post(v, o, z, names, describe, family, member, rnd, flip=False, event=None, tag=None):
    """A member's rows for one outcome, from a stack of terms: the MOST with the highest lift, each with the places its scan took. `names` are the series a term names; a term that names the outcome, or a series a row for this outcome may not name, is not posted nor counted among the member's terms.
    With `flip` each place goes its own way: what is scanned is how much further the places of a group go each their own way than all one way, less what that comes to at the other alignments."""
    ok = v["allowed"]
    use = np.flatnonzero([o not in n for n in names] if ok is None else [o not in n and all(ok[o, s] for s in n) for n in names])
    if not len(use):
        return []
    a, c, b = sums(z[use], residual(v, o, event), v["shifts"])
    ag = a @ v["member"].T
    if flip:
        ag = np.abs(a) @ v["member"].T - np.abs(ag)
        ag = ag - ag[:, 1:].mean(axis=1, keepdims=True)
    stand, order, k, way = scan(ag, c @ v["member"].T, b @ v["member"].T, v["size"], both=not flip)
    up = lift(stand)
    rows = []
    for i in np.argsort(-up, kind="stable")[:MOST]:
        if not np.isfinite(up[i]):
            break
        j = int(use[i])
        rows.append({"outcome": o, "where": _where(v, order[i], k[i]), "event": event, "family": family, "member": member, "round": rnd, "lift": float(up[i]), "stand": float(stand[i, 0]),
                     "names": frozenset(int(s) for s in names[j]), "tag": None if tag is None else tag[j], **describe(j, way[i], a[i, 0])})
    return rows


def _single(v):
    return [(s,) for s in range(len(v["comp"]))]


def slope(v, o, board, lag=1):
    """The reference: what own history leaves, on each series that many years before."""
    return _post(v, o, lagged(v, "slope", lag), _single(v), lambda i, way, a: {"inputs": [(i, lag)], "form": "slope"}, "slope", f"lag {lag}", 1)


def hinge(v, o, board, q=0.8):
    """Only beyond a level of the series' own past."""
    return _post(v, o, lagged(v, "hinge", 1, q), _single(v), lambda i, way, a: {"inputs": [(i, 1)], "form": "hinge", "level": q}, "shape", f"hinge {q}", 1)


def by_place(v, o, board):
    """A sign that differs by place: each place goes its own way, and the proposal names which way each went in the early years."""
    return _post(v, o, lagged(v, "slope", 1), _single(v), lambda i, way, a: {"inputs": [(i, 1)], "form": "by_group", "groups": (a > 0).astype(int)}, "shape", "sign by place", 1, flip=True)


def by_state(v, o, board):
    """A sign that turns on which side of its own past a series common to all places stood the year before: what that says beyond the plain line."""
    key = ("by_state",)
    if key not in v["cache"]:
        z = lagged(v, "slope", 1)
        states = [int(q) for q in np.flatnonzero(v["common"])]
        side = rf._lag(v["comp"][states], 1)[:, :, rf.WARM:]
        side = np.where(side > 0, 1.0, np.where(side <= 0, -1.0, 0.0))
        names = [(s, q) for s in range(len(z)) for q in states if s != q]
        terms = np.array([z[s] * side[states.index(q)] for s, q in names]).reshape(len(names), *z.shape[1:])
        v["cache"][key] = names, beyond(terms, [z[[s for s, _ in names]]]) if names else terms
    names, terms = v["cache"][key]
    if not names:
        return []
    return _post(v, o, terms, names, lambda i, way, a: {"inputs": [(names[i][0], 1)], "form": "by_state", "state": (names[i][1], 1)}, "shape", "sign by state", 1)


def tail(v, o, board, q=0.9, event=None):
    """A tail event in a series the year before; with `event`, against the chance of a tail event in the outcome."""
    member = f"tail {q}" + ("" if event is None else f" to event {event}")
    return _post(v, o, lagged(v, "tail", 1, q), _single(v), lambda i, way, a: {"inputs": [(i, 1)], "form": "tail", "level": q}, "extremes", member, 1, event=event)


def _products(v):
    """Every pair of series a year before, multiplied: what the product says beyond the plain lines through the two."""
    key = ("products",)
    if key not in v["cache"]:
        z = lagged(v, "slope", 1)
        names = list(combinations(range(len(z)), 2))
        i, j = (np.array(x) for x in zip(*names))
        v["cache"][key] = names, beyond(z[i] * z[j], [z[i], z[j]])
    return v["cache"][key]


def pairs(v, o, board):
    """Two together: every pair of series, as a product. Tried directly, which this number of series allows."""
    names, z = _products(v)
    return _post(v, o, z, names, lambda i, way, a: {"inputs": [(names[i][0], 1), (names[i][1], 1)], "form": "product"}, "pairs", "every pair", 1)


def pairs_from_board(v, o, board):
    """Two together, starting from the board: the pairs among the series that single-series members put forward for this outcome, which are few enough to stand out among themselves."""
    seen = []
    for r in sorted((r for r in board if r["outcome"] == o and r["round"] == 1 and r["family"] in ("slope", "shape", "extremes")), key=lambda r: -r["lift"]):
        seen += [s for s, _ in r["inputs"] if s not in seen]
    mine = list(combinations(sorted(seen[:SEEDS]), 2))  # only these products are built, so the member runs on a table too wide for every pair
    if len(mine) < 2:
        return []
    z = lagged(v, "slope", 1)
    i, j = (np.array(x) for x in zip(*mine))
    return _post(v, o, beyond(z[i] * z[j], [z[i], z[j]]), mine, lambda i, way, a: {"inputs": [(mine[i][0], 1), (mine[i][1], 1)], "form": "product"}, "pairs", "pairs from the board", 2)


def components(v, o, board):
    """Shared modes: the main components of the block of series that differ by place, each as one term. Nothing about the outcome goes into the weights."""
    ok = v["allowed"]
    block = [int(s) for s in np.flatnonzero(~v["common"]) if s != o and (ok is None or ok[o, s])]
    if len(block) < 2:
        return []
    key = ("components", o)
    if key not in v["cache"]:
        x = np.nan_to_num(v["comp"][block][:, :, rf.MIN_PAST:]).reshape(len(block), -1)
        v["cache"][key] = np.linalg.eigh(x @ x.T)[1][:, ::-1][:, :MODES].T
    w = v["cache"][key]
    z = np.einsum("ms,spt->mpt", w, lagged(v, "slope", 1)[block]) / np.sqrt((w * w).sum(axis=1))[:, None, None]
    return _post(v, o, z, [tuple(block)] * len(w), lambda i, way, a: {"inputs": [(s, 1) for s in block], "form": "mode", "weights": [float(x) for x in w[i]]}, "modes", "components", 1,
                 tag=[f"component {i + 1}" for i in range(len(w))])


def gathered(v, o, board):
    """Many weak: the series that stand highest for this outcome on the plain line, gathered into one term with their signs. The choosing and gathering are repeated at every other alignment, so that having chosen the series does not count for the term."""
    z = lagged(v, "slope", 1)
    r = residual(v, o)
    a, c, b = sums(z, r, v["shifts"])
    bg = b @ v["member"].T
    stand = scan(a @ v["member"].T, c @ v["member"].T, bg, v["size"])[0]
    stand[o] = -np.inf
    ok = v["allowed"]
    if ok is not None:
        stand[~ok[o]] = -np.inf
    most = len(z) - 1 if ok is None else int(ok[o].sum()) - int(ok[o, o])  # the outcome itself is never gathered
    rs = np.stack([r] + [np.roll(r, k, axis=1) for k in v["shifts"]])
    rows = []
    for m in sorted({min(m, most) for m in GATHER} - {0}):
        top = np.argsort(-stand, axis=0, kind="stable")[:m]  # the m series, at each alignment; never the outcome, which stands last
        sign = np.where(np.take_along_axis(a.sum(axis=2), top, 0) >= 0, 1.0, -1.0)
        st = []
        for k in range(len(rs)):  # each alignment's own term, scanned against the outcome at that alignment
            zk = (sign[:, k, None, None] * z[top[:, k]]).sum(axis=0) / np.sqrt(m)
            st.append(scan(((zk * rs[k]).sum(axis=1) @ v["member"].T)[None, None], ((zk * zk).sum(axis=1) @ v["member"].T)[None], bg, v["size"]))
        up = lift(np.array([[s[0][0, 0] for s in st]]))[0]
        if not np.isfinite(up):
            continue
        series = [int(s) for s in top[:, 0]]
        rows.append({"outcome": o, "where": _where(v, st[0][1][0], st[0][2][0]), "event": None, "family": "modes", "member": f"gathered {m}", "round": 2, "lift": float(up), "stand": float(st[0][0][0, 0]),
                     "names": frozenset(series), "tag": None, "inputs": [(s, 1) for s in series], "form": "mode", "weights": [float(x) for x in sign[:, 0]]})
    return rows


MEMBERS = [  # in the order they run; the second round reads the board
    slope, lambda v, o, b: slope(v, o, b, 2),
    lambda v, o, b: hinge(v, o, b, LEVELS[0]), lambda v, o, b: hinge(v, o, b, LEVELS[1]), by_place, by_state,
    lambda v, o, b: tail(v, o, b, TAILS[0]), lambda v, o, b: tail(v, o, b, TAILS[1]),
    lambda v, o, b: tail(v, o, b, TAILS[0], TAILS[0]), lambda v, o, b: tail(v, o, b, TAILS[1], TAILS[0]), lambda v, o, b: tail(v, o, b, TAILS[0], TAILS[1]), lambda v, o, b: tail(v, o, b, TAILS[1], TAILS[1]),
    pairs, components,
    pairs_from_board, gathered,
]


def swarm(v, members=None):
    """Every member, in a fixed order, for every outcome: the board. Same table, same board, every time. `members`: fewer than all, for a table too wide for the every-pair member."""
    board = []
    for member in MEMBERS if members is None else members:
        for o in v["outcomes"]:
            board += member(v, o, board)
    return board


def ranked(board, floor=FLOOR, families=ORDER, rounds=2):
    """The board as the steward reads it. A family's rows that name the same series for the same outcome count as one, the one with the highest lift standing for them. Returns those rows by key (outcome, series named, family, tag); for each outcome and set of series, the families that arrived at it; and each family's keys, best first."""
    best, agree = {}, {}
    for r in board:
        if r["round"] > rounds or r["family"] not in families or not r["lift"] >= floor:
            continue
        agree.setdefault((r["outcome"], r["names"]), set()).add(r["family"])
        key = (r["outcome"], r["names"], r["family"], r["tag"])
        if key not in best or r["lift"] > best[key]["lift"]:
            best[key] = r
    return best, agree, {f: sorted((k for k in best if k[2] == f), key=lambda k: -best[k]["lift"]) for f in families}


def steward(board, sent=SENT, share=SHARE, floor=FLOOR, families=ORDER, rounds=2):
    """Which rows go to the referee. Each family in turn sends its best not yet sent, up to `share` each; what is left of `sent` goes to the rows whose series most families arrived at separately, then by lift. Agreement decides the order, never the verdict.
    Returns the rows, each with the families that named its series for its outcome and how it was chosen."""
    best, agree, queue = ranked(board, floor, families, rounds)
    out = []
    for turn in range(share):
        for f in families:
            if len(queue[f]) > turn and len(out) < sent:
                out.append((queue[f][turn], f))
    taken = {k for k, _ in out}
    rest = sorted((k for k in best if k not in taken), key=lambda k: (-len(agree[k[:2]]), -best[k]["lift"]))
    out += [(k, "agreement") for k in rest[: sent - len(out)]]
    return [{**best[k], "families": sorted(agree[k[:2]]), "chosen": how} for k, how in out]


def proposal(row):
    """A row of the board as the referee takes it."""
    return rf.proposal(row["outcome"], row["inputs"], row["form"], row["where"], level=row.get("level"), groups=row.get("groups"), state=row.get("state"), weights=row.get("weights"), event=row["event"],
                       by=f"{row['family']}: {row['member']}")
