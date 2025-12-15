# Deepfakes_Detection_dataset

This repository contains the data and documentation for a two-phase study investigating the impact of an educational video on human deepfake detection performance and response bias.

## 1. Study Design Overview (Two-Phase Survey)

This study utilized a two-phase survey design to assess detection performance against deepfakes, administered via Google Forms.

### Phase I (Baseline)

This phase established baseline detection ability and gathered qualitative ethical viewpoints.

| Category | Details |
| :--- | :--- |
| **Media Items** | $\mathbf{10}$ total items: $\mathbf{6}$ Images (created via remaker.ai faceswap) and $\mathbf{4}$ Audios (created via elevenlabs.io voice cloning). |
| **Detection Questions** | For each item: |
| | 1. How aware are you of the context? (Likert scale) |
| | 2. Do you think the item is a deepfake? ($\mathbf{Binary}$) |
| **Ethical Questions (Subjective)** | $\mathbf{5}$ open-ended questions covering ethical perspectives: |
| | 1. Do you think the use of deepfake technology should be regulated by law? Why or why not? |
| | 2. In what situations (if any) do you believe deepfake technology can be ethically used? |
| | 3. Can deepfake technology be a tool for creativity and innovation? Where do you draw the line between ethical and unethical use? |
| | 4. What could be some advantages of using deepfakes, given a specific context? Give examples. |
| | 5. According to you what are some serious negative consequences of using deepfakes? Give examples. |
| **Demographics** | Name, age, gender, and Email ID were collected but have been removed from the published dataset to maintain participant privacy. |

### Phase II (Intervention)

This phase measured the effect of the intervention on detection performance.

| Category | Details |
| :--- | :--- |
| **Intervention** | Participants first viewed a short video on how to detect deepfakes ([Video Link](https://www.youtube.com/watch?v=tfMmhyE8DxY)). |
| **Media Items** | $\mathbf{15}$ total items: $\mathbf{9}$ Images and $\mathbf{6}$ Audios (a new set of stimuli). |
| **Detection Questions** | For each item: |
| | 1. How aware are you of the context? (Likert scale) |
| | 2. Do you think the item is a deepfake? ($\mathbf{Binary}$) |
| | 3. Give a brief reason for what gave it away (qualitative text response). |

## 3. Score Calculation

Scores in both Phase I and Phase II were calculated based on the correctness of the **binary detection response** ("Do you think the item is a deepfake?") against the established Ground Truth.

| Outcome | Criteria | Score |
| :--- | :--- | :--- |
| **Correct Response** | Participant's binary answer matched the Ground Truth (Real/Deepfake). | $\mathbf{1}$ |
| **Incorrect Response** | Participant's binary answer failed to match the Ground Truth. | $\mathbf{0}$ |

The total score for each participant is the sum of these correctness scores across all media items in that form ($\mathbf{\text{out of } 10}$ in Phase I, and $\mathbf{\text{out of } 15}$ in Phase II). In the Baseline Form (Phase 1), Name, age, gender, Email Id were also asked, but have been removed due to privacy concerns.
