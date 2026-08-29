# Data Directory

This directory contains all data used in the project, organized to support reproducibility and clear data provenance.

---

## Folder Structure
- `example_scenes/`
  - Vision-To-Text JSON examples for testing reasoning/action LLMs
- `raw/`
  - Original driving videos (unmodified). Currently has one synthetic test
    clip (`sample_construction_drive.mp4`, stitched from `frames/construction_test/`)
    for exercising `run_pipeline.py` end to end - swap in a real dashcam clip
    when available
- `frames/`
  - Extracted image frames from videos
- `annotations/`
  - Human-provided labels or expected actions (optional)

---

## Data Sources

Initial development may use:
- Publicly available dashcam or driving videos
- Curated clips from public platforms

Later stages should use:
- Public autonomous driving datasets (e.g., BDD100K, KITTI)

All data sources should be documented with:
- Source URL or dataset name
- License or usage terms
- Date of access


## Test Image URL:
https://www.istockphoto.com/photo/daytime-interstate-traffic-perspective-gm1361912866-434114689

Data Schema (produced by `vision_to_text.py`, also used for hand-authored test scenes):
{
  "observation": "",
  "scene_type": "",
  "frame_id": "",
  "road_type": "",
  "objects": [],
  "traffic_density": "",
  "lane_configuration": "",
  "traffic_control": [],
  "lane_changes": "",
  "hazards": [],
  "hazard_severity": "",
  "hazard_proximity": "",
  "path_status": "",
  "action_urgency": "",
  "merge_necessity": "",
  "visibility": "",
  "ego_vehicle_state": {
    "speed": "",
    "lane_position": ""
  }
}
