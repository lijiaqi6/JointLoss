r"""Synthetic smoke test of the BPS harness (IGE/bps_reconciliation, 2026-10-18). Results: HARNESS.md.

A simple monthly couple panel with KNOWN wage-shock variances is generated in the schema of sim_panel_writer.py,
written to BPS's layout by the writer (with and without measurement error), and run through bps_on_sim.do.

Wage DGP (annual components, the hourly wage is constant within a calendar year):
    log w_jy = mu_j(educ, age) + a_j + p_jy + u_jy,  p_jy = p_j,y-1 + e_jy,  j = husband (1), wife (2)
    (e_1, e_2) ~ N(0, [[0.015, 0.003], [0.003, 0.020]]) per year = BPS's sigma2_v1, sigma2_v2, sigma_v1v2 (BPS's v is
         the annual permanent innovation; a two-year difference carries two of them), rho 0.173
    (u_1, u_2) ~ N(0, [[0.030, 0.006], [0.006, 0.020]]) iid per year: sigma2_u1 = 0.030, sigma2_u2 = 0.020,
         sigma_u1u2 = 0.006 (rho 0.245)
Hours (annual, spread evenly over worked months): log H1 = log 2100 + 0.5 u1 + 0.1 u2 - 0.05 p1 - 0.10 p2 + f1 + n1,
    log H2 = log 1500 + 0.9 u2 + 0.2 u1 + 0.4 p2 - 0.3 p1 + f2 + n2 (f fixed effects sd 0.15, n iid sd 0.10).
    15% of wives never work, 4% of wife-years not worked. Job losses: husbands 2.5% a year, wives 2% a year, plus a
    wife displaced in the husband's month with probability 0.10; spells of 1-6 months (10%: 13-18 months, so some
    husbands have a calendar year with zero hours), status 3 (70%) or 2 (30%) during the spell, wage unchanged.
Consumption (monthly): log C = 7.4 + 0.35 p1 + 0.15 p2 - 0.10 u1 - 0.03 u2 + 0.1 (educ_h - 2) + c_fe - 0.05 in spell months.
Assets: kappa * (age_h - 22)/10 * 40,000 * exp(p1), kappa lognormal. Separation 0.8% a year; 10% SEO-type couples.

Usage: python smoke_sim_dgp.py <outdir> [n_couples]   -> writes smoke_*.dta, smoke_truth.json, smoke_me_info.csv
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sim_panel_writer as spw  # noqa: E402

# BPS's sigma2_v is the ANNUAL permanent variance: variance_estimation.do fits E(dw_t^2) = p_t + p_{t-1} + t_t + t_{t-2}
# (two annual permanent innovations in a two-year difference), so the truth for s_v is the annual e variance.
TRUTH = {"s_u1": 0.030, "s_v1": 0.015, "s_u2": 0.020, "s_v2": 0.020, "c_u1u2": 0.006, "c_v1v2": 0.003}
TRUTH["rho_u1u2"] = TRUTH["c_u1u2"] / np.sqrt(TRUTH["s_u1"] * TRUTH["s_u2"])
TRUTH["rho_v1v2"] = TRUTH["c_v1v2"] / np.sqrt(TRUTH["s_v1"] * TRUTH["s_v2"])
Y0, Y1 = 1995, 2009


def simulate(n=10000, seed=2016):
    rng = np.random.default_rng(seed)
    years = np.arange(Y0, Y1 + 1)
    ny = len(years)
    age_h98 = rng.uniform(27, 55, n)
    age_w98 = np.clip(age_h98 - 2 + rng.normal(0, 2.5, n), 20, None)
    race_h = rng.choice([1, 2, 3], n, p=[0.75, 0.20, 0.05])
    race_w = np.where(rng.random(n) < 0.95, race_h, rng.choice([1, 2, 3], n))
    educ_h = rng.choice([1, 2, 3], n, p=[0.12, 0.35, 0.53])
    educ_w = np.where(rng.random(n) < 0.6, educ_h, rng.choice([1, 2, 3], n, p=[0.10, 0.35, 0.55]))
    state = rng.integers(1, 52, n)
    seo = (rng.random(n) < np.where(race_h == 2, 0.30, 0.05)).astype(int)
    kids0 = rng.choice([0, 1, 2, 3], n, p=[0.30, 0.25, 0.30, 0.15])
    birth_year = np.where(rng.random(n) < 0.10, rng.integers(Y0, Y1 + 1, n), 9999)
    mort0 = np.where(rng.random(n) < 0.6, 100000 * np.exp(rng.normal(0, 0.5, n)), 0.0)
    kappa = np.exp(rng.normal(np.log(0.8), 0.7, n))
    never_w = rng.random(n) < 0.15
    sep_year = np.where(rng.random(n) < 1 - (1 - 0.008) ** ny, rng.integers(Y0 + 1, Y1 + 1, n), 9999)
    sep_month = rng.integers(1, 13, n)

    # annual wage components
    E = rng.multivariate_normal([0, 0], [[0.015, 0.003], [0.003, 0.020]], size=(n, ny))
    U = rng.multivariate_normal([0, 0], [[0.030, 0.006], [0.006, 0.020]], size=(n, ny))
    P = np.cumsum(E, axis=1) - E[:, :1, :]              # p = 0 in the first year
    a1, a2 = rng.normal(0, 0.45, n), rng.normal(0, 0.45, n)
    f1, f2 = rng.normal(0, 0.15, n), rng.normal(0, 0.15, n)
    cfe = rng.normal(0, 0.25, n)
    n1, n2 = rng.normal(0, 0.10, (n, ny)), rng.normal(0, 0.10, (n, ny))
    wife_off = rng.random((n, ny)) < 0.04

    # monthly grid
    T = ny * 12
    yr = np.repeat(years, 12)
    mo = np.tile(np.arange(1, 13), ny)
    t_idx = np.arange(T)
    age_h = age_h98[:, None] + (yr[None, :] - 1998) + (mo[None, :] - 1) / 12
    age_w = age_w98[:, None] + (yr[None, :] - 1998) + (mo[None, :] - 1) / 12
    yi = (yr - Y0)[None, :].repeat(n, 0)

    def spells(rate, extra=None):
        out = np.zeros((n, T), bool)
        start = np.zeros((n, T), bool)
        stat = np.ones((n, T), int)
        ev = rng.random((n, ny)) < rate
        if extra is not None:
            ev = ev | extra
        for i, k in zip(*np.nonzero(ev)):
            m0 = k * 12 + rng.integers(0, 12)
            ln = rng.integers(13, 19) if rng.random() < 0.10 else rng.integers(1, 7)
            out[i, m0:m0 + ln] = True
            start[i, m0] = True
            stat[i, m0:m0 + ln] = 3 if rng.random() < 0.7 else 2
        return out, start, stat

    sp_h, st_h, stat_h = spells(0.025)
    # wife: own displacements and joint ones (same month as the husband's with probability 0.10)
    sp_w, st_w, stat_w = spells(0.020)
    joint = st_h & (rng.random((n, T)) < 0.10)
    for i, m0 in zip(*np.nonzero(joint)):
        ln = rng.integers(1, 7)
        sp_w[i, m0:m0 + ln] = True
        st_w[i, m0] = True
        stat_w[i, m0:m0 + ln] = 3

    mu1 = 2.6 + 0.12 * (educ_h[:, None] - 2) + 0.03 * (age_h - 40) - 0.0006 * (age_h - 40) ** 2
    mu2 = 2.35 + 0.12 * (educ_w[:, None] - 2) + 0.02 * (age_w - 40) - 0.0005 * (age_w - 40) ** 2
    p1, p2 = P[:, :, 0][np.arange(n)[:, None], yi], P[:, :, 1][np.arange(n)[:, None], yi]
    u1, u2 = U[:, :, 0][np.arange(n)[:, None], yi], U[:, :, 1][np.arange(n)[:, None], yi]
    w1 = np.exp(mu1 + a1[:, None] + p1 + u1)
    w2 = np.exp(mu2 + a2[:, None] + p2 + u2)
    H1 = np.exp(np.log(2100) + 0.5 * u1 + 0.1 * u2 - 0.05 * p1 - 0.10 * p2 + f1[:, None]
                + n1[np.arange(n)[:, None], yi]) / 12
    H2 = np.exp(np.log(1500) + 0.9 * u2 + 0.2 * u1 + 0.4 * p2 - 0.3 * p1 + f2[:, None]
                + n2[np.arange(n)[:, None], yi]) / 12
    married = ~((yr[None, :] > sep_year[:, None]) | ((yr[None, :] == sep_year[:, None]) & (mo[None, :] >= sep_month[:, None])))
    w_works = (~never_w[:, None]) & (~wife_off[np.arange(n)[:, None], yi]) & married
    hours_h = np.where(sp_h, 0.0, H1)
    hours_w = np.where(w_works & ~sp_w, H2, 0.0)
    emp_h = np.where(sp_h, stat_h, 1)
    emp_w = np.where(~married, 0, np.where(~w_works, 6, np.where(sp_w, stat_w, 1)))
    cons = np.exp(7.4 + 0.35 * p1 + 0.15 * p2 - 0.10 * u1 - 0.03 * u2 + 0.1 * (educ_h[:, None] - 2)
                  + cfe[:, None] - 0.05 * sp_h)
    assets = kappa[:, None] * np.maximum(age_h - 22, 0) / 10 * 40000 * np.exp(p1)
    kids = kids0[:, None] + (yr[None, :] >= birth_year[:, None])
    mortgage = mort0[:, None] * np.clip(1 - (yr[None, :] - Y0) / 25, 0, 1)

    df = pd.DataFrame({
        "couple_id": np.repeat(np.arange(1, n + 1), T), "year": np.tile(yr, n), "month": np.tile(mo, n),
        "age_h": age_h.ravel(), "age_w": age_w.ravel(),
        "race_h": np.repeat(race_h, T), "race_w": np.repeat(race_w, T),
        "educ_h": np.repeat(educ_h, T), "educ_w": np.repeat(educ_w, T),
        "hours_h": hours_h.ravel(), "hours_w": hours_w.ravel(),
        "earn_h": (hours_h * w1).ravel(), "earn_w": (hours_w * w2).ravel(),
        "wage_h": w1.ravel(), "wage_w": w2.ravel(),
        "emp_h": emp_h.ravel(), "emp_w": emp_w.ravel(),
        "cons": cons.ravel(), "assets": assets.ravel(), "kids": kids.ravel(),
        "married": married.ravel().astype(int),
        "disp_h": st_h.ravel().astype(int), "disp_w": (st_w & married).ravel().astype(int),
        "seo": np.repeat(seo, T), "state": np.repeat(state, T), "mortgage": mortgage.ravel(),
    })
    return df


def main(outdir, n=10000):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    m = simulate(n)
    base = spw.to_bps_panel(m, seed=7)
    print("biennial rows", len(base), "years", sorted(base["year"].unique()))
    # (A) Bound et al. shares (BPS's calibration), no gross errors; calibration cells: married, husband 30-57
    pA, infoA = spw.add_measurement_error(base, seed=11)
    spw.write_bps_dta(pA, out / "smoke_me.dta")
    # (B) the two-component mixture: + gross errors on 1% of observations per variable, sd 0.7 in logs
    pB, infoB = spw.add_measurement_error(base, gross_rate=0.01, gross_sd=0.7, seed=11)
    spw.write_bps_dta(pB, out / "smoke_mix.dta")
    # (C) no measurement error at all
    spw.write_bps_dta(base, out / "smoke_noME.dta")
    pd.concat([infoA.assign(panel="me"), infoB.assign(panel="mix")]).to_csv(out / "smoke_me_info.csv", index=False)
    (out / "smoke_truth.json").write_text(json.dumps(TRUTH, indent=1))
    # direct check of the DGP on the panel before measurement error: BPS-style raw wage-growth moments
    b = base[(base["marit"] == 1) & (base["seo"] == 0)].sort_values(["person", "year"]).copy()
    b["lw"] = np.log(b["ly"] / b["hours"].where(b["hours"] > 0)) - np.log(b["year"].map(
        {y - 1900: v for y, v in spw.bps_price_index().items()}))
    b["gap"] = b.groupby("person")["year"].diff()
    b["dlw"] = (b["lw"] - b.groupby("person")["lw"].shift(1)).where(b["gap"] == 2)
    b["dlw"] = b["dlw"] - b.groupby("year")["dlw"].transform("mean")
    b["dlw_l"] = b.groupby("person")["dlw"].shift(1).where(b["gap"] == 2)
    ok = b[["dlw", "dlw_l"]].notna().all(axis=1)
    print("panel before ME, husbands: var(dw) =", round(float(b["dlw"].var()), 4),
          "(DGP: 2 s_u1 + 2 s_v1 = 0.090, + age-profile dispersion); E(dw dw_-2) =",
          round(float((b.loc[ok, "dlw"] * b.loc[ok, "dlw_l"]).mean()), 4), "(DGP: -s_u1 = -0.030)")
    return base


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10000)
