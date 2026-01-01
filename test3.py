import pyautogui
import time
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional, Tuple
import threading


class VideoAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Automation Controller")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        self.is_running = False
        self.automation_thread = None
        self.cycle_count = 0

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Video Automation Controller",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Control buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start Automation",
            command=self.start_automation,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop Automation",
            command=self.stop_automation,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Status frame
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=5)

        tk.Label(status_frame, text="Status:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.status_label = tk.Label(
            status_frame,
            text="Idle",
            font=("Arial", 10),
            fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        tk.Label(status_frame, text="Cycles:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(20, 0))
        self.cycle_label = tk.Label(
            status_frame,
            text="0",
            font=("Arial", 10),
            fg="blue"
        )
        self.cycle_label.pack(side=tk.LEFT, padx=5)

        # Log area
        log_label = tk.Label(self.root, text="Logs:", font=("Arial", 10, "bold"))
        log_label.pack(anchor=tk.W, padx=10, pady=(10, 0))

        self.log_text = scrolledtext.ScrolledText(
            self.root,
            width=80,
            height=20,
            font=("Courier", 9),
            bg="#f5f5f5"
        )
        self.log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Clear log button
        clear_button = tk.Button(
            self.root,
            text="Clear Logs",
            command=self.clear_logs,
            font=("Arial", 9)
        )
        clear_button.pack(pady=5)

    def log(self, message: str, level: str = "INFO"):
        """Add a log message to the text area."""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}\n"

        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_logs(self):
        """Clear all logs."""
        self.log_text.delete(1.0, tk.END)

    def update_status(self, status: str, color: str = "black"):
        """Update the status label."""
        self.status_label.config(text=status, fg=color)

    def update_cycle_count(self):
        """Update the cycle count label."""
        self.cycle_label.config(text=str(self.cycle_count))

    def start_automation(self):
        """Start the automation process."""
        self.is_running = True
        self.cycle_count = 0
        self.update_cycle_count()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_status("Running", "green")

        self.log("Automation started - waiting 5 seconds before beginning...", "INFO")

        # Start automation in a separate thread
        self.automation_thread = threading.Thread(target=self.run_automation, daemon=True)
        self.automation_thread.start()

    def stop_automation(self):
        """Stop the automation process."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Stopped", "red")
        self.log(f"Automation stopped by user after {self.cycle_count} cycles", "INFO")

    def wait_for_image(self, image_path: str, confidence: float = 0.8,
                       timeout: int = 30, check_interval: float = 0.5) -> Optional[Tuple[int, int, int, int]]:
        """Wait for an image to appear on screen."""
        start_time = time.time()
        while time.time() - start_time < timeout and self.is_running:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    return location
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(check_interval)
        return None

    def click_center(self, location: Tuple[int, int, int, int]) -> None:
        """Click the center of a located image."""
        x, y, w, h = location
        pyautogui.click(x + w / 2, y + h / 2)

    def process_video(self) -> bool:
        """Process one video cycle."""
        try:
            # Click play button
            self.log("Looking for play button...")
            play_location = self.wait_for_image('play.png', confidence=0.8, timeout=30)
            if not play_location:
                self.log("Play button not found", "ERROR")
                return False

            self.log("Clicking play button")
            self.click_center(play_location)
            time.sleep(2)

            # Click fullscreen button
            self.log("Looking for fullscreen button...")
            fullscreen_location = self.wait_for_image('fullscreen.png', confidence=0.8, timeout=30)
            if not fullscreen_location:
                self.log("Fullscreen button not found", "ERROR")
                return False

            self.log("Clicking fullscreen button")
            self.click_center(fullscreen_location)

            # Wait for video to end
            self.log("Waiting for video to end...")
            out_location = self.wait_for_image('out.png', confidence=0.8, timeout=3600)
            if not out_location:
                self.log("Video end indicator not found within timeout", "ERROR")
                return False

            self.log("Video ended, pressing ESC")
            pyautogui.press('esc')
            time.sleep(2)

            # Click next button
            self.log("Looking for next button...")
            next_images = ["next1.png", "next2.png"]
            next_clicked = False

            for img in next_images:
                self.log(f"Trying to locate {img}...")
                next_location = self.wait_for_image(img, confidence=0.7, timeout=2)
                if next_location:
                    self.log(f"Found {img}, clicking")
                    self.click_center(next_location)
                    next_clicked = True
                    break

            if not next_clicked:
                self.log("No next button found", "WARNING")
                return False

            self.log("Video cycle completed successfully", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"Error in video processing: {e}", "ERROR")
            return False

    def run_automation(self):
        """Main automation loop."""
        time.sleep(5)

        while self.is_running:
            self.cycle_count += 1
            self.update_cycle_count()

            self.log("=" * 50)
            self.log(f"Starting cycle #{self.cycle_count}")
            self.log("=" * 50)

            success = self.process_video()

            if not success:
                self.log(f"Cycle #{self.cycle_count} failed. Retrying in 5 seconds...", "WARNING")
                time.sleep(5)
            else:
                self.log(f"Cycle #{self.cycle_count} completed successfully", "SUCCESS")
                time.sleep(2)

        self.log("Automation loop exited", "INFO")


def main():
    root = tk.Tk()
    app = VideoAutomationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()