#!/usr/bin/env python3
#SBATCH --job-name=Joint-smm-main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=64G
#SBATCH --time=36:00:00
#SBATCH --output=joint_%x_%j.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jiaqi.li@sheffield.ac.uk
"""
Paper A structural model on the Sheffield HPC (Stanage, Slurm): job script and launcher in one file, modelled on
scripts/hpc_job.py (which is not touched). The #SBATCH lines are comments to Python; sbatch options on the command
line override them. The job runs paperA_model/estimate.py. The PI submits (login needs the password and Duo).

PAPER A HAS ITS OWN REPOSITORY AND HPC ENVIRONMENT (since 2026-10-20 github.com/lijiaqi6/JointLoss; before that the
clone ~/joint of Selection-vs-risk): the clone ~/jointloss, with its own .venv and its own results folder
/mnt/parscratch/users/$USER/joint_smm_results; never ~/svr (child penalty), ~/ige or the old ~/joint. Everything below
is relative to ~/jointloss.

ONE-TIME SETUP on the Stanage login node, idempotent (creates only what is missing and stops if ~/jointloss is
non-empty and not a clone of the repository). GitHub deploy keys belong to one repository: the key ~/.ssh/github_svr
opens Selection-vs-risk only, so JointLoss needs its own deploy key with write access (ssh-keygen -t ed25519 -f
~/.ssh/github_jointloss; add the .pub under JointLoss > Settings > Deploy keys, 'Allow write access'; and in
~/.ssh/config a 'Host github-jointloss' entry with HostName github.com and IdentityFile ~/.ssh/github_jointloss, so
the URL below is git@github-jointloss:lijiaqi6/JointLoss.git). Paste as is (the parentheses run it in a subshell, so
a stop does not close the login shell):
    ( set -e
      J=~/jointloss; URL=git@github-jointloss:lijiaqi6/JointLoss.git
      if git -C "$J" remote -v 2>/dev/null | grep -q 'lijiaqi6/JointLoss'; then
          echo "$J is already a clone: pulling"; git -C "$J" pull --ff-only
      elif [ ! -e "$J" ] || [ -z "$(ls -A "$J")" ]; then
          echo "cloning into $J"; git clone "$URL" "$J"
      else
          echo "STOP: $J is not empty and is not a clone of $URL (move its contents, then rerun)"; exit 1
      fi
      cd "$J"
      UV=$(command -v uv || echo ~/.local/bin/uv)
      [ -x "$UV" ] || { curl -LsSf https://astral.sh/uv/install.sh | sh; UV=~/.local/bin/uv; }
      if [ -x .venv/bin/python ]; then echo ".venv exists"; else "$UV" venv --python 3.12.13 .venv; fi
      "$UV" pip install --python .venv/bin/python -r requirements.txt     # numba, cma, scipy, pandas, statsmodels
      git config user.email >/dev/null || echo "NOTE: set git user.name / user.email in $J (needed by --push)"
      mkdir -p /mnt/parscratch/users/$USER/joint_smm_results
      [ -f paperA_model/inputs/psid_entry_couples.csv ] || echo "NOTE: copy the entry couples (scp below)" )
  The PSID entry couples are git-ignored (PSID terms: individual records are never committed or pushed): copy them
  from the PC once, and again whenever IGE/62 rewrites them (Git Bash or PowerShell on the PC; your username in place
  of cm1jil):
    scp "G:/My Drive/JointLoss/paperA_model/inputs/psid_entry_couples.csv" cm1jil@stanage.shef.ac.uk:~/jointloss/paperA_model/inputs/
  Every job checks that the file exists and stops at once with this command if it does not. Then the 45-minute test:
    cd ~/jointloss && sbatch --job-name=Joint-test --time=01:30:00 paperA_model/hpc_job_a.py --test

SUBMIT from ~/jointloss after 'git pull' (job names start with 'Joint-'; 32 cores, --threads 2 -> 16 workers, 64G; the
objective is the trimmed vector (moments.OBJ_EXCLUDE, 85 moments: the husband's employment rate is reported, not
targeted) with diag_noise weights (inputs/moment_noise.csv); CPS entry / exit as persistent flows (--cps-persist on;
--cps-persist off --cps-classif on gives the one-month flows with the Poterba-Summers correction); extensions on by
default (estimate.EXT_DEFAULTS): borrowing wedge (inputs/borrowing_wedge.json), accumulation falling in the level
(eta_up free); memory of displacement off (--cs-memory on to test it); 31 free parameters (30 + eta_up);
order of the Fable review 2026-10-18, Section 2):
  0. test (checks; moments / Q at the analytic start against the PC; 2 CMA generations, resume; one LM iteration):
    sbatch --job-name=Joint-test --time=01:30:00 paperA_model/hpc_job_a.py --test
  1. pseudo-data recovery by Levenberg-Marquardt, all free parameters, from the truth (analytic start) perturbed by
     N(0, 0.5) in z units; targets at the same CRN seed (Q = 0 at the truth). Per iteration one Jacobian (61
     evaluations = 4 rounds of 16) + one round of 7 trial steps; 15 iterations + final Jacobian + 5 s.e. seeds
     ~ 1,100 evaluations ~ 80 rounds x 2.3 min ~ 3.1 h -> 5 h:
    sbatch --job-name=Joint-recovery-gn --time=10:00:00 paperA_model/hpc_job_a.py polish --pseudo --label all \
           --start-noise 0.5 --iters 15 --push
  2. Levenberg-Marquardt on the real targets from the analytic start (same sizing):
    sbatch --job-name=Joint-gn-main --time=10:00:00 paperA_model/hpc_job_a.py polish --label main --iters 15 --push
  2b. simulation noise at the LM candidate (the weights' var_sim; the noise file in inputs/ is from the pre-extension
     start): 5 CRN seeds, one round:
    sbatch --job-name=Joint-noise --time=00:30:00 paperA_model/hpc_job_a.py noise --start <gn>/best.json \
           --reps 5 --weighting diag --push
     then add --noise-file /mnt/parscratch/users/$USER/joint_smm_results/noise_<stamp>/moment_noise.csv to step 3
     and to the final LM polish (the objective then uses the same weights in both).
  3. CMA-ES around the LM candidate (<gn> = the Joint-gn-main run folder under
     /mnt/parscratch/users/$USER/joint_smm_results/runs/), per-coordinate stds from its final Jacobian, sigma0 0.2,
     popsize 16, 3,500 evaluations = 219 generations x 2.3 min ~ 8.4 h -> 12 h; two restarts with other CMA seeds:
    sbatch --job-name=Joint-smm-main --time=12:00:00 paperA_model/hpc_job_a.py run --label main \
           --start <gn>/best.json --cma-stds-from <gn>/jacobian.npz --sigma0 0.2 --maxfevals 3500 --tolfun 30 \
           --cma-seed 1 --push
    sbatch --job-name=Joint-smm-main-s2 --time=12:00:00 paperA_model/hpc_job_a.py run --label main_s2 \
           --start <gn>/best.json --cma-stds-from <gn>/jacobian.npz --sigma0 0.2 --maxfevals 3500 --tolfun 30 \
           --cma-seed 2 --push
    sbatch --job-name=Joint-smm-main-s3 --time=12:00:00 paperA_model/hpc_job_a.py run --label main_s3 \
           --start <gn>/best.json --cma-stds-from <gn>/jacobian.npz --sigma0 0.2 --maxfevals 3500 --tolfun 30 \
           --cma-seed 3 --push
  then an LM polish of the best CMA point (job 2 with --start <smm run>/best.json or mean.json).
  restricted independent-shock model (same targets and draws; LM then CMA as above):
    sbatch --job-name=Joint-gn-indep --time=10:00:00 paperA_model/hpc_job_a.py polish --label indep \
           --fix pi_c0=0 pi_c1=0 pi_c2=0 m_H=1 --push
  resume a CMA run stopped by its time limit (state saved every generation):
    sbatch --job-name=Joint-smm-main-r --time=12:00:00 paperA_model/hpc_job_a.py --push \
           --resume /mnt/parscratch/users/$USER/joint_smm_results/runs/<run dir>
  Jacobian / standard errors at an estimate:
    sbatch --job-name=Joint-jacobian --time=01:00:00 paperA_model/hpc_job_a.py jacobian --start <best.json> --push
    sbatch --job-name=Joint-se --time=01:30:00 paperA_model/hpc_job_a.py se --start <best.json> --push
  block-weighting robustness:
    sbatch --job-name=Joint-smm-block --time=12:00:00 paperA_model/hpc_job_a.py run --label block \
           --weighting block --start <gn>/best.json --sigma0 0.2 --maxfevals 3500 --push
  options for any estimate.py command: --set-fixed sigma_eps=<v>; --free-extra sigma_eps; --tie lam_h_W=lam_h_B;
  --drop <moment ids>; --weighting diag (the old weights)
  results of a job that ended without --push (dependent job, no computation):
    sbatch --job-name=Joint-push --dependency=afterany:<job> --time=00:10:00 --cpus-per-task=1 --mem=2G \
           paperA_model/hpc_job_a.py --push-only <run dir>
  queue with full names:  squeue -u $USER -o "%.10i %.24j %.8T %.10M %.6D %R"
--time sizing: rounds x (seconds per evaluation: 78-100 s alone on 2 threads on the PC; on Stanage 300 s alone and ~3.5-4
min per round of 16 under full load, measured in job 11863423) x 1.3; one LM iteration = 5 rounds ~ 20 min, so 15
iterations + final Jacobian + s.e. ~ 6.5 h -> --time 10:00:00 (the 45-minute test timed out in its LM step); at 16 workers one CMA generation of 16 is one round (the job stops itself 15 minutes before the limit, pushes,
and a CMA run resumes with --resume; an LM run restarts with --start <run>/best.json).
Results: run folders under PAPERA_OUT (default /mnt/parscratch/users/$USER/joint_smm_results); --push copies the
small, aggregate files (run.json, best.json, generations.csv, evals.csv.gz, Jacobian / se / noise reports, the job log)
into paperA_model/results/hpc_runs/<run>/ of ~/jointloss, commits on main and pushes (the --push logic of
scripts/hpc_job.py; a lock directory serialises pushes of jobs that end together); on the PC a git pull brings them in
(or scp the run folder). Nothing individual-level is pushed (es.pkl stays on scratch).
Code snapshot: the job runs 'git archive' of one commit (default HEAD of ~/jointloss; --commit SHA pins another) in
node-local storage; the git-ignored inputs are linked from the clone, so later pulls do not reach a queued job.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


def _find_repo():
    for c in (os.environ.get("JOINT_REPO"), os.environ.get("SLURM_SUBMIT_DIR"), str(Path(__file__).resolve().parents[1])):
        if not c:
            continue
        p = Path(c).resolve()
        for d in [p] + list(p.parents):
            if (d / "paperA_model" / "estimate.py").exists():
                return d
    sys.exit("cannot find the repository: submit from ~/jointloss (cd ~/jointloss) or set JOINT_REPO")


REPO = _find_repo()
_VENV = REPO / ".venv"
if (_VENV / "bin" / "python").exists() and Path(sys.prefix).resolve() != _VENV.resolve():
    os.execv(str(_VENV / "bin" / "python"), [str(_VENV / "bin" / "python")] + sys.argv)

MODEL = Path("paperA_model")
ENTRY = MODEL / "inputs" / "psid_entry_couples.csv"
NEEDED = [MODEL / "inputs" / f for f in ("schedules_era1.json", "schedules_era2.json", "schedules_era3.json",
                                         "start_analytic.json", "wage_process.json", "fixed_inputs.json",
                                         "moment_noise.csv", "expected_start_moments.csv",
                                         "borrowing_wedge.json")] + \
         [Path("output") / "paperA_targets.csv"]
UNTRACKED_LINKS = [ENTRY, MODEL / "inputs" / "psid_entry_couples_25_30.csv", MODEL / "inputs" / "start_overrides.json"]
# Q at the analytic start on the PC (estimate.py evaluate, default size, K 3, seed 20261018, inputs of 2026-10-18 20:20;
# trimmed objective (moments.OBJ_EXCLUDE) and diag_noise weights (inputs/moment_noise.csv)) and the 91 simulated
# moments there (inputs/expected_start_moments.csv): the reproducibility check of --test passes if every moment agrees to
# a relative 1e-6 or Q to a relative 1e-3 (Numba reductions differ across CPUs). Update both (estimate.py evaluate, then
# copy moments.csv's id and sim columns) when the code, the inputs or the targets change.
EXPECTED_Q = 11733.7   # clean numba build on the PC 11,733.703 (cached 11,733.685); Stanage 11,733.6 (job 11863423); the earlier 11,726.0 came from a stale PC cache
EXPECTED_MOMENTS = MODEL / "inputs" / "expected_start_moments.csv"
SCP = ('scp "G:/My Drive/JointLoss/paperA_model/inputs/psid_entry_couples.csv" '
       'cm1jil@stanage.shef.ac.uk:~/jointloss/paperA_model/inputs/')
PEAK_GB = 3.2                       # resident memory of one evaluation (default size, 12,360 couples x 3 copies)
RESULTS_DIR = MODEL / "results" / "hpc_runs"


def sh(cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def checks():
    print(f"repo {REPO}  commit {sh(['git', 'rev-parse', '--short', 'HEAD'])}")
    print(f"python {sys.version.split()[0]} at {sys.executable}")
    if not (REPO / ENTRY).exists():
        sys.exit(f"MISSING {ENTRY}: the PSID entry couples are git-ignored (PSID terms) and must be copied from the PC "
                 f"once:\n    {SCP}\n(replace cm1jil by your Stanage username), then resubmit.")
    miss = [str(p) for p in NEEDED if not (REPO / p).exists()]
    if miss:
        sys.exit(f"missing input files: {miss} (git pull?)")
    print(f"inputs present (entry couples: {sum(1 for _ in open(REPO / ENTRY)) - 1:,} rows)")


def code_snapshot(job, commit=None):
    import tarfile
    sha = sh(["git", "rev-parse", "--verify", f"{commit or 'HEAD'}^{{commit}}"])
    if not sha:
        sys.exit(f"unknown commit {commit!r}")
    dest = Path(os.environ.get("TMPDIR", "/tmp")) / f"paperA_code_{job}"
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True)
    proc = subprocess.Popen(["git", "archive", "--format=tar", sha, "--", "paperA_model", "output",
                             "60.PaperATargets.py", "common.py", "bps_reconciliation/code",
                             ":(exclude)paperA_model/results"], cwd=REPO, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tf:
        tf.extractall(dest, filter="fully_trusted")
    if proc.wait() != 0:
        sys.exit("git archive failed")
    for rel in UNTRACKED_LINKS:
        if not (dest / rel).exists() and (REPO / rel).exists():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            (dest / rel).symlink_to(REPO / rel)
    return dest, sha


def push_results(run_dirs):
    import gzip
    from datetime import datetime
    job = os.environ.get("SLURM_JOB_ID", "")
    lock = REPO / ".git" / "paperA_push.lock"
    t0 = time.time()
    while True:
        try:
            lock.mkdir()
            break
        except FileExistsError:
            if time.time() - lock.stat().st_mtime > 1800:
                shutil.rmtree(lock, ignore_errors=True)
                continue
            if time.time() - t0 > 7200:
                print("push: waited 2 h for the lock; results stay on scratch")
                return False
            time.sleep(15)
    try:
        dests = []
        for d in map(Path, run_dirs):
            if not d.exists():
                continue
            dest = REPO / RESULTS_DIR / d.name
            dest.mkdir(parents=True, exist_ok=True)
            for f in d.iterdir():
                if f.name == "es.pkl" or not f.is_file():
                    continue
                if f.name == "evals.csv":
                    with open(f, "rb") as fi, gzip.open(dest / "evals.csv.gz", "wb") as fo:
                        shutil.copyfileobj(fi, fo)
                elif f.stat().st_size < 20_000_000:
                    shutil.copy2(f, dest / f.name)
            log = REPO / f"joint_{os.environ.get('SLURM_JOB_NAME', 'Joint')}_{job}.log"
            if job and log.exists():
                keep = [ln for ln in log.read_text(errors="replace").splitlines()][-400:]
                (dest / "job_log.txt").write_text("\n".join(keep) + "\n")
            (dest / "summary.txt").write_text(f"run {d.name}\npushed {datetime.now():%Y-%m-%d %H:%M} (job {job or '-'})\n")
            dests.append(str(dest.relative_to(REPO)))
        if not dests:
            return False
        git = lambda *a: subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True)   # noqa: E731
        if not git("config", "user.email").stdout.strip():
            print("push: git user.email not set; results copied but not pushed")
            return False
        git("add", "--", *dests)
        git("commit", "-m", f"Paper A HPC results: {', '.join(Path(x).name for x in dests)}", "--", *dests)
        for attempt in range(3):
            git("pull", "--rebase", "--autostash", "origin", "main")
            if git("push", "origin", "HEAD:main").returncode == 0:
                print(f"push: {dests} pushed")
                return True
            time.sleep(30)
        print("push failed: push from the login node with 'git push'")
        return False
    finally:
        shutil.rmtree(lock, ignore_errors=True)


def _time_left():
    job = os.environ.get("SLURM_JOB_ID")
    if not job:
        return None
    try:
        out = subprocess.run(["squeue", "-h", "-j", job, "-o", "%L"], capture_output=True, text=True,
                             timeout=30).stdout.strip()
        days = 0
        if "-" in out:
            d, out = out.split("-", 1)
            days = int(d)
        parts = [int(x) for x in out.split(":")]
        while len(parts) < 3:
            parts.insert(0, 0)
        return days * 86400 + parts[0] * 3600 + parts[1] * 60 + parts[2]
    except Exception:
        return None


def run_test(est, env, workers, threads, code):
    t0 = time.time()
    root = Path(env["PAPERA_OUT"]) / "tests"
    root.mkdir(parents=True, exist_ok=True)
    env = dict(env, PAPERA_OUT=str(root))
    verdict = [("checks", True, "inputs, entry couples, commit")]
    print("\n== 2. objective at the analytic start", flush=True)
    r = subprocess.run(est + ["evaluate", "--threads", str(threads)], cwd=code, env=env, capture_output=True, text=True)
    print(r.stdout[-3000:], r.stderr[-2000:], flush=True)
    qs = re.findall(r"Q\(start\) = ([\d,.]+)", r.stdout)
    outs = re.findall(r"-> (.+evaluate_\S+)", r.stdout)
    if not qs:
        verdict.append(("reproducibility", False, "evaluation failed"))
    else:
        q = float(qs[0].replace(",", ""))
        d = q - EXPECTED_Q
        ok_q = abs(d) <= 1e-3 * abs(EXPECTED_Q)
        msg_m, ok_m = "expected moments file or evaluate output missing", False
        exp_p = code / EXPECTED_MOMENTS
        if outs and exp_p.exists():
            import csv
            pc = {row["id"]: float(row["sim"]) for row in csv.DictReader(open(exp_p))}
            hp = {row["id"]: float(row["sim"]) for row in csv.DictReader(open(Path(outs[-1].strip()) / "moments.csv"))}
            rel = [abs(hp[k] - v) / max(abs(v), 1e-12) for k, v in pc.items() if k in hp]
            ok_m = len(rel) == len(pc) and max(rel) <= 1e-6
            msg_m = f"max relative moment difference {max(rel):.1e} over {len(rel)} moments"
        verdict.append(("reproducibility", ok_m or ok_q,
                        f"{msg_m}; Q {q:,.1f} vs PC {EXPECTED_Q:,.1f} (relative {d / EXPECTED_Q:+.1e}; pass: moments "
                        f"within 1e-6 or Q within 1e-3; large = inputs / environment)"))
    print("\n== 3. short estimation (2 generations of 16)", flush=True)
    rf = Path(env.get("TMPDIR", "/tmp")) / f"paperA_test_run_{os.getpid()}.txt"
    env2 = dict(env, PAPERA_RUN_DIR_FILE=str(rf))
    subprocess.run(est + ["run", "--workers", str(workers), "--threads", str(threads), "--popsize", "16",
                          "--maxfevals", "32", "--label", "test"], cwd=code, env=env2)
    run_dir = Path(rf.read_text().strip()) if rf.exists() else None

    def n_evals(d):
        f = d / "evals.csv"
        return sum(1 for _ in open(f)) - 1 if f.exists() else 0

    # pycma runs the generation in which countevals reaches maxfevals and stops after it (32 / 16 -> 48 evaluations)
    n1 = n_evals(run_dir) if run_dir else 0
    ok3 = run_dir is not None and all((run_dir / f).exists() for f in ("run.json", "best.json", "es.pkl", "mean.json")) \
        and n1 >= 32 and n1 % 16 == 0
    verdict.append(("estimation", ok3, f"{run_dir} with {n1} evaluations (expected a multiple of 16, >= 32)"))
    print("\n== 4. resume (more generations)", flush=True)
    if run_dir is not None:
        subprocess.run(est + ["run", "--resume", str(run_dir), "--workers", str(workers), "--threads", str(threads),
                              "--extend-to", str(n1 + 16)], cwd=code, env=env)
    n2 = n_evals(run_dir) if run_dir else 0
    ok4 = run_dir is not None and n2 > n1 and n2 % 16 == 0
    verdict.append(("resume", ok4, f"{n2} evaluations after the resume (expected more than {n1})"))
    print("\n== 5. Levenberg-Marquardt polish (two free parameters, one iteration)", flush=True)
    rf.unlink(missing_ok=True)
    subprocess.run(est + ["polish", "--workers", str(workers), "--threads", str(threads), "--free", "delta_w_B",
                          "delta_w_W", "--iters", "1", "--se-reps", "2", "--label", "test"], cwd=code, env=env2)
    pdir = Path(rf.read_text().strip()) if rf.exists() else None
    ok5 = pdir is not None and all((pdir / f).exists() for f in ("best.json", "iterations.csv", "jacobian.npz",
                                                                   "report.md", "se.csv"))
    verdict.append(("polish", ok5, f"{pdir} with best.json, iterations.csv, jacobian.npz, report.md, se.csv"))
    print(f"\n== TEST RESULT ({(time.time() - t0) / 60:.1f} min)")
    for name, ok, msg in verdict:
        print(f"  {'PASS' if ok else 'FAIL'}  {name:16s} {msg}")
    return 0 if all(v[1] for v in verdict) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="run", choices=["run", "polish", "jacobian", "se", "noise",
                                                                   "evaluate"])
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--resume", default=None)
    ap.add_argument("--threads", type=int, default=2, help="numba threads per worker (never 64 cores without asking)")
    ap.add_argument("--popsize", type=int, default=16)
    ap.add_argument("--commit", default=None)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--push-only", dest="push_only", nargs="+", default=None)
    args, passthrough = ap.parse_known_args()
    if args.push_only:
        sys.exit(0 if push_results(args.push_only) else 1)
    cpus = int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count() or 1))
    threads = max(1, min(args.threads, cpus))
    workers = max(1, min(args.popsize, cpus // threads))
    mem_gb = int(os.environ.get("SLURM_MEM_PER_NODE", "0")) / 1024
    if mem_gb > 0:
        fit = max(1, int(0.92 * mem_gb / PEAK_GB) - 1)
        if fit < workers:
            print(f"WARNING memory: {mem_gb:.0f} GB fits {fit} workers of ~{PEAK_GB} GB, not {workers}", flush=True)
            workers = fit
    env = dict(os.environ)
    user = env.get("USER", "user")
    scratch = Path(f"/mnt/parscratch/users/{user}")
    env.setdefault("PAPERA_OUT", str((scratch if scratch.exists() else Path.home()) / "joint_smm_results"))
    Path(env["PAPERA_OUT"]).mkdir(parents=True, exist_ok=True)
    job = env.get("SLURM_JOB_ID", str(os.getpid()))
    env["NUMBA_CACHE_DIR"] = str(Path(env.get("TMPDIR", "/tmp")) / f"numba_paperA_{job}")
    env["PYTHONUNBUFFERED"] = "1"
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        env[v] = "1"
    checks()
    code, sha = code_snapshot(job, args.commit)
    print(f"code snapshot {sha[:7]} in {code}; job {job}: {cpus} cores -> {workers} workers x {threads} threads; "
          f"results in {env['PAPERA_OUT']}", flush=True)
    est = [sys.executable, "-u", str(code / MODEL / "estimate.py")]
    if args.test:
        rc = run_test(est, env, workers, threads, code)
        shutil.rmtree(code, ignore_errors=True)
        sys.exit(rc)
    if args.resume:
        cmd = est + ["run", "--resume", args.resume, "--workers", str(workers), "--threads", str(threads)] + passthrough
    else:
        cmd = est + [args.command, "--workers", str(workers), "--threads", str(threads)] + \
            (["--popsize", str(args.popsize)] if args.command == "run" else []) + passthrough
    rf = Path(env.get("TMPDIR", "/tmp")) / f"paperA_run_dir_{job}.txt"
    env["PAPERA_RUN_DIR_FILE"] = str(rf)
    print("running:", " ".join(cmd), flush=True)
    before = set(Path(env["PAPERA_OUT"]).glob("*"))
    left = _time_left()
    proc = subprocess.Popen(cmd, cwd=code, env=env, start_new_session=True)
    try:
        rc = proc.wait(timeout=max(60, left - 900) if left else None)
    except subprocess.TimeoutExpired:
        print("time limit near: stopping the run to push its results (resume with --resume)", flush=True)
        import signal
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=60)
        except Exception:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
        rc = 0
    if args.push:
        if args.resume:
            dirs = [args.resume]
        elif rf.exists():
            dirs = [rf.read_text().strip()]
        else:
            dirs = [str(p) for p in set(Path(env["PAPERA_OUT"]).glob("*")) - before if p.is_dir()]
        push_results(dirs)
    shutil.rmtree(code, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
