import cv2

from config import MOTION_MIN_AREA


def detectar_movimentos(frame_anterior, frame_atual, debug=False):
    frame_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (3, 3), 0)

    regioes = []

    if frame_anterior is not None:
        delta = cv2.absdiff(frame_anterior, frame_gray)
        delta = cv2.multiply(delta, 2)
        thresh = cv2.threshold(delta, 15, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            if cv2.contourArea(contorno) < MOTION_MIN_AREA:
                continue
            (x, y, w, h) = cv2.boundingRect(contorno)
            regioes.append((x, y, w, h))

        if debug:
            cv2.imshow("Delta", delta)
            cv2.imshow("Threshold", thresh)

    return frame_gray, regioes
