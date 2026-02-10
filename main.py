"""
look-forward: Point wrist camera forward and detect objects.

Moves the arm to position the wrist camera looking ahead (tilted ~40° from down),
runs YOLO object detection, and returns to home position.

Author: jarvis
"""
from robot_sdk import arm, sensors, yolo


def run(objects: str = "person, chair, table, cup, bottle, bag, backpack, monitor", 
        pitch_angle: float = 0.7,
        confidence: float = 0.15):
    """
    Point the wrist camera forward and detect objects.
    
    Args:
        objects: Comma-separated list of objects to detect
        pitch_angle: EE pitch angle in radians (default 0.7 = ~40°, max safe ~0.7)
        confidence: YOLO confidence threshold (default 0.15)
    
    Returns:
        dict with 'detections' list and metadata
    """
    print("=== look-forward skill ===")
    
    # Step 1: Go home
    print("Going home...")
    arm.go_home()
    
    # Step 2: Extend forward and lower slightly
    print("Positioning arm...")
    arm.move_delta(dx=0.15, dz=-0.1, duration=2.5)
    
    # Step 3: Pitch up to tilt camera forward
    print(f"Tilting camera forward ({pitch_angle:.1f} rad)...")
    arm.move_delta(dpitch=pitch_angle, duration=3.0)
    
    # Get camera position
    ee_pos = sensors.get_ee_position()
    print(f"Camera at: x={ee_pos[0]:.3f}, y={ee_pos[1]:.3f}, z={ee_pos[2]:.3f}")
    
    # Step 4: Run YOLO detection on wrist camera
    print(f"Detecting: {objects}")
    wrist_camera_id = "309622300814"
    
    result = yolo.segment_camera(
        text_prompt=objects,
        camera_id=wrist_camera_id,
        confidence=confidence,
        save_visualization=True
    )
    
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
    else:
        print(f"[YOLO] {len(detections)} object(s) detected")
    
    # Step 5: Return home
    print("Returning home...")
    arm.go_home()
    
    print("=== Done ===")
    
    return {
        "detections": detections,
        "count": len(detections),
        "objects_searched": objects,
        "ee_position": list(ee_pos),
        "pitch_angle": pitch_angle
    }


if __name__ == "__main__":
    result = run()
    print(f"\nResult: {result}")
