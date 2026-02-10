# look-forward

Author: jarvis  
Dependencies: none

Point the wrist camera forward and detect objects using YOLO.

## How It Works

Simple approach: rotate **J4 (elbow) by +30°** from home position. This tilts the wrist camera forward while keeping the arm in a safe configuration.

Two camera views available:
- **Wrist camera** (high view, ~0.6m height)
- **Base camera** (low view, fallback)

## Usage

```python
from main import run

# Run with defaults
result = run()

# Specify objects to look for  
result = run(objects="person, door, chair")

# Adjust the tilt angle
result = run(j4_delta_deg=45)  # More tilt = looks further down
```

## Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| objects | str | "person, chair, table, cup, ..." | Comma-separated YOLO prompts |
| j4_delta_deg | float | 30.0 | J4 rotation in degrees from home |
| confidence | float | 0.15 | YOLO detection threshold |
| use_base_cam | bool | True | Fall back to base camera if wrist fails |

## Returns

```python
{
    "detections": [{"class": "person", "confidence": 0.85, "bbox": [...]}],
    "count": 1,
    "camera_used": "309622300814",
    "ee_position": [0.57, 0.0, 0.61],
    "j4_delta_deg": 30.0
}
```

## Camera IDs

| Camera | ID | View |
|--------|-----|------|
| Wrist | 309622300814 | High (~0.6m), tilted forward |
| Base | 336222071022 | Low, fixed forward |

## Hardware Notes

- Home J4: -135° → After +30°: -105°
- Final EE height: ~0.61m (wrist camera elevated)
- Simple joint move = reliable, stays in workspace
- If wrist camera unavailable, falls back to base camera

## Tested

- 2026-02-10: J4 +30° approach works reliably on Tidybot
