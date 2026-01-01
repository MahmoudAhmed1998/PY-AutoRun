import pyautogui
import time
import tkinter as tk
from tkinter import scrolledtext, ttk
from typing import Optional, Tuple
import threading


class VideoAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Automation Controller")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        self.is_running = False
        self.automation_thread = None
        self.cycle_count = 0
        self.none_video_count = 0

        # Color scheme
        self.colors = {
            'primary': '#2196F3',
            'success': '#4CAF50',
            'danger': '#f44336',
            'warning': '#FF9800',
            'bg': '#f0f0f0',
            'card': '#ffffff',
            'text': '#333333',
            'text_light': '#666666'
        }

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header Section
        header_frame = tk.Frame(main_container, bg=self.colors['card'], relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        header_content = tk.Frame(header_frame, bg=self.colors['card'])
        header_content.pack(pady=20)

        title_label = tk.Label(
            header_content,
            text="🎬 Video Automation Controller",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_content,
            text="Automated video playback and navigation",
            font=("Segoe UI", 10),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        )
        subtitle_label.pack(pady=(5, 0))

        # Control Panel
        control_frame = tk.Frame(main_container, bg=self.colors['card'], relief=tk.FLAT)
        control_frame.pack(fill=tk.X, pady=(0, 20))

        control_inner = tk.Frame(control_frame, bg=self.colors['card'])
        control_inner.pack(pady=20, padx=20)

        # Buttons with modern styling
        button_container = tk.Frame(control_inner, bg=self.colors['card'])
        button_container.pack()

        self.start_button = tk.Button(
            button_container,
            text="▶ Start Automation",
            command=self.start_automation,
            bg=self.colors['success'],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=18,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#45a049"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            button_container,
            text="⬛ Stop Automation",
            command=self.stop_automation,
            bg=self.colors['danger'],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            width=18,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            activebackground="#da190b"
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Statistics Cards
        stats_frame = tk.Frame(main_container, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))

        # Status Card
        status_card = tk.Frame(stats_frame, bg=self.colors['card'], relief=tk.FLAT)
        status_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        status_content = tk.Frame(status_card, bg=self.colors['card'])
        status_content.pack(pady=15, padx=20)

        tk.Label(
            status_content,
            text="Status",
            font=("Segoe UI", 9),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack()

        self.status_label = tk.Label(
            status_content,
            text="Idle",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg="#999999"
        )
        self.status_label.pack(pady=(5, 0))

        # Cycles Card
        cycles_card = tk.Frame(stats_frame, bg=self.colors['card'], relief=tk.FLAT)
        cycles_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        cycles_content = tk.Frame(cycles_card, bg=self.colors['card'])
        cycles_content.pack(pady=15, padx=20)

        tk.Label(
            cycles_content,
            text="Total Cycles",
            font=("Segoe UI", 9),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack()

        self.cycle_label = tk.Label(
            cycles_content,
            text="0",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['primary']
        )
        self.cycle_label.pack(pady=(5, 0))

        # None Videos Card
        none_card = tk.Frame(stats_frame, bg=self.colors['card'], relief=tk.FLAT)
        none_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        none_content = tk.Frame(none_card, bg=self.colors['card'])
        none_content.pack(pady=15, padx=20)

        tk.Label(
            none_content,
            text="Skipped Videos",
            font=("Segoe UI", 9),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack()

        self.none_video_label = tk.Label(
            none_content,
            text="0",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['card'],
            fg=self.colors['warning']
        )
        self.none_video_label.pack(pady=(5, 0))

        # Log Section
        log_frame = tk.Frame(main_container, bg=self.colors['card'], relief=tk.FLAT)
        log_frame.pack(fill=tk.BOTH, expand=True)

        log_header = tk.Frame(log_frame, bg=self.colors['card'])
        log_header.pack(fill=tk.X, pady=(15, 0), padx=20)

        tk.Label(
            log_header,
            text="Activity Log",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)

        clear_button = tk.Button(
            log_header,
            text="🗑 Clear",
            command=self.clear_logs,
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=5
        )
        clear_button.pack(side=tk.RIGHT)

        # Log text area with custom styling
        log_container = tk.Frame(log_frame, bg=self.colors['card'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))

        self.log_text = scrolledtext.ScrolledText(
            log_container,
            width=80,
            height=15,
            font=("Consolas", 9),
            bg="#fafafa",
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground="#e0e0e0",
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Configure tags for colored log messages
        self.log_text.tag_config("INFO", foreground="#2196F3")
        self.log_text.tag_config("SUCCESS", foreground="#4CAF50", font=("Consolas", 9, "bold"))
        self.log_text.tag_config("WARNING", foreground="#FF9800")
        self.log_text.tag_config("ERROR", foreground="#f44336", font=("Consolas", 9, "bold"))

    def log(self, message: str, level: str = "INFO"):
        """Add a log message to the text area with color coding."""
        timestamp = time.strftime("%H:%M:%S")

        # Insert timestamp
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")

        # Insert level with tag
        self.log_text.insert(tk.END, f"[{level}] ", level)

        # Insert message
        self.log_text.insert(tk.END, f"{message}\n")

        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_logs(self):
        """Clear all logs."""
        self.log_text.delete(1.0, tk.END)
        self.log("Logs cleared", "INFO")

    def update_status(self, status: str, color: str = "black"):
        """Update the status label."""
        self.status_label.config(text=status, fg=color)

    def update_cycle_count(self):
        """Update the cycle count label."""
        self.cycle_label.config(text=str(self.cycle_count))

    def update_none_video_count(self):
        """Update the none video count label."""
        self.none_video_label.config(text=str(self.none_video_count))

    def start_automation(self):
        """Start the automation process."""
        self.is_running = True
        self.cycle_count = 0
        self.none_video_count = 0
        self.update_cycle_count()
        self.update_none_video_count()

        self.start_button.config(state=tk.DISABLED, bg="#cccccc")
        self.stop_button.config(state=tk.NORMAL, bg=self.colors['danger'])
        self.update_status("Running", self.colors['success'])

        self.log("Automation started - waiting 5 seconds before beginning...", "INFO")

        # Start automation in a separate thread
        self.automation_thread = threading.Thread(target=self.run_automation, daemon=True)
        self.automation_thread.start()

    def stop_automation(self):
        """Stop the automation process."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL, bg=self.colors['success'])
        self.stop_button.config(state=tk.DISABLED, bg="#cccccc")
        self.update_status("Stopped", self.colors['danger'])
        self.log(f"Automation stopped by user after {self.cycle_count} cycles ({self.none_video_count} none videos)",
                 "INFO")

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

    def handle_none_video(self) -> bool:
        """Handle videos that don't have play/fullscreen buttons (none videos)."""
        self.log("Detected none video - skipping directly to next", "INFO")
        self.none_video_count += 1
        self.update_none_video_count()

        time.sleep(1)

        # Click next button
        self.log("Looking for next button...", "INFO")
        next_images = ["next1.png", "next2.png"]
        next_clicked = False

        for img in next_images:
            self.log(f"Trying to locate {img}...", "INFO")
            next_location = self.wait_for_image(img, confidence=0.7, timeout=5)
            if next_location:
                self.log(f"Found {img}, clicking", "INFO")
                self.click_center(next_location)
                next_clicked = True
                break

        if not next_clicked:
            self.log("No next button found", "WARNING")
            return False

        self.log("None video handled successfully", "SUCCESS")
        return True

    def process_video(self) -> bool:
        """Process one video cycle."""
        try:
            # Check for play button with shorter timeout
            self.log("Looking for play button...", "INFO")
            play_location = self.wait_for_image('play.png', confidence=0.8, timeout=5)

            if not play_location:
                # No play button found - this is a none video
                self.log("Play button not found - treating as none video", "INFO")
                return self.handle_none_video()

            # Play button found - this is a regular video, proceed with full flow
            self.log("Play button found - processing as regular video", "INFO")
            self.log("Clicking play button", "INFO")
            self.click_center(play_location)
            time.sleep(2)

            # Click fullscreen button
            self.log("Looking for fullscreen button...", "INFO")
            fullscreen_location = self.wait_for_image('fullscreen.png', confidence=0.8, timeout=30)

            if not fullscreen_location:
                # Play button was found but fullscreen is missing - this is an error
                self.log("Fullscreen button not found after clicking play", "ERROR")
                return False

            self.log("Clicking fullscreen button", "INFO")
            self.click_center(fullscreen_location)

            # Wait for video to end
            self.log("Waiting for video to end...", "INFO")
            out_location = self.wait_for_image('out.png', confidence=0.8, timeout=3600)
            if not out_location:
                self.log("Video end indicator not found within timeout", "ERROR")
                return False

            self.log("Video ended, pressing ESC", "INFO")
            pyautogui.press('esc')
            time.sleep(2)

            # Click next button
            self.log("Looking for next button...", "INFO")
            next_images = ["next1.png", "next2.png"]
            next_clicked = False

            for img in next_images:
                self.log(f"Trying to locate {img}...", "INFO")
                next_location = self.wait_for_image(img, confidence=0.7, timeout=5)
                if next_location:
                    self.log(f"Found {img}, clicking", "INFO")
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

            self.log("=" * 60, "INFO")
            self.log(f"Starting cycle #{self.cycle_count}", "INFO")
            self.log("=" * 60, "INFO")

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