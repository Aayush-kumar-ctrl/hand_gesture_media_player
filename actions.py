# actions.py
import pyautogui
import platform
import time

# Check OS
_is_windows = platform.system() == "Windows"

# Try to import Windows volume control
if _is_windows:
    try:
        from ctypes import POINTER, cast
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        _has_pycaw = True
    except Exception:
        _has_pycaw = False
else:
    _has_pycaw = False

# Cooldown to avoid multiple triggers
last_action_time = {}
COOLDOWN = 2.0  # seconds

def cool(name):
    now = time.time()
    if name in last_action_time and now - last_action_time[name] < COOLDOWN:
        return False
    last_action_time[name] = now
    return True

# --- Media Actions ---

def play_pause():
    if not cool('play_pause'):
        return
    try:
        import keyboard
        keyboard.send('play/pause media')
    except Exception:
        pyautogui.press('space')

def next_track():
    if not cool('next'):
        return
    try:
        import keyboard
        keyboard.send('next track')
    except Exception:
        pyautogui.hotkey('ctrl', 'right')

def previous_track():
    if not cool('prev'):
        return
    try:
        import keyboard
        keyboard.send('previous track')
    except Exception:
        pyautogui.hotkey('ctrl', 'left')

# --- Volume Control ---
def change_volume(delta=0.05):
    """
    delta > 0 -> increase volume
    delta < 0 -> decrease volume
    """
    if not cool('volume'):
        return

    if _has_pycaw:
        try:
            sessions = AudioUtilities.GetSpeakers()
            interface = sessions.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            current = volume.GetMasterVolumeLevelScalar()
            new = min(max(0.0, current + delta), 1.0)
            volume.SetMasterVolumeLevelScalar(new, None)
            print(f"System Volume Changed: {new*100:.0f}%")
            return
        except Exception as e:
            print("Pycaw failed:", e)

    # Fallback for media player (VLC, Spotify, YouTube)
    steps = int(abs(delta) * 20) + 1
    key = 'volume up' if delta > 0 else 'volume down'
    try:
        import keyboard
        for _ in range(steps):
            keyboard.send(key)
    except Exception:
        try:
            for _ in range(steps):
                pyautogui.press(key)
        except Exception:
            print("Volume control failed. Focus on media player window or run as admin.")

