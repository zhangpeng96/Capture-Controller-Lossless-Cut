import time
from pynput import keyboard


class Timer:
    def __init__(self):
        self.start_time = 0
        self.start_shift = 0
        self.map = { 0: { 'mark': False, 'select': True } }

    def stamp(self):
        return int(time.time() * 10000000)

    def series(self, shift=0):
        if shift:
            ans = self.stamp() - self.start_time + int(shift*10000000)
            if ans > 0:
                return ans
            else:
                return 0
        else:
            return self.stamp() - self.start_time

    def start(self):
        self.start_time = self.stamp()

    def mark(self, select=False):
        key = self.series()
        self.map[key] = { 'mark': True, 'select': select }

    def select(self):
        key = self.series()
        self.map[key] = { 'mark': False, 'select': True }

    def remove(self):
        key = self.series()
        self.map[key] = { 'mark': False, 'select': False }

    def backout(self, second):
        back_key = self.series(-1 * second)
        self.map[back_key] = { 'mark': False, 'select': False }
        key = self.series()
        self.map[key] = { 'mark': False, 'select': True }

    def print(self):
        print(self.map)

    def output_xml(self, filename=''):
        lines = ['<timelines version="2" >','\t<timeline>','\t\t<group>',
'\t\t\t<track video="1" audio="1" text="0" accuracy="frame" flags="interlaced_fields_alignment,keep_mpeg_closedcaptions,keep_rtp_hint_tracks" >']
        lines.append( '\t\t\t\t<clip src="{}" start="0" stop="{}" timeFormat="100ns_units" />'.format(filename, self.series()) )
        lines += ['\t\t\t</track>','\t\t</group>', '\t\t<view>', '\t\t\t<markers>']
        for timeline, flag in sorted(self.map.items(), key=lambda x:x[0]):
            if flag['select']:
                lines.append( '\t\t\t\t<marker time="{}" timeFormat="100ns_units" flags="select_interval"/>'.format(timeline) )
            else:
                lines.append( '\t\t\t\t<marker time="{}" timeFormat="100ns_units" />'.format(timeline) )
        lines += ['\t\t\t</markers>', '\t\t\t<preview_streams video="0" audio="0" text="-1" />', '\t\t</view>','\t</timeline>','</timelines>']
        fstring = '\n'.join(lines)
        with open('test.ssp', 'w', encoding='utf-8') as f:
            f.write(fstring)


ts = Timer()

def on_release(key):
    try:
        keycode = key.vk
    except AttributeError:
        keycode = key.value.vk

    # print(key, type(key), keycode, type(keycode))
    if key == keyboard.Key.esc:
        ts.print()
        filename = input('输入视频路径 >')
        ts.output_xml(filename=filename)
        return False
    elif key == keyboard.Key.f12 or key == keyboard.Key.f9:
        ts.start()
        print(key)
    elif key == keyboard.KeyCode.from_char('+'):
        ts.select()
        print(key, '+')
    else:
        if 96 < keycode < 106:
            second = keycode - 96
            ts.backout(second)
            print('Num {}'.format(keycode))
        elif keycode == 96:
            ts.remove()
            print('Zero')
        elif keycode == 110:
            ts.mark()
            print('Dot')

    # elif key == keyboard.KeyCode.from_vk(96):
    # # elif key == keyboard.KeyCode.from_char('+'):
    #     print('get f2')


# Collect events until released
with keyboard.Listener(
        suppress=True,
        # on_press=on_press,
        on_release=on_release) as listener:
    listener.join()