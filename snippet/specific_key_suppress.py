import threading
import time

from pynput import keyboard


def __win32_event_filter__(msg, data):
    global listener
    print('filter', msg, data)
    # print(listener)
    suppress_map = { 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 110 }
    if data.vkCode in suppress_map and msg == 256:
        listener.suppress_event()

def on_release(key):
    try:
        keycode = key.vk
    except AttributeError:
        keycode = key.value.vk

    print(keycode)

    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(
        on_release = on_release,
        win32_event_filter = __win32_event_filter__) as listener:
    listener.join()






# def __win32_event_filter__(self, msg, data):
#     if not self.on_playing_lol:
#         return
#     # win key ,disable win
#     if data.vkCode == 0x5B:
#         # Suppress x
#         self.listener.suppress_event()
#     # msg 256 按下，msg 257 抬起
#     # 1秒内连按两下left crtl 屏蔽第二下,257指按下
#     if data.vkCode == 0xa2:
#         if msg == 256 and self.pre_event == 257:
#             diff = (datetime.now() - self.last_time).microseconds
#             if diff < self.wait_time:
#                 self.pre_event = msg
#                 self.listener.suppress_event()
#         if msg == 257:
#             self.last_time = datetime.now()
#             self.pre_event = msg
