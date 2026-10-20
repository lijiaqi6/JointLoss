r"""LaTeX tables for Paper B Section 8 from the final hypothesis lattice (chain x4, R = 20; model/output/final_x4/,
copied from model/hpc_runs/ on 2026-10-19). Writes paperB_age_profile/tab_model_hyp.tex (the hypothesis tests),
tab_model_lattice.tex (the ten models), tab_model_estimates.tex (selected model E), tab_model_fit.tex and
tab_model_cf.tex (counterfactuals of model E, output/postestimation_Lx4_E.json)."""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402

DEST = HERE.parent / "paperB_age_profile"
F = HERE / "output" / "final_x4"
L = json.load(open(F / "lattice.json"))
H4 = json.load(open(F / "h4_seeds.json"))
D = json.load(open(HERE / "output" / "data_moments.json"))
MD, SD = dict(zip(core.MOMENT_NAMES, D["m"])), dict(zip(core.MOMENT_NAMES, D["sd"]))
PE = json.load(open(HERE / "output" / "postestimation_Lx4_E.json"))
SEL = "E"


def est(name):
    E = json.load(open(F / f"estimates_{name}.json"))
    m = name[0]
    return E[m]


def est_lat(name):
    """The lattice's estimates: model E at step 4 (estimates_E_lattice.json) once a later step is selected."""
    return est("E_lattice") if name == "E" and (F / "estimates_E_lattice.json").exists() else est(name)


def star(p):
    return "^{***}" if p < 0.01 else "^{**}" if p < 0.05 else "^{*}" if p < 0.10 else ""


def coef(v, s, dec=3, stars=True):
    p = 2 * (1 - norm.cdf(abs(v) / s)) if s and s > 0 else 1.0
    return f"${v:.{dec}f}{star(p) if stars else ''}$ ({s:.{dec}f})"


def num(v, dec=3):
    return f"${v:.{dec}f}$"


def table(name, caption, label, align, head, rows, notes):
    T = [r"\begin{table}[!htbp]", r"\centering", r"\caption{" + caption + "}", r"\label{" + label + "}",
         r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%", r"\begin{tabular}{" + align + "}",
         r"\toprule", head, r"\midrule"] + rows + [
        r"\bottomrule", r"\end{tabular}}", r"\par\smallskip",
        r"\begin{minipage}{\textwidth}\footnotesize \textit{Notes:} " + notes + r"\end{minipage}", r"\end{table}"]
    (DEST / f"{name}.tex").write_text("\n".join(T) + "\n", encoding="utf-8")


HYP = {"a3": "H1", "dg1": "H2", "db1": "H3"}


def hyps_in(model):
    return {HYP[p] for p in ("a3", "dg1", "db1") if p not in core.NESTED[model]}


# ------------------------------------------------------------------ hypothesis tests
def tab_hyp():
    rows = []
    names = {"H1 access (a3)": r"\textit{H1: access to good jobs ($\alpha_3$)}",
             "H2 pay-off of schooling in accumulation (dg1)":
                 r"\textit{H2: pay-off of schooling in accumulation ($\gamma_1(B) - \gamma_1(W)$)}",
             "H3 entry return to schooling (db1)": r"\textit{H3: entry return to schooling ($b_1(B) - b_1(W)$)}"}
    lab = {"alone": "alone", "given a3": "given H1", "given dg1": "given H2", "given db1": "given H3",
           "given a3 + dg1": "given H1 and H2", "given a3 + db1": "given H1 and H3", "given db1 + dg1": "given H2 and H3"}
    for h, rr in L["hypotheses"].items():
        rows.append(r"\multicolumn{6}{l}{" + names[h] + r"} \\")
        par = {"H1": "a3", "H2": "dg1", "H3": "db1"}[h[:2]]
        for k, r in rr.items():
            d = r["R20"]
            e = est_lat(r["with"])                                 # s.e. of the estimation job (R = 20)
            rows.append(f"\\quad {lab[k]} & {r['without']} $\\to$ {r['with']} & {num(d['mean'], 1)} ({d['sd']:.1f}) & "
                        f"{num(d['min'], 1)} & {'yes' if d['pass_all'] else 'no'} & "
                        f"{coef(e['theta'][par], e['se'][par], 4)}" r" \\")
    rows.append(r"\multicolumn{6}{l}{\textit{H4: pay-off of parental income in accumulation ($\gamma_x(B) - \gamma_x(W)$)}}"
                r" \\")
    for k, lab_, m in (("alone", "alone", "A"), ("given dg1 + db1", "given H2 and H3", "E")):
        d = H4["drops"][k]
        e = est_lat(m)
        rows.append(f"\\quad {lab_} & {m} without H4 $\\to$ {m} & {num(d['mean'], 1)} ({d['sd']:.1f}) & {num(d['min'], 1)}"
                    f" & {'yes' if d['pass_all'] else 'no'} & {coef(e['theta']['dgx'], e['se']['dgx'], 4)}" r" \\")
    table("tab_model_hyp", "The four hypotheses: drop in the SMM criterion when the race parameter is added",
          "tab:modelhyp", "llcccc",
          r" & Models & Drop in $Q$: mean (s.d.) & Minimum & $> 3.84$ at & Estimate in the \\"
          "\n" r" & & over ten seeds & & every seed & richer model (s.e.) \\",
          rows,
          "Each row adds one race parameter to a model and reports the fall in the SMM criterion $Q$ (66 moments, "
          "diagonal weights) at the two models' estimates, computed on the same simulation draws at ten seeds (7--16), "
          "20 simulated sons per PSID son; mean, standard deviation and minimum over the seeds. A parameter is kept if "
          "the fall exceeds 3.84 at every seed (with diagonal weights this is a rule of thumb on the scale of a "
          "one-restriction test, not an exact $\\chi^2$ test). All models include the age profiles of job loss and of "
          "the on-the-job search friction, re-employment in the year of a displacement and the race-neutral pay-off of "
          "parental income in accumulation $\\gamma_x(W)$; the H4 rows fix $\\gamma_x(B) = \\gamma_x(W)$ in the model "
          "without H4. Models H and G moved by 0.0 and 0.1 from their starting points (B's and A's solutions with "
          "$b_1(B) - b_1(W) = 0$) in 12,000 evaluations; along $b_1(B) - b_1(W)$ alone $Q$ rises on both sides of these "
          "points (by 6 to 10 at $\\pm 0.01$), so they are minima in that direction (at E, $Q$ falls by 0.3 at "
          "$\\alpha_3 = -0.1$, consistent with the 0.5 that D finds at the estimation draws), and a joint move of "
          "several "
          "parameters is tested by a polish re-estimation of every model from its own solution, which moved no $Q$ by "
          "more than 0.12 (D; C 0.06, all others 0.00), so the rows through G and H are not bounds. Polish runs: "
          "\\texttt{model/hpc\\_runs/P\\_*}. Profiles: \\texttt{model/profile\\_q.py}. Last column: the parameter in the richer model, sandwich standard errors "
          "of the estimation (20 simulated sons per PSID son); $^{***}$ $p<0.01$, "
          "$^{**}$ $p<0.05$, $^{*}$ $p<0.1$. Code: \\texttt{model/lattice\\_q.py}, \\texttt{model/h4\\_seeds.py}; "
          "output \\texttt{model/output/final\\_x4/}.")


# ------------------------------------------------------------------ the ten models
def tab_lattice():
    rows = []
    order = [("A_noH4", "A without H4"), ("E_noH4", "E without H4"), ("A", "A"), ("B", "B"), ("F", "F"), ("G", "G"),
             ("C", "C"), ("H", "H"), ("E", "E"), ("D", "D")]
    rows.append(r"\multicolumn{10}{l}{\textit{Without H4}} \\")
    for key, lab in order:
        if key == "A":
            rows.append(r"\midrule \multicolumn{10}{l}{\textit{With H4}} \\")
        m = key[0]
        e = est_lat(key)
        mm = dict(zip(core.MOMENT_NAMES, e["moments"]))
        h = hyps_in(m) | (set() if key.endswith("noH4") else {"H4"})
        if key.endswith("noH4"):
            qs = np.array(H4["Q"][lab])
        else:
            qs = np.array(L["models"][m]["R20"]["Q"])
        qige = sum(((mm[k] - MD[k]) / SD[k]) ** 2 for k in core.MOMENT_NAMES if k.startswith("ige_"))
        tick = " & ".join(r"$\checkmark$" if x in h else "" for x in ("H1", "H2", "H3", "H4"))
        rows.append(f"{lab} & {tick} & {e['Q']:.1f} & {qs.mean():.1f} ({qs.std(ddof=1):.1f}) & "
                    f"{mm['ige_3034_W'] - mm['ige_3034_B']:.3f} & {mm['ige_4549_W'] - mm['ige_4549_B']:.3f} & "
                    f"{qige:.1f}" r" \\")
    rows.append(r"\midrule")
    rows.append(f"PSID & & & & & & & {MD['ige_3034_W'] - MD['ige_3034_B']:.3f} & "
                f"{MD['ige_4549_W'] - MD['ige_4549_B']:.3f} &" r" \\")
    table("tab_model_lattice", "The hypothesis lattice: fit of every combination of race parameters", "tab:modellattice",
          "lccccccccc",
          r"Model & H1 & H2 & H3 & H4 & $Q$ & $Q$ over ten & W $-$ B IGE gap & W $-$ B IGE gap & $Q$ of the \\"
          "\n" r" & & & & & & seeds: mean (s.d.) & 30--34 & 45--49 & 12 IGE moments \\",
          rows,
          "Each model is estimated by SMM on the 66 moments with 20 simulated sons per PSID son (12,000 CMA-ES "
          "evaluations, each started from the best solution of the models nested in it). $Q$: the criterion at the "
          "estimation draws, and its mean (standard deviation) over ten simulation seeds. IGE gaps and the $Q$ of the "
          "IGE moments at the estimation draws. IGE gaps: White $-$ Black "
          "coefficient of the son's log wage on log parental income, simulated with the PSID observation scheme. H1 "
          "access ($\\alpha_3$), H2 pay-off of schooling in accumulation, H3 entry return to schooling, H4 pay-off of "
          "parental income in accumulation. Model H's solution is model B's (see the note to "
          "Table~\\ref{tab:modelhyp}). Code: \\texttt{model/hpc\\_ige\\_chain.sh}, "
          "\\texttt{model/lattice\\_q.py}.")


# ------------------------------------------------------------------ estimates of model E
LAB = {"muB": r"$\mu_B$, racial wage level", "dg1": r"$\gamma_1(B) - \gamma_1(W)$, pay-off of schooling (H2)",
       "db1": r"$b_1(B) - b_1(W)$, entry return to schooling (H3)",
       "dgx": r"$\gamma_x(B) - \gamma_x(W)$, pay-off of parental income (H4)",
       "bx": r"$b_x$, starting level", "a1": r"$\alpha_1$, access to $G$ jobs", "gx": r"$\gamma_x(W)$, accumulation",
       "d1": r"$\delta_1$, displacement", "b1": r"$b_1(W)$, starting level", "a2": r"$\alpha_2$, access to $G$ jobs",
       "g1": r"$\gamma_1(W)$, accumulation", "b0": r"$b_0$, starting level", "lsig0": r"$\ln\sigma_0$, starting level",
       "a0": r"$\alpha_0$, access to $G$ jobs", "gO": r"$\gamma_O$, accumulation on $O$ jobs",
       "gG": r"$\gamma_G$, accumulation on $G$ jobs", "lrho": r"$\ln\rho$, decline of accumulation with age",
       "lsigm": r"$\ln\sigma_m$, match component", "llam_e": r"logit $\lambda_e$ at 30, on-the-job search friction",
       "la": r"$\lambda_a$, its age slope (per decade)", "llam_u": r"logit $\bar\lambda_u$, job finding out of work",
       "d0B": r"$\delta_{0B}$, displacement, Black", "d0W": r"$\delta_{0W}$, displacement, White",
       "da": r"$\delta_a$, its age slope (per decade)", "lsigeta": r"$\ln\sigma_\eta$, permanent shock",
       "lsigeps": r"$\ln\sigma_\varepsilon$, transitory shock",
       "dlu": r"$\Delta\ell_u$, job finding out of work, Black $-$ White (logit)"}
GROUPS = [("Race", ["muB", "dg1", "db1", "dgx"]), ("Parental income", ["bx", "a1", "gx", "d1"]),
          ("Schooling", ["b1", "a2", "g1"]), ("Jobs, search frictions and job loss",
                                              ["a0", "gO", "gG", "lrho", "lsigm", "llam_e", "la", "llam_u", "dlu", "d0B", "d0W",
                                               "da"]),
          ("Starting level and shocks", ["b0", "lsig0", "lsigeta", "lsigeps"])]


def tab_estimates():
    e = est("E")
    rows = []
    for g, ps in GROUPS:
        rows.append(r"\multicolumn{2}{l}{\textit{" + g + r"}} \\")
        for p in (q for q in ps if q in e["theta"]):
            log_scale = p.startswith(("l", "lsig"))
            rows.append(f"\\quad {LAB[p]} & {coef(e['theta'][p], e['se'][p], 4, stars=not log_scale)}" r" \\")
    rows.append(r"\midrule")
    rows.append(f"$Q$ (66 moments), estimation draws & {e['Q']:.1f}" r" \\")
    cap = "Estimates of the selected model (E: H2, H3 and H4" + (
        "; job finding out of work by race)" if "dlu" in e["theta"] else ")")
    table("tab_model_estimates", cap, "tab:modelest", "lc",
          r"Parameter & Estimate (s.e.) \\", rows,
          "Simulated method of moments, 66 moments, diagonal weights equal to the inverse cluster-bootstrap variances "
          "(500 draws of 1968 families), 20 simulated sons per PSID son. Sandwich standard errors $(1 + 1/R)\\,"
          "(G'WG)^{-1}G'W\\Omega WG(G'WG)^{-1}$ with $\\Omega$ the bootstrap covariance of the moments; $^{***}$ "
          "$p<0.01$, $^{**}$ $p<0.05$, $^{*}$ $p<0.1$ (not shown for parameters on a log or logit scale). Accumulation "
          "parameters per year; parental income and schooling are centred at the sample mean and at 12 years. Fixed: "
          "$\\beta = 0.95$, $b = 0.4$, cyclical elasticities $\\mp 0.10$, $\\alpha_3 = 0$ (H1 rejected), the match "
          "premium of $G$ jobs $\\mu_G = 0$ and depreciation out of work $d_u = 0$ (Section~\\ref{sec:model}). Code: "
          "\\texttt{model/estimate.py}; output \\texttt{model/output/final\\_x4/estimates\\_E.json}.")


# ------------------------------------------------------------------ fit of model E
def tab_fit():
    e = est("E")
    mm = dict(zip(core.MOMENT_NAMES, e["moments"]))
    groups = [("Persistence by age (log-wage IGE)", [f"ige_{b}_{r}" for r in "WB" for b in
                                                     ("2529", "3034", "3539", "4044", "4549", "5055")]),
              ("Return to schooling", [f"rets_{b}_{r}" for r in "WB" for b in ("2529", "4549")]),
              ("Careers", ["G_t1_B", "G_t3_B", "G_t1_W", "G_t3_W", "gst_2534_O", "gst_2534_G", "dsp_2534_B",
                           "dsp_2534_W", "dsp_3555_B", "dsp_3555_W", "mov_2534_W", "mov_3555_W", "gmv_2534_B",
                           "gmv_2534_W", "zero_B", "zero_W", "vlw_4549_B", "vlw_4549_W", "vgst", "acgst"])]
    lab = {"ige": "IGE", "rets": "return to schooling", "G": "share in $G$ jobs at 25--34", "gst": "same-employer growth",
           "dsp": "displacement rate", "mov": "move rate", "gmv": "wage growth at a move", "zero": "zero-hours years",
           "vlw": "variance of log wages", "vgst": "variance of stayers' growth", "acgst": "autocovariance of stayers' growth"}
    sub = {"2529": "25--29", "3034": "30--34", "3539": "35--39", "4044": "40--44", "4549": "45--49", "5055": "50--55",
           "2534": "25--34", "3555": "35--55", "t1": "bottom tercile", "t3": "top tercile", "B": "Black", "W": "White",
           "O": "$O$ jobs", "G": "$G$ jobs"}
    rows = []
    for g, ks in groups:
        rows.append(r"\multicolumn{5}{l}{\textit{" + g + r"}} \\")
        for k in ks:
            parts = k.split("_")
            name = lab[parts[0]] + (", " + ", ".join(sub.get(x, x) for x in parts[1:]) if len(parts) > 1 else "")
            rows.append(f"\\quad {name} & {num(MD[k])} & ({SD[k]:.3f}) & {num(mm[k])} & "
                        f"{num((mm[k] - MD[k]) / SD[k], 1)}" r" \\")
    table("tab_model_fit", "Fit of the selected model (E): targeted moments", "tab:modelfit", "lcccc",
          r"Moment & PSID & (s.e.) & Model & $t$ \\", rows,
          "PSID sons (Black and White male heads, 25--55), cluster-bootstrap standard errors; model moments from the "
          "simulated panel with the PSID's observation scheme at the estimate (20 simulated sons per PSID son). $t$ = "
          "(model $-$ PSID) / s.e. Rates per interview pair, growth annualised. All 66 moments: "
          "\\texttt{model/output/final\\_x4/estimates\\_E.json}.")


# ------------------------------------------------------------------ counterfactuals of model E
def tab_cf():
    rows = []
    lab = {"Baseline": "Baseline: White $-$ Black gap",
           "Equal pay-off of parental income in accumulation (dgx = 0)":
               r"Equal pay-off of parental income in accumulation (H4 off)",
           "Equal pay-off of schooling (dg1 = 0)": r"Equal pay-off of schooling in accumulation (H2 off)",
           "Equalising schooling": "Equalising schooling",
           "Equal access by parental income (a1 = 0)": r"Equal access to $G$ jobs by parental income ($\alpha_1 = 0$)",
           "Equal displacement risk (d0B = d0W)": r"Equal displacement risk ($\delta_{0B} = \delta_{0W}$)",
           "Recession at entry (+3 points, 3 years)": "Recession at entry (+3 points for three years)",
           "Equal job finding out of work (dlu = 0)": r"Equal job finding out of work ($\Delta\ell_u = 0$)"}
    order = ["Baseline", "Equal pay-off of parental income in accumulation (dgx = 0)",
             "Equal pay-off of schooling (dg1 = 0)", "Equalising schooling", "Equal access by parental income (a1 = 0)",
             "Equal displacement risk (d0B = d0W)", "Equal job finding out of work (dlu = 0)",
             "Recession at entry (+3 points, 3 years)"]
    for k in (k for k in order if k in PE["cf"]):
        v = PE["cf"][k]

        def c(key):
            d = v[key]
            return f"${d['value']:.3f}{star(d['p'])}$ ({d['se']:.3f})"
        rows.append(f"{lab[k]} & {c('gap_3034')} & {c('gap_4549')} & {v['mlw2534_B']['value']:.3f} & "
                    f"{v['mlw2534_W']['value']:.3f}" r" \\")
        if k == "Baseline":
            rows.append(r"\midrule \multicolumn{5}{l}{\textit{Change from the baseline}} \\")
    table("tab_model_cf", "Counterfactuals in the selected model (E)", "tab:modelcf", "lcccc",
          r"Experiment & IGE gap, 30--34 & IGE gap, 45--49 & Log wage 25--34, Black & Log wage 25--34, White \\",
          rows,
          "Simulated at the estimates of model E with the PSID sons' race, parental income, schooling and birth "
          "years and the PSID observation scheme, 20 simulated sons per PSID son. First row: baseline White $-$ Black "
          "gap in the log-wage IGE and mean log wages; other rows: changes from it. The racial wage level $\\mu_B$ is "
          "held fixed. H4 off: Black sons get White sons' pay-off of parental income in accumulation; because Black "
          "sons' parental income is mostly below the pooled mean around which the term is centred, this raises the "
          "Black IGE and lowers the mean Black wage; it is a decomposition of the gap, not a policy. Equalising "
          "schooling: Black sons' schooling drawn from White sons' within the same parental-income decile. Recession at "
          "entry: national unemployment 3 points higher in each son's first three years in the labor market. "
          "Delta-method standard errors (same draws at every parameter value); $^{***}$ $p<0.01$, $^{**}$ $p<0.05$, "
          "$^{*}$ $p<0.1$. Code: \\texttt{model/postestimation.py}; output "
          "\\texttt{model/output/postestimation\\_Lx4\\_E.json}.")


def tab_untargeted():
    ps = json.load(open(HERE / "output" / "validation_psid.json"))
    mo = json.load(open(F / "validation_E.json"))["stats"]
    U = json.load(open(HERE / "output" / "untargeted_psid.json"))
    UE = L["models"]["E"]["R20"]
    groups = [
        ("Mean log wage", [("mlw_3539_W", "White, 35--39"), ("mlw_3539_B", "Black, 35--39"), ("mlw_4549_W", "White, 45--49"),
                           ("mlw_4549_B", "Black, 45--49"), ("mlw_3539_gap", "White $-$ Black, 35--39"),
                           ("mlw_4549_gap", "White $-$ Black, 45--49")]),
        ("Rank--rank slope (son's wage percentile on parental-income percentile)",
         [(f"rank_{b}_{r}", f"{'White' if r == 'W' else 'Black'}, {lab}") for r in "WB"
          for b, lab in (("2529", "25--29"), ("3034", "30--34"), ("4549", "45--49"))]
         + [(f"rank_{b}_gap", f"White $-$ Black, {lab}") for b, lab in (("2529", "25--29"), ("4549", "45--49"))]),
        ("Share whose modal job at 35--55 is a $G$ job", [(f"G3555_t{t}_{r}", f"{'White' if r == 'W' else 'Black'}, "
                                                            f"{'bottom' if t == 1 else 'top'} parental tercile")
                                                           for r in "WB" for t in (1, 3)]),
        ("Log-wage IGE below the median of parental income", [(f"igebelow_{b}_{r}", f"{'White' if r == 'W' else 'Black'}"
                                                                f", {lab}") for r in "WB"
                                                               for b, lab in (("2529", "25--29"), ("4549", "45--49"))]),
        ("Parental-income gradient of log wages without / with a $G$-job dummy",
         [(f"{k}_{b}_{r}", f"{'White' if r == 'W' else 'Black'}, {lab}, {'without' if k == 'ige' else 'with'}")
          for r in "WB" for b, lab in (("2534", "25--34"), ("3555", "35--55")) for k in ("ige", "igewithinG")]),
    ]
    rows = []
    for g, items in groups:
        rows.append(r"\multicolumn{5}{l}{\textit{" + g + r"}} \\")
        for k, lab in items:
            p_, m_ = ps[k], mo[k]
            rows.append(f"\\quad {lab} & {num(p_['value'])} & ({p_['se']:.3f}) & {num(m_['mean'])} & "
                        f"{num((m_['mean'] - p_['value']) / p_['se'], 1)}" r" \\")
    rows.append(r"\multicolumn{5}{l}{\textit{Same-employer growth at 25--34 on log parental income}} \\")
    for k, lab in (("gst_x_W", "White"), ("gst_x_B", "Black"), ("gst_x_net_e_W", "White, net of schooling"),
                   ("gst_x_net_e_B", "Black, net of schooling")):
        m_ = float(np.mean(UE[k]))
        rows.append(f"\\quad {lab} & {num(U[k]['value'])} & ({U[k]['se']:.3f}) & {num(m_)} & "
                    f"{num((m_ - U[k]['value']) / U[k]['se'], 1)}" r" \\")
    table("tab_model_untargeted", "Untargeted validation of the selected model (E)", "tab:modeluntargeted", "lcccc",
          r"Statistic & PSID & (s.e.) & Model & $t$ \\", rows,
          "None of these statistics is a target. PSID: the sons' panel of the targets, 300 cluster-bootstrap draws of "
          "1968 families. Model: model E at its estimates, mean over ten simulation seeds, 20 simulated sons per PSID "
          "son, the same code (\\texttt{model/core.py}, \\texttt{validation} and \\texttt{untargeted}) on the "
          "simulated panel with the PSID observation scheme. $t$ = (model $-$ PSID) / PSID s.e. Ranks: percentile of "
          "the son's log wage among Black and White sons in the band and of parental income among the same sons. "
          "Output: \\texttt{model/output/validation\\_psid.json}, \\texttt{final\\_x4/validation\\_E.json}; code "
          "\\texttt{model/validation\\_run.py}.")


def tab_cf_h4():
    O = json.load(open(HERE / "output" / "postestimation_Lx4_E_h4.json"))["cf"]
    b = O["Baseline"]
    h = O["Equal pay-off of parental income in accumulation (dgx = 0)"]
    z = O["No pay-off of parental income in accumulation (gx = dgx = 0)"]

    def c(d):
        return f"${d['value']:.3f}{star(d['p'])}$ ({d['se']:.3f})"
    rows = [r"\multicolumn{7}{l}{\textit{A. Log-wage IGE by age}} \\"]
    for k, lab in (("2529", "25--29"), ("3034", "30--34"), ("3539", "35--39"), ("4044", "40--44"), ("4549", "45--49"),
                   ("5055", "50--55")):
        rows.append(f"\\quad {lab} & {b['B_' + k]['value']:.3f} & {c(h['B_' + k])} & {b['gap_' + k]['value']:.3f} & "
                    f"{c(h['gap_' + k])} & {b['W_' + k]['value']:.3f} & {c(z['W_' + k])}" r" \\")
    rows.append(r"\midrule \multicolumn{7}{l}{\textit{B. Mean log wage by parental-income tercile}} \\")
    rows.append(r" & Black & H4 off: change & & & White & No pay-off: change \\")
    for a, alab in (("2534", "25--34"), ("4549", "45--49")):
        for t, tlab in ((1, "bottom"), (2, "middle"), (3, "top")):
            kb, kw = f"mlw{a}_t{t}_B", f"mlw{a}_t{t}_W"
            c4 = lambda d: f"${d['value']:.4f}{star(d['p'])}$ ({d['se']:.4f})"          # noqa: E731
            rows.append(f"\\quad {alab}, {tlab} tercile & {b[kb]['value']:.3f} & {c4(h[kb])} & & & {b[kw]['value']:.3f} & "
                        f"{c4(z[kw])}" r" \\")
    table("tab_model_cf_h4", "The pay-off of parental income in accumulation: by age and parental income (model E)",
          "tab:modelcfh4", "lcccccc",
          r" & Black IGE & H4 off: & W $-$ B gap & H4 off: & White IGE & No pay-off: \\"
          "\n" r" & baseline & change & baseline & change & baseline & change \\", rows,
          "Model E at its estimates, 20 simulated sons per PSID son, the PSID observation scheme. H4 off: Black sons get "
          "White sons' pay-off of parental income in accumulation, $\\gamma_x(B) = \\gamma_x(W)$. No pay-off: "
          "$\\gamma_x(B) = \\gamma_x(W) = 0$, the race-neutral channel switched off for both races. Parental income is "
          "centred at the pooled mean, so a pay-off lowers the wages of sons below the mean and raises those above it. "
          "Terciles of parental income over all sons. Delta-method standard errors; $^{***}$ $p<0.01$, $^{**}$ "
          "$p<0.05$, $^{*}$ $p<0.1$. Code: \\texttt{model/postestimation.py} (\\texttt{IGE\\_CFS}); output "
          "\\texttt{model/output/postestimation\\_Lx4\\_E\\_h4.json}.")


def tab_sens():
    S = json.load(open(F / "sensitivity.json"))
    blocks = ["IGE", "returns to schooling", "levels and variances", "G shares", "stayer growth",
              "moves and displacement", "zero hours"]
    lab = {"dgx (E)": r"$\gamma_x(B) - \gamma_x(W)$ (H4)", "gx (E)": r"$\gamma_x(W)$",
           "dg1 (E)": r"$\gamma_1(B) - \gamma_1(W)$ (H2)", "db1 (E)": r"$b_1(B) - b_1(W)$ (H3)",
           "a3 (D)": r"$\alpha_3$ (H1, model D)", "H4 off: change in the gap at 45-49": r"H4 off: change in the gap, 45--49"}
    mlab = {"ige": "IGE", "rets": "return", "G": "$G$ share", "gste": "stayer slope", "gst": "stayer growth",
            "dsp": "displacement"}

    def mname(n):
        parts = n.split("_")
        head = mlab.get(parts[0], parts[0])
        rest = " ".join(p.replace("2529", "25--29").replace("3034", "30--34").replace("3539", "35--39")
                        .replace("4044", "40--44").replace("4549", "45--49").replace("5055", "50--55")
                        .replace("2534", "25--34").replace("3555", "35--55").replace("t1", "bottom tercile")
                        .replace("t2", "middle tercile").replace("t3", "top tercile") for p in parts[1:])
        return f"{head} {rest}"
    rows = []
    for k, v in S.items():
        sh = " & ".join(f"{100 * v['block_shares'][b]:.0f}" for b in blocks)
        top = "; ".join(f"{mname(n)} ${s:+.2f}$" for n, s in v["top"][:3])
        rows.append(f"{lab[k]} & {sh} & {top}" r" \\")
    table("tab_model_sens", "Which moments identify the race parameters: sensitivity of the estimates (model E)",
          "tab:modelsens", "lccccccc p{5.2cm}",
          r" & IGE & Returns & Levels, & $G$ & Stayer & Moves, & Zero & Largest loadings \\"
          "\n" r" & & & variances & shares & growth & displacement & hours & \\", rows,
          "Sensitivity in the sense of \\citet{andrews2017measuring}: $\\Lambda = (G'WG)^{-1}G'W$, the derivative of the "
          "estimate with respect to the data moments, from the numerical Jacobian $G$ at the estimate (20 simulated sons "
          "per PSID son) and the diagonal weights $W$. $S_{jk} = \\Lambda_{jk}\\hat s_k / \\mathrm{se}_j$ is the shift of "
          "parameter $j$, in its standard errors, when moment $k$ rises by one data standard error. Columns 1--7: the "
          "share (\\%) of $\\sum_k S_{jk}^2$ in each block of moments; last column: the three largest $S_{jk}$ with "
          "their signs (race W / B, age band). Last row: the same for the counterfactual change in the W $-$ B IGE gap "
          "at 45--49 when Black sons get White sons' pay-off of parental income, from its gradient. Code: "
          "\\texttt{model/sensitivity.py}; output \\texttt{model/output/final\\_x4/sensitivity.json}.")


def tab_steps():
    S = json.load(open(F / "steps.json"))
    rows = []
    for r in S:
        dq = "" if r["dQ"] is None else f"${r['dQ']:+.1f}$"
        rows.append(f"{r['step']} & {r['what']} & {r['model']} & {r['draws']} & {r['Q']:.1f} & {dq}" r" \\")
    table("tab_model_steps", "How the model was built: each step, its model and the change in the criterion",
          "tab:modelsteps", "clcccc",
          r"Step & What changed & Model & Draws & $Q$ & $\Delta Q$ \\", rows,
          "$Q$: the SMM criterion on the 66 moments at the step's estimate; $\\Delta Q$: against the run listed in "
          "\\texttt{model/output/final\\_x4/steps.json} on the same simulation draws (five simulated sons per PSID "
          "son for steps 1--4, twenty for step 5, so $Q$ is comparable only within those groups). Step 1 is the first "
          "lattice of three race hypotheses; steps 2--4 change the model one at a time; step 5 is the final lattice of "
          "Section~\\ref{sec:model} (estimation draws; the ten-seed means are in Table~\\ref{tab:modelhyp}). Code: "
          "\\texttt{model/steps\\_summary.py}.")


def tab_h4measure():
    J = json.load(open(HERE.parent / "output" / "long_difference_measures.json"))
    R, M = J["results"], J["model"]
    srcs = ["PSID 13-19 mean", "PSID 12-17 mean", "PSID one year (16)", "NLSY79 1979-81 mean", "PSID born 1957-64"]
    labs = {"PSID 13-19 mean": "PSID, parental income 13--19 mean (the paper's)", "PSID 12-17 mean": "PSID, 12--17 mean",
            "PSID one year (16)": "PSID, one year at 16", "NLSY79 1979-81 mean": "NLSY79, 1979--81 mean",
            "PSID born 1957-64": "PSID, sons born 1957--64, 13--19 mean"}

    def c(r):
        p = 2 * (1 - norm.cdf(abs(r["raw"]) / r["raw_se"]))
        return f"${r['raw']:.3f}{star(p)}$ ({r['raw_se']:.3f})"
    rows = []
    for g in ("White", "Black"):
        rows.append(r"\multicolumn{5}{l}{\textit{" + g + r" sons}} \\")
        for s in srcs:
            cells = [c(R[f"{h}|{k}|{s}"][g]) for h in ("3539", "4549") for k in ("raw", "net")]
            rows.append(f"\\quad {labs[s]} & " + " & ".join(cells) + r" \\")
        N97 = json.load(open(HERE.parent / "output" / "long_difference_nlsy97.json"))
        cells = [c(N97[f"one year 1996|{k}"][g]) for k in ("raw", "net")] + ["", ""]
        rows.append("\\quad NLSY97, one year (1996; schooling: degree dummies) & " + " & ".join(cells) + r" \\")
        r_ = "W" if g == "White" else "B"
        for xm, lab in (("x13", "model E, 13--19 mean"), ("x1", "model E, the same sons' one-year measure")):
            cells = [f"${M[f'{xm}_ld{hh}_x{nn}_{r_}'][0]:.3f}$ [{M[f'{xm}_ld{hh}_x{nn}_{r_}'][1]:.3f}]"
                     for hh in ("10", "20") for nn in ("", "_net_e")]
            rows.append(f"\\quad {lab} & " + " & ".join(cells) + r" \\")
    table("tab_h4measure", "The pay-off of parental income in long differences, by measure of parental income",
          "tab:h4measure", "lcccc",
          r" & \multicolumn{2}{c}{Ten years (25--29 to 35--39)} & \multicolumn{2}{c}{Twenty years (to 45--49)} \\"
          "\n" r" & raw & net of schooling & raw & net of schooling \\", rows,
          "Change of a son's own mean log hourly wage between the bands on log parental income, sons with a wage in "
          "both bands, by race; columns 2 and 4 control for years of schooling. PSID: the model's sample of sons, "
          "parental income measured as the 13--19 mean (the paper's), the 12--17 mean or one year at 16; standard "
          "errors from 200 cluster-bootstrap draws of 1968 families. NLSY79: men, 1979--81 mean of the youth's household "
          "income, clusters 1979 household. Model E: the statistic on the simulated panel (twenty simulated sons per "
          "PSID son, ten seeds, seed s.d.\\ in brackets), with each simulated son's parental income measured as his PSID "
          "son's 13--19 mean (which generated the model's wages) or his one-year measure. The PSID sample of sons born "
          "1957--64 (the NLSY79's cohorts) has 385 (ten years) and 271 (twenty years) White sons. NLSY97: men born "
          "1980--84, parental income the 1996 parent report, schooling as final-degree dummies, ten years only, clusters "
          "1997 household (\\texttt{IGE/69.LongDifferenceNLSY97.py}). $^{***}$ $p<0.01$, "
          "$^{**}$ $p<0.05$, $^{*}$ $p<0.1$. Code: \\texttt{IGE/68.LongDifferenceMeasurement.py}.")


if __name__ == "__main__":
    tab_h4measure()
    tab_steps()
    tab_sens()
    tab_cf_h4()
    tab_untargeted()
    tab_hyp()
    tab_lattice()
    tab_estimates()
    tab_fit()
    tab_cf()
    print("tables written")
