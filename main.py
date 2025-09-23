# main.py
import cv2
import time
from gesture_recognition import HandDetector, fingers_up, MovementBuffer
import actions

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    mov_buf = MovementBuffer(maxlen=8)

    play_state = False  # we just toggle play/pause
    swipe_cooldown = 1.0
    last_swipe = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Couldn't read from webcam.")
            break

        hands = detector.find_hands(frame, draw=True)
        if hands:
            lm_list = hands[0]  # single hand
            # index tip x for swipe detection
            index_tip_x = lm_list[8][0]
            mov_buf.add(index_tip_x)

            # detect swipe
            swipe = mov_buf.detect_swipe(thresh_px=120, max_duration=0.6)
            if swipe and (time.time() - last_swipe) > swipe_cooldown:
                if swipe == 'right':
                    print("Gesture -> Swipe Right -> Next track")
                    actions.next_track()
                else:
                    print("Gesture -> Swipe Left -> Previous track")
                    actions.previous_track()
                last_swipe = time.time()

            f_up = fingers_up(lm_list)  # list of 5 ints
            # Determine gestures
            # Open palm: all four fingers (except thumb) up -> play/pause
            if f_up[1] == 1 and f_up[2] == 1 and f_up[3] == 1 and f_up[4] == 1:
                # Treat as open palm
                print("Gesture -> Open Palm -> Play/Pause")
                actions.play_pause()
                time.sleep(0.7)  # simple debounce

            # Thumbs up: thumb up, other fingers down
            if f_up[0] == 1 and f_up[1] == 0 and f_up[2] == 0 and f_up[3] == 0 and f_up[4] == 0:
                print("Gesture -> Thumbs Up -> Volume Up")
                actions.change_volume(0.06)
                time.sleep(0.5)

            # Thumbs down: detect thumb down (we'll check relative vertical position)
            thumb_tip_y = lm_list[4][1]
            thumb_ip_y = lm_list[3][1]
            # approximate thumbs down: thumb tip lower (greater y) than thumb ip and other fingers down
            if (thumb_tip_y > thumb_ip_y) and (f_up[1] == 0 and f_up[2] == 0 and f_up[3] == 0 and f_up[4] == 0):
                print("Gesture -> Thumbs Down -> Volume Down")
                actions.change_volume(-0.06)
                time.sleep(0.5)

        cv2.imshow("Hand Gesture Media Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
