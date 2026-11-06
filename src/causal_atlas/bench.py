"""The test framework's scorecard: one way to read any method's claims against a world's truth. See results/framework-stage-1.md."""
import math

from causal_atlas import screen as c


def claims(t, names, gaps=c.GAPS, widths=c.WIDTHS):
    """One form's T table as ranked claims: input, gap, width, strength, and whether the gate named it. Named leads come first, as the gate stepped down."""
    leads, top, z = c.gate(t)
    per = len(gaps) * len(widths)
    out = []
    for rank, col in enumerate(top):
        out.append(dict(input=names[col // per], gap=gaps[(col % per) // len(widths)], width=widths[col % len(widths)], strength=z[rank], lead=rank < len(leads)))
    return out


def read_world(found, true):
    """A ranked list against the truth. Found means the first lead is truly linked; R2's any-lead reading is beside."""
    leads = [x for x in found if x["lead"]]
    return dict(named=bool(leads), first_true=bool(leads) and leads[0]["input"] in true, any_true=any(x["input"] in true for x in leads), top_true=any(x["input"] in true for x in found))


def wilson(k, n, z=1.96):
    """The 95% Wilson interval of k in n."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, mid - half), min(1.0, mid + half))


def tally(planted, nulls):
    """Counts for one method and form, from read_world rows."""
    return dict(planted=len(planted), first_true=sum(x["first_true"] for x in planted), any_true=sum(x["any_true"] for x in planted), top_true=sum(x["top_true"] for x in planted),
                nulls=len(nulls), null_named=sum(x["named"] for x in nulls))


def choose_form(by_form, quiet_most=2):
    """Most planted worlds with the first lead true, among forms quiet enough; ties to fewer named on nulls, then the order given. None if no form is quiet. Pure."""
    ok = [(-v["first_true"], v["null_named"], i, f) for i, (f, v) in enumerate(by_form.items()) if v["null_named"] <= quiet_most]
    return min(ok)[3] if ok else None


def step_two(v, least=8, quiet_most=2):
    """Go on to fresh seeds only if the chosen form clears the development line. Pure."""
    return v["first_true"] >= least and v["null_named"] <= quiet_most


def marks(rows, instrument=0.8, recovery=0.5, quiet_most=3):
    """Step 3's three marks. rows: planted with ceiling (bool), heard (bool), first_true (bool); nulls with named (bool). Pure."""
    planted, nulls = rows["planted"], rows["nulls"]
    e = [x for x in planted if x["ceiling"]]
    heard, found, named = sum(x["heard"] for x in e), sum(x["first_true"] for x in e), sum(x["named"] for x in nulls)
    return dict(E=len(e), outside=len(planted) - len(e), heard=heard, found=found, found_ci=wilson(found, len(e)), named=named, nulls=len(nulls), named_ci=wilson(named, len(nulls)),
                instrument=bool(e) and heard >= instrument * len(e), recovery=bool(e) and found >= recovery * len(e), quiet=named <= quiet_most)
