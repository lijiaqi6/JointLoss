"""Assemble IGE/bps_reconciliation/bps_reconciliation.md from the narrative and the tables of compile_results.py."""
import re
from pathlib import Path

D = Path(__file__).resolve().parents[1]
T = D / "tables"


def blocks(text):
    """split a tables file into {heading: block} at '### ' headings"""
    out, cur, key = {}, [], None
    for line in text.splitlines():
        if line.startswith("### "):
            if key:
                out[key] = "\n".join(cur).strip()
            key, cur = line, [line]
        else:
            cur.append(line)
    if key:
        out[key] = "\n".join(cur).strip()
    return out


def get(b, prefix):
    k = [x for x in b if x.startswith(prefix)]
    return b[k[0]] if k else f"({prefix} missing)"


s2 = blocks((T / "step2.md").read_text(encoding="utf-8"))
at = blocks((T / "attrition.md").read_text(encoding="utf-8"))
md = [(D / "code" / "narrative_head.md").read_text(encoding="utf-8").rstrip(), "",
      "## Step 0. BPS as shipped", "", (T / "step0.md").read_text(encoding="utf-8").strip(), "",
      "## Step 1. Relaxing the restrictions", "",
      "Columns = specifications (one estimation each); rows = parameters. Wage-process rows: stationary ('all ages') "
      "GMM of T4C41 with GMM s.e.; correlations = covariance / sqrt(product of variances), no s.e. (the test of the "
      "covariance is the test of the correlation). Preference, elasticity, chain and share rows: T4C1 (age-varying "
      "variances) with bootstrap s.e. where a bootstrap was run (last row), else GMM s.e. (†) or none (chain rows). "
      "beta: T4C5. 'n.c.' = GMM did not converge. Black couples: the residual and pi / s steps run, but the "
      "preference step is not identified (see summary).", "",
      (T / "step1.md").read_text(encoding="utf-8").strip(), "", get(at, "### Table S1e"), "",
      "## Step 2. Displacement and joint displacement in BPS's panel", "",
      get(s2, "### Table S2.1"), "", get(at, "### Table S2.2"), "", get(s2, "### Table S2.3"), "",
      (T / "step2_cov.md").read_text(encoding="utf-8").strip(), "", get(s2, "### Table S2.5"), "",
      get(s2, "### Table S2.6"), "",
      "## Extension to 1999-2021: not done", "",
      "The PSID family files to 2021 are on disk, but BPS's pipeline needs, for each new wave, the ER-variable mapping "
      "of `psid_interview.do` (about 100 variables per wave), and for each new year the federal tax, EITC and Food "
      "Stamp parameters hard-coded in `tax_rate_estimation_snap.do` (1998-2008 only), poverty lines "
      "(`poverty_line2.dta` ends in 2008) and state minimum wages (`min_wage.dta` ends in 2010). None of these exist "
      "in the package or the repo; see `README.md`. A raw rebuild of 1999-2009 is also blocked by the missing "
      "early-release 1999 income file `faminc99`; Step 0 therefore starts from BPS's shipped `psid_cons.dta`, which "
      "reproduces their estimation file exactly.", "",
      "## Caveats", "",
      "- 50 bootstrap replications (BPS: 200); residual regressions are not re-estimated inside the bootstrap (as in "
      "BPS). Failed replications are dropped (kept: c 48, Black 47, f 47, f weighted 46 of 50); in these four runs BPS's own table step in `bootstrap.do` then stops (r(198), logs), after the replications file is saved; s.e. come from that file.",
      "- Weighted runs weight the residual regressions, both GMM steps (through scaled instruments, because Stata's "
      "`gmm` refuses weights with `nocommonesample`) and the chain means, not the tax-function and pi / s projections.",
      "- Displacement flags exist only for SRC + SEO heads (IGE's person file): Step 2 shares and event studies use "
      "BPS's rows less the 1997 immigrant refresher; Table 7 uses all rows.",
      "- Displacements are dated to calendar years from the reason-for-job-end items (19 / 25); a row with income "
      "year t carries those of t-1 and t. Odd calendar years (two years before the interview) are under-reported "
      "(recall), as in 19 / 25.",
      "- Joint displacement cells are small (17-28 couple-years in BPS's sample; 25 with all relaxations): "
      "every joint estimate is imprecise and an association.",
      ""]
txt = "\n".join(md)
(D / "bps_reconciliation.md").write_text(txt, encoding="utf-8")
print(len(txt), "chars;", txt.count("missing)"), "missing blocks")
