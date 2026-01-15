# SST_Autonomous_Driving: Self-Talk Reasoning for Explainable Autonomous Driving Decisions
This repo explores the use of **Safety Self-Talk (SST) based reasoning** to support explainable decision-making in autonomous driving scenarios. The project implements a modular Python pipeline that converts driving video frames into structured scene descriptions, applies an LLM-based self-talk reasoning process to interpret risk and intent, and outputs explicit driving decisions along with audience-specific explanations (car-to-self, car-to-passenger, car-to-car).

---

## High-Level Pipeline

1. Driving video input (rush hour, construction, accidents)
2. Frame extraction from video
3. Visual perception (image -> structured text)
4. SST reasoning (what is happening, risks, actions)
5. Decision extraction (explicit action output)
6. Communication generation (self / passenger / other vehicles)

---

## Project Plan

**Phase 1: Prototype**
- Curate a small set of driving videos
- Extract representative frames
- Generate scene descriptions using a vision-language model
- Apply SST prompts to reason about each scene
- Output structured decisions and explanations

**Phase 2: Refinement**
- Improve prompt consistency and determinism
- Add light human-expected action annotations
- Compare LLM decisions to human expectations

**Phase 3: Research Expansion**
- Replace videos with public driving datasets
- Expand communication modes
- Formalize evaluation metrics

---

## Repository Structure
SST_Autonomous_Driving/
├── data/ # videos, frames, annotations
├── src/ # core pipeline scripts
├── prompts/ # SST prompt templates
├── notebooks/ # exploratory analysis only
├── logs/ # outputs and experiment logs
├── docs/ # research notes and drafts

## Getting Started
1. Create a Python virtual environment
2. Install dependencies from `requirements.txt`
3. Place videos in `data/raw/videos`
4. Run scripts in `src/` in pipeline order