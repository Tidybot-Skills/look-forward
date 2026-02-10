# look-forward

Author: jarvis  
Dependencies: none

Point the wrist camera forward and detect objects using YOLO.

## What It Does

1. Moves arm to home position
2. Extends forward (dx=0.15m) and lowers slightly (dz=-0.1m)
3. Pitches the end-effector up ~40° so wrist camera looks ahead
4. Runs YOLO object detection on wrist camera
5. Returns to home position

## Usage

```python
from main import run

# Run with defaults
result = run()
# Returns: {"detections": [...], "count": 1, "ee_position": [...], ...}

# Specify objects to look for
result = run(objects="person, door, chair")

# Adjust pitch (0.7 rad is max safe value)
result = run(pitch_angle=0.5)
```

## Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| objects | str | "person, chair, table, cup, bottle, bag, backpack, monitor" | Comma-separated YOLO prompts |
| pitch_angle | float | 0.7 | EE pitch in radians (~40°). Max safe: 0.7 |
| confidence | float | 0.15 | YOLO detection threshold |

## Returns

```python
{
    "detections": [{"class": "person", "confidence": 0.22, "bbox": [...]}],
    "count": 1,
    "objects_searched": "person, chair, ...",
    "ee_position": [0.60, 0.0, 0.14],
    "pitch_angle": 0.7
}
```

## Hardware Notes

- **Wrist camera**: 309622300814 (RealSense, on inner wrist)
- Camera faces -Z in EE frame; at home it looks straight down
- Pitching EE tilts camera view forward
- **Max pitch ~0.7 rad** — higher values hit workspace limits
- Final EE position: ~(0.60, 0, 0.14) in world frame
- View is tilted ~40° from vertical — catches floor + objects ahead

## Visualization

YOLO saves annotated image to `GET /yolo/visualization` on the robot API.

## Tested

- 2026-02-10: Works on Tidybot (Franka + mobile base)
- Detected person at 22% confidence
