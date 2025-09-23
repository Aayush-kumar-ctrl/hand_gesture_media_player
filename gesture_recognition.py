# gesture_recognition.py
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# indices for tips in MediaPipe hand landmarks
TIP_IDS = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

class HandDetector:
    def __init__(self, maxHands=1, detection_conf=0.7, track_conf=0.7):
        self.hands = mp_hands.Hands(max_num_hands=maxHands,
                                     min_detection_confidence=detection_conf,
                                     min_tracking_confidence=track_conf)
        self.tip_ids = TIP_IDS

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        h, w, _ = img.shape
        all_hands = []
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    lm_list.append((int(lm.x * w), int(lm.y * h), lm.z))
                all_hands.append(lm_list)
                if draw:
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return all_hands

def fingers_up(lm_list):
    """
    Return list of 5 values 1/0 for each finger whether it's up.
    Thumb logic uses x-direction (handedness could change; this is a simple heuristic).
    """
    fingers = []
    # thumb
    if lm_list[TIP_IDS[0]][0] < lm_list[TIP_IDS[0] - 1][0]:
        fingers.append(1)
    else:
        fingers.append(0)
    # other four fingers: tip y < pip y => finger up
    for id in range(1, 5):
        if lm_list[TIP_IDS[id]][1] < lm_list[TIP_IDS[id] - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

class MovementBuffer:
    """Buffer last N index-tip x positions to detect swipes."""
    def __init__(self, maxlen=6):
        self.buf = deque(maxlen=maxlen)
        self.time_buf = deque(maxlen=maxlen)

    def add(self, x):
        self.buf.append(x)
        self.time_buf.append(time.time())

    def detect_swipe(self, thresh_px=120, max_duration=0.6):
        if len(self.buf) < 2:
            return None
        dx = self.buf[-1] - self.buf[0]
        dt = self.time_buf[-1] - self.time_buf[0]
        if dt > max_duration:
            return None
        if abs(dx) > thresh_px:
            return 'right' if dx > 0 else 'left'
        return None
