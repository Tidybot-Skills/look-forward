"""
look-forward: Point wrist camera forward and detect objects.

Simple approach: rotate J4 (elbow) by +30° from home to tilt camera forward.
Captures from both wrist camera (high view) and base camera (low view).

Author: jarvis
"""
import math
from robot_sdk import arm, sensors, yolo


# Camera IDs
WRIST_CAM = "309622300814"
BASE_CAM = "336222071022"


def run(objects: str = "person, chair, table, cup, bottle, bag, monitor",
        j4_delta_deg: float = 30.0,
        confidence: float = 0.15,
        use_base_cam: bool = True):
    """
    Point the wrist camera forward and detect objects.
    
    Args:
        objects: Comma-separated list of objects to detect
        j4_delta_deg: How much to rotate J4 in degrees (default 30°)
        confidence: YOLO confidence threshold
        use_base_cam: If True, also capture from base camera (fallback if wrist fails)
    
    Returns:
        dict with detections and metadata
    """
    print("=== look-forward skill ===")
    
    # Step 1: Go home
    print("Going home...")
    arm.go_home()
    
    # Step 2: Rotate J4 to tilt camera forward
    joints = list(sensors.get_arm_joints())
    original_j4 = joints[3]
    joints[3] += math.radians(j4_delta_deg)
    
    print(f"Rotating J4: {math.degrees(original_j4):.1f}° → {math.degrees(joints[3]):.1f}° (+{j4_delta_deg}°)")
    arm.move_joints(joints, duration=3.0)
    
    ee_pos = sensors.get_ee_position()
    print(f"Camera at: x={ee_pos[0]:.2f}, y={ee_pos[1]:.2f}, z={ee_pos[2]:.2f}")
    
    # Step 3: Run YOLO detection
    print(f"Detecting: {objects}")
    
    # Try wrist camera first, fall back to base camera
    camera_used = WRIST_CAM
    try:
        result = yolo.segment_camera(
            text_prompt=objects,
            camera_id=WRIST_CAM,
            confidence=confidence,
            save_visualization=True
        )
    except Exception as e:
        if use_base_cam:
            print(f"Wrist camera failed ({e}), using base camera...")
            camera_used = BASE_CAM
            result = yolo.segment_camera(
                text_prompt=objects,
                camera_id=BASE_CAM,
                confidence=confidence,
                save_visualization=True
            )
        else:
            raise
    
    # Collect detections
    detections = []
    for det in result.detections:
        detections.append({
            "class": det.class_name,
            "confidence": round(det.confidence, 2),
            "bbox": det.bbox
        })
        print(f"  Found: {det.class_name} ({det.confidence:.0%})")
    
    if not detections:
        print("  No objects detected")
    
    # Step 4: Return home
    print("Returning home...")
    arm.go_home()
    
    print(f"=== Done ({len(detections)} objects) ===")
    
    return {
        "detections": detections,
        "count": len(detections),
        "camera_used": camera_used,
        "ee_position": list(ee_pos),
        "j4_delta_deg": j4_delta_deg
    }


if __name__ == "__main__":
    result = run()
    print(f"\nResult: {result}")
