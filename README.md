# Deepfakes Detection Dataset

This repository contains the data, human-coded qualitative labels, and reproducible analysis
code for a two-phase study investigating human deepfake detection performance, the effect of
an educational intervention on detection behaviour, and youth perceptions of deepfake ethics
and regulation.

## 1. Study Design Overview (Two-Phase Survey)

This study used a two-phase survey design, administered via Google Forms, to assess detection
performance against deepfakes and to test the effect of a brief educational intervention.

### Phase I (Baseline)

This phase established baseline detection ability and gathered qualitative ethical viewpoints.

| Category | Details |
| :--- | :--- |
| **Participants** | N = 268 currently enrolled students at IIIT Bangalore. Participants who took part in an earlier pilot survey (run to calibrate the Phase II eligibility threshold and refine the assessment items) were excluded from this main sample. |
| **Media Items** | 10 total items: 6 Images (created via remaker.ai faceswap) and 4 Audios (created via elevenlabs.io voice cloning). |
| **Detection Questions** | For each item: (1) How aware are you of the context? (2) Do you think the item is a deepfake? (binary) |
| **Ethical Questions (Subjective)** | 5 open-ended questions covering ethical perspectives (regulation, permissible use-cases, creativity/innovation, advantages, disadvantages) — see `qualitative_ethics_coding.csv` for the coded variables. |
| **Demographics** | Name, age, gender, and email were collected but have been removed from the published dataset to protect participant privacy. |

### Phase II (Intervention)

Participants who scored **≤ 7 out of 10** in Phase I were invited to Phase II. This threshold
was set following the pilot survey referenced above, which indicated that a score at or below
this level reliably identified participants who would benefit from the educational intervention.

| Category | Details |
| :--- | :--- |
| **Intervention** | Participants viewed a short educational video on deepfake detection ([Video Link](https://www.youtube.com/watch?v=tfMmhyE8DxY)), created with InVideo. |
| **Media Items** | 15 total items: 9 Images and 6 Audios (a new, separate stimulus set). |
| **Detection Questions** | Same as Phase I, plus a free-text "what gave it away" question. |
| **Responses** | 181 valid, non-duplicate responses were received. Three respondents answered "Yes" to every item (straight-lining) and are flagged in the raw data; results are reported both with and without this exclusion (N = 178), with no material difference in conclusions. |

Because both forms were collected anonymously with no participant identifier, Phase I and
Phase II responses cannot be linked at the individual level. All comparisons between the two
phases are therefore independent-samples comparisons of a defined, disclosed population (the
≤ 7/10 scorers in Phase I vs. the Phase II respondents), not paired pre/post measurements.

## 2. Score Calculation

Scores in both phases were calculated from the binary detection response ("Do you think the
item is a deepfake?") against ground truth, given in each form folder's `Correct Answers.xlsx`.

| Outcome | Criteria | Score |
| :--- | :--- | :--- |
| **Correct Response** | Participant's binary answer matched the ground truth (Real/Deepfake). | 1 |
| **Incorrect Response** | Participant's binary answer did not match the ground truth. | 0 |

Total score per participant is the sum of correctness across all items (out of 10 in Phase I,
out of 15 in Phase II).

## 3. Qualitative Ethics Coding

The five open-ended ethics questions in Phase I were manually coded into four binary thematic
variables to allow statistical testing:

| Variable | Categories |
| :--- | :--- |
| Q1 — Regulatory Advocacy | Strict Regulatory Advocate / Conditional-Skeptic |
| Q2 — Permissiveness | Broadly Permissive / Highly Restrictive |
| Q3 — Creativity Perception | Innovation Optimist / Ethical Realist |
| Q4 — Perceived Uses | Educational/Societal / Commercial/Entertainment |

The raw text responses and their coded labels are provided in `qualitative_ethics_coding.csv`.

## 4. Repository Contents

```
Dataset deepfakes/
  Form 1 - Deepfake Detection and Ethical Considerations in Digital Media/
    Anonymous Responses.csv      # Phase I raw responses (N=268)
    Correct Answers.xlsx         # Phase I ground truth
  Form 2 - Re-test form/
    Anonymous_Responses.csv      # Phase II raw responses (N=181)
    Correct Answers.xlsx         # Phase II ground truth
qualitative_ethics_coding.csv    # Human-coded ethics variables (Q1-Q4), all 268 participants
reproduce_analysis.py            # Reproduces every table in the manuscript from raw data
README.md
```

## 5. Reproducing the Analysis

`reproduce_analysis.py` recomputes every reported table (detection accuracy by context
awareness, Signal Detection Theory metrics, the cluster-robust logistic model, and the
qualitative chi-square tests) directly from the raw CSVs above. Requires Python 3 with
`numpy` and `scipy`:

```bash
pip install numpy scipy
python3 reproduce_analysis.py
```
