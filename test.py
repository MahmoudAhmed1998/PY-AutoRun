import pyautogui
import time
from typing import Optional, Tuple


def wait_for_image(image_path: str, confidence: float = 0.8, timeout: int = 30, check_interval: float = 0.5) -> \
Optional[Tuple[int, int, int, int]]:
    """
    Wait for an image to appear on screen.

    Args:
        image_path: Path to the image file
        confidence: Confidence level for image matching (0-1)
        timeout: Maximum time to wait in seconds
        check_interval: Time between checks in seconds

    Returns:
        Tuple of (x, y, width, height) if found, None if timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return location
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(check_interval)
    return None


def click_center(location: Tuple[int, int, int, int]) -> None:
    """Click the center of a located image."""
    x, y, w, h = location
    pyautogui.click(x + w / 2, y + h / 2)


def process_video() -> bool:
    """
    Process one video cycle.

    Returns:
        True if successful, False if any error occurred
    """
    try:
        # Click play button
        print("Looking for play button...")
        play_location = wait_for_image('play.png', confidence=0.8, timeout=30)
        if not play_location:
            print("Error: Play button not found")
            return False

        print("Clicking play button")
        click_center(play_location)
        time.sleep(2)

        # Click fullscreen button
        print("Looking for fullscreen button...")
        fullscreen_location = wait_for_image('fullscreen.png', confidence=0.8, timeout=30)
        if not fullscreen_location:
            print("Error: Fullscreen button not found")
            return False

        print("Clicking fullscreen button")
        click_center(fullscreen_location)

        # Wait for video to end
        print("Waiting for video to end...")
        out_location = wait_for_image('out.png', confidence=0.8, timeout=3600)  # 1 hour max
        if not out_location:
            print("Error: Video end indicator not found within timeout")
            return False

        print("Video ended, pressing ESC")
        pyautogui.press('esc')
        time.sleep(2)

        # Click next button
        print("Looking for next button...")
        next_images = ["next1.png", "next2.png"]
        next_clicked = False

        for img in next_images:
            print(f"Trying to locate {img}...")
            next_location = wait_for_image(img, confidence=0.7, timeout=2)
            if next_location:
                print(f"Found {img}, clicking")
                click_center(next_location)
                next_clicked = True
                break

        if not next_clicked:
            print("Warning: No next button found")
            return False

        print("Video cycle completed successfully")
        return True

    except Exception as e:
        print(f"Error in video processing: {e}")
        return False


def main():
    print("Starting automation in 5 seconds...")
    print("Press Ctrl+C to stop the loop at any time")
    time.sleep(5)

    cycle_count = 0

    try:
        while True:
            cycle_count += 1
            print(f"\n{'=' * 50}")
            print(f"Starting cycle #{cycle_count}")
            print(f"{'=' * 50}\n")

            success = process_video()

            if not success:
                print(f"\nCycle #{cycle_count} failed. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"\nCycle #{cycle_count} completed successfully")
                time.sleep(2)  # Brief pause before next cycle

    except KeyboardInterrupt:
        print(f"\n\nAutomation stopped by user after {cycle_count} cycles")
        print("Exiting gracefully...")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")
        print(f"Stopped after {cycle_count} cycles")


if __name__ == "__main__":
    main()