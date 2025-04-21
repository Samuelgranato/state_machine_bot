from humancursor import SystemCursor

cursor = SystemCursor()


# def mover_mouse_humanizado(dest_x, dest_y, total_time=0.15):
#     atual_x, atual_y = pyautogui.position()
#     dx = dest_x - atual_x
#     dy = dest_y - atual_y
#     dist = (dx**2 + dy**2) ** 0.5

#     if dist < 1:
#         return

#     steps = min(25, max(8, int(dist / 5)))  # número de steps baseado na distância
#     interval = total_time / steps

#     for i in range(1, steps + 1):
#         t = i / steps
#         x = int(atual_x + dx * t + random.uniform(-1, 1))
#         y = int(atual_y + dy * t + random.uniform(-1, 1))
#         pyautogui.moveTo(x, y, duration=0)
#         time.sleep(interval)

#     pyautogui.moveTo(dest_x, dest_y, duration=0)


# def clicar():
#     pyautogui.click()


def mover_mouse_humanizado(x, y):
    cursor.move_to([x, y], duration=0.1)


def clicar(x, y):
    cursor.click_on([x, y])
