"""
Deepfake Detection Study — Reproducible Analysis
==================================================
Reproduces every corrected table and statistic reported in the manuscript
(Tables 3-14) directly from the raw survey exports.

Inputs expected in the same directory as this script:
  - "Anonymous Responses.csv"      (Phase I raw responses, Form 1)
  - "Anonymous_Responses.csv"      (Phase II raw responses, Form 2)
  - "Correct Answers.xlsx"         (Phase I ground truth, in Form 1 folder)
  - "Correct Answers.xlsx"         (Phase II ground truth, in Form 2 folder)
  - "qualitative_ethics_coding.csv" (human-coded ethics variables, Q1-Q4)

Requires: numpy, scipy. (pandas not required.)
"""
import csv
import numpy as np
from scipy.stats import norm, chi2_contingency

# ---------------------------------------------------------------------------
# 1. Load Phase I raw responses and ground truth
# ---------------------------------------------------------------------------
PHASE1_CSV = "Anonymous Responses.csv"      # Form 1 export
PHASE2_CSV = "Anonymous_Responses.csv"      # Form 2 export

GT_IMAGE_P1 = {1: 'D', 2: 'D', 3: 'D', 4: 'D', 5: 'R', 6: 'R'}
GT_AUDIO_P1 = {1: 'D', 2: 'D', 3: 'R', 4: 'R'}
GT_IMAGE_P2 = {1: 'D', 2: 'R', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'R', 9: 'D'}
GT_AUDIO_P2 = {1: 'D', 2: 'R', 3: 'D', 4: 'R', 5: 'R', 6: 'D'}

IMAGE_STARTS_P1 = [1, 7, 13, 19, 25, 31]
AUDIO_STARTS_P1 = [37, 43, 49, 55]
STARTS_P2 = [1 + 9 * i for i in range(15)]


def parse_awareness(v):
    v = v.strip().lower()
    if 'highly' in v:
        return 2
    if 'moderate' in v:
        return 1
    return 0


def load_phase1(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        rows = list(csv.reader(f))[1:]
    participants = []
    for i, row in enumerate(rows):
        score = float(row[0].split('/')[0].strip())
        items = []
        for j, start in enumerate(IMAGE_STARTS_P1):
            items.append(dict(media='image', gt=GT_IMAGE_P1[j + 1],
                               yes=row[start + 3].strip().lower() == 'yes',
                               awareness=parse_awareness(row[start])))
        for j, start in enumerate(AUDIO_STARTS_P1):
            items.append(dict(media='audio', gt=GT_AUDIO_P1[j + 1],
                               yes=row[start + 3].strip().lower() == 'yes',
                               awareness=parse_awareness(row[start])))
        participants.append(dict(pid=f"P1_{i}", score=score, items=items))
    return participants


def load_phase2(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        rows = list(csv.reader(f))[1:]
    gts = [(GT_IMAGE_P2[i], 'image') for i in range(1, 10)] + \
          [(GT_AUDIO_P2[i], 'audio') for i in range(1, 7)]
    participants = []
    for i, row in enumerate(rows):
        items = []
        for j, start in enumerate(STARTS_P2):
            gt, media = gts[j]
            items.append(dict(media=media, gt=gt,
                               yes=row[start + 3].strip().lower() == 'yes',
                               awareness=parse_awareness(row[start])))
        resp_pattern = tuple(row[s + 3].strip() for s in STARTS_P2)
        participants.append(dict(pid=f"P2_{i}", items=items,
                                  straightliner=len(set(resp_pattern)) == 1))
    return participants


def confusion(participants, items_filter=None):
    h = m = fa = cr = 0
    for p in participants:
        for it in p['items']:
            if items_filter and not items_filter(it):
                continue
            signal = it['gt'] == 'D'
            if signal and it['yes']:
                h += 1
            elif signal and not it['yes']:
                m += 1
            elif not signal and it['yes']:
                fa += 1
            else:
                cr += 1
    return h, m, fa, cr


def sdt_metrics(h, m, fa, cr, correction=True):
    tf, tr = h + m, fa + cr
    if correction:
        hr_c, far_c = (h + 0.5) / (tf + 1), (fa + 0.5) / (tr + 1)
    else:
        hr_c, far_c = h / tf, fa / tr
    d = norm.ppf(hr_c) - norm.ppf(far_c)
    c = -0.5 * (norm.ppf(hr_c) + norm.ppf(far_c))
    return dict(hr=h / tf, mr=m / tf, far=fa / tr, crr=cr / tr, d=d, c=c, tf=tf, tr=tr)


# ---------------------------------------------------------------------------
# 2. Phase I full-cohort baseline (Tables 3-5)
# ---------------------------------------------------------------------------
p1 = load_phase1(PHASE1_CSV)
print(f"Phase I: N = {len(p1)}")

h, m, fa, cr = confusion(p1)
print("Table 5 (Phase I, full N=268):", sdt_metrics(h, m, fa, cr))

# Table 3: accuracy by context-awareness level
aware_labels = {0: 'Not Aware', 1: 'Moderately Aware', 2: 'Highly Aware'}
aware_tab = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
for p in p1:
    for it in p['items']:
        correct = (it['gt'] == 'D') == it['yes']
        aware_tab[it['awareness']][0] += int(correct)
        aware_tab[it['awareness']][1] += 1
print("Table 3 (accuracy by awareness):")
for k, (c_, n_) in aware_tab.items():
    print(f"  {aware_labels[k]}: {c_}/{n_} = {100*c_/n_:.2f}%")

# Table 6: eligible (<=7) vs excluded (>7) subgroups
eligible = [p for p in p1 if p['score'] <= 7]
excluded = [p for p in p1 if p['score'] > 7]
print(f"\nTable 6: eligible n={len(eligible)}, excluded n={len(excluded)}")
print("  Eligible:", sdt_metrics(*confusion(eligible)))
print("  Excluded:", sdt_metrics(*confusion(excluded)))

# ---------------------------------------------------------------------------
# 3. Phase II (Tables 7-9)
# ---------------------------------------------------------------------------
p2 = load_phase2(PHASE2_CSV)
print(f"\nPhase II: N = {len(p2)} (straight-liners: {sum(p['straightliner'] for p in p2)})")
print("Table 7 (Phase II, full N=181):", sdt_metrics(*confusion(p2)))
print("Table 7 (Phase II, cleaned N=178):", sdt_metrics(*confusion([p for p in p2 if not p['straightliner']])))

# Table 9: eligible Phase I vs Phase II, two-proportion z-tests + bootstrap CI for d'/c
def two_prop_z(x1, n1, x2, n2):
    p1_, p2_ = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2_ - p1_) / se
    return z, 2 * (1 - norm.cdf(abs(z)))


h1, m1, fa1, cr1 = confusion(eligible)
h2, m2, fa2, cr2 = confusion(p2)
print("\nTable 9 (eligible Phase I vs Phase II):")
for label, (x1, n1, x2, n2) in {
    'HR': (h1, h1 + m1, h2, h2 + m2), 'FAR': (fa1, fa1 + cr1, fa2, fa2 + cr2),
}.items():
    z, pval = two_prop_z(x1, n1, x2, n2)
    print(f"  {label}: z={z:.2f} p={pval:.4g}")

rng = np.random.default_rng(0)
def boot_dc(h, m, fa, cr, B=3000):
    tf, tr = h + m, fa + cr
    ds, cs = [], []
    for _ in range(B):
        hb = rng.binomial(tf, h / tf)
        fab = rng.binomial(tr, fa / tr)
        hr_c, far_c = (hb + 0.5) / (tf + 1), (fab + 0.5) / (tr + 1)
        ds.append(norm.ppf(hr_c) - norm.ppf(far_c))
        cs.append(-0.5 * (norm.ppf(hr_c) + norm.ppf(far_c)))
    return np.array(ds), np.array(cs)

d_elig, c_elig = boot_dc(h1, m1, fa1, cr1)
d_p2, c_p2 = boot_dc(h2, m2, fa2, cr2)
print(f"  d' eligible: {d_elig.mean():.3f} [{np.percentile(d_elig,2.5):.3f}, {np.percentile(d_elig,97.5):.3f}]")
print(f"  d' Phase II: {d_p2.mean():.3f} [{np.percentile(d_p2,2.5):.3f}, {np.percentile(d_p2,97.5):.3f}]")
print(f"  c eligible:  {c_elig.mean():.3f} [{np.percentile(c_elig,2.5):.3f}, {np.percentile(c_elig,97.5):.3f}]")
print(f"  c Phase II:  {c_p2.mean():.3f} [{np.percentile(c_p2,2.5):.3f}, {np.percentile(c_p2,97.5):.3f}]")

# ---------------------------------------------------------------------------
# 4. Table 10: cluster-robust logistic model
# ---------------------------------------------------------------------------
def build_design(participants, phase_val):
    X_rows, y_rows, cluster_ids = [], [], []
    for p in participants:
        for it in p['items']:
            X_rows.append([1.0, it['awareness'], phase_val, 1.0 if it['media'] == 'audio' else 0.0])
            y_rows.append(1.0 if (it['gt'] == 'D') == it['yes'] else 0.0)
            cluster_ids.append(p['pid'])
    return np.array(X_rows), np.array(y_rows), np.array(cluster_ids)

X1, y1, c1 = build_design(eligible, 0.0)
X2, y2, c2 = build_design(p2, 1.0)
X = np.vstack([X1, X2]); y = np.concatenate([y1, y2]); pid_arr = np.concatenate([c1, c2])
uniq = {p: i for i, p in enumerate(sorted(set(pid_arr)))}
pid_idx = np.array([uniq[p] for p in pid_arr])

beta = np.zeros(X.shape[1])
for _ in range(50):
    eta = X @ beta
    p_hat = 1 / (1 + np.exp(-eta))
    W = np.clip(p_hat * (1 - p_hat), 1e-8, None)
    step = np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (y - p_hat))
    if np.max(np.abs(step)) < 1e-10:
        break
    beta += step
eta = X @ beta; p_hat = 1 / (1 + np.exp(-eta)); W = np.clip(p_hat * (1 - p_hat), 1e-8, None)
bread = np.linalg.inv(X.T @ (X * W[:, None]))
resid = y - p_hat
meat = np.zeros((X.shape[1], X.shape[1]))
for g in set(pid_idx):
    idx = pid_idx == g
    sg = X[idx].T @ resid[idx]
    meat += np.outer(sg, sg)
n, k, G = len(y), X.shape[1], len(set(pid_idx))
sandwich = bread @ meat @ bread * (G / (G - 1)) * ((n - 1) / (n - k))
cluster_se = np.sqrt(np.diag(sandwich))
print("\nTable 10 (cluster-robust logistic model):")
for i, name in enumerate(['Intercept', 'Awareness', 'Phase(post)', 'Media(audio)']):
    z = beta[i] / cluster_se[i]
    print(f"  {name}: OR={np.exp(beta[i]):.3f} p={2*(1-norm.cdf(abs(z))):.4g}")

# ---------------------------------------------------------------------------
# 5. Table 11: awareness-accuracy correlation, before vs after
# ---------------------------------------------------------------------------
from scipy.stats import pearsonr
def per_participant_awareness_accuracy(participants):
    aw, acc = [], []
    for p in participants:
        correct = [int((it['gt'] == 'D') == it['yes']) for it in p['items']]
        awa = [it['awareness'] for it in p['items']]
        acc.append(np.mean(correct)); aw.append(np.mean(awa))
    return np.array(aw), np.array(acc)

aw1, acc1 = per_participant_awareness_accuracy(eligible)
aw2, acc2 = per_participant_awareness_accuracy(p2)
r1, pv1 = pearsonr(aw1, acc1)
r2, pv2 = pearsonr(aw2, acc2)
print(f"\nTable 11: r(awareness,accuracy) eligible={r1:.3f} (p={pv1:.3g}); Phase II={r2:.3f} (p={pv2:.3g})")

# ---------------------------------------------------------------------------
# 6. Tables 12-14: qualitative chi-square tests (human-coded data)
# ---------------------------------------------------------------------------
QUAL_CSV = "qualitative_ethics_coding.csv"
with open(QUAL_CSV, encoding='utf-8') as f:
    qual = list(csv.DictReader(f))

def valid(row, *cols):
    return all(row[c] and 'Invalid' not in row[c] for c in cols)

def two_by_two(rowcol, colcol, row_cats, col_cats):
    mat = np.zeros((2, 2), dtype=int)
    for row in qual:
        if not valid(row, rowcol, colcol):
            continue
        r_, c_ = row[rowcol], row[colcol]
        if r_ not in row_cats or c_ not in col_cats:
            continue
        mat[row_cats.index(r_), col_cats.index(c_)] += 1
    return mat

m_h1 = two_by_two('q3_code', 'q4_code', ['Ethical Realist', 'Innovation Optimist'],
                   ['Commercial/Entertainment', 'Educational/Societal'])
m_h2 = two_by_two('q2_code', 'q3_code', ['Highly Restrictive', 'Broadly Permissive'],
                   ['Ethical Realist', 'Innovation Optimist'])
m_h3 = two_by_two('q1_code', 'q3_code', ['Conditional/Skeptic', 'Strict Regulatory Advocate'],
                   ['Ethical Realist', 'Innovation Optimist'])

print("\nTables 12-14 (qualitative chi-square tests, human-coded):")
for name, mat in [('Table 12', m_h1), ('Table 13', m_h2), ('Table 14', m_h3)]:
    chi2, pval, dof, exp = chi2_contingency(mat, correction=True)
    v = np.sqrt(chi2 / mat.sum())
    print(f"  {name}: {mat.tolist()}  chi2={chi2:.3f} p={pval:.4f} CramersV={v:.3f}")
