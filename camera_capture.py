import cv2
import os
from datetime import datetime #Working with dates and times
import time #Handling delays and timing

def test_camera_indices():
    """Test which camera index works (macOS safe)"""
    print("🔍 Testing camera indices (0–4)...")
    working = []
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)  # macOS backend
        if cap.isOpened():
            ret, frame = cap.read() # ret → a boolean (True/False) that says whether capturing worked. ,  frame → the actual image data captured from the camera.
            if ret and frame is not None: #The capture succeeded (ret is True), And an image (frame) was actually received.
                print(f"✅ Camera index {i} works!")
                working.append(i)
            cap.release()
        else:
            cap.release()
    return working

def capture_image():
    # Create output folder if needed
    folder = "captured_images"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Find a working camera
    indices = test_camera_indices()
    if not indices:
        print("\n❌ No working camera found.")
        print("➡ Check:")
        print("1. System Settings → Privacy & Security → Camera → Enable Python/VS Code")
        print("2. Quit and reopen VS Code")
        print("3. Or run from Terminal (not VS Code): python3 camera_capture.py")
        return

    cam_index = indices[0]
    print(f"\n📷 Using camera index: {cam_index}")

    # Initialize camera with macOS backend
    cam = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cam.isOpened():
        print("❌ Error: Could not open camera.")
        return

    time.sleep(1)
    print("\n✅ Camera started.")
    print("Press SPACE to capture, Q to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("⚠️ Frame not received.")
            break

        cv2.imshow("Camera (Press SPACE to capture, Q to quit)", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # SPACE
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(folder, f"image_{ts}.jpg")
            cv2.imwrite(filename, frame)
            print(f"💾 Saved: {filename}")
        elif key == ord('q') or key == 27:  # Q or ESC
            print("👋 Exiting...")
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_image()
