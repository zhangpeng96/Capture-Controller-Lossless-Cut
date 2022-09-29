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

    def output_xml(self, filename='', outfile='test'):
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
        with open('{}.ssp'.format(outfile), 'w', encoding='utf-8') as f:
            f.write(fstring)
        print('已保存档案 {}.ssp'.format(outfile))



def __win32_event_filter__(msg, data):
    global listener
    suppress_map = { 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 110 }
    if data.vkCode in suppress_map and msg == 256:
        listener.suppress_event()


def on_release(key):
    try:
        keycode = key.vk
    except AttributeError:
        keycode = key.value.vk

    if key == keyboard.Key.esc:
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


while True:
    print('welcome! ')
    ts = Timer()

    with keyboard.Listener(
            on_release = on_release,
            win32_event_filter = __win32_event_filter__) as listener:
        listener.join()

    ts.print()
    outfile = time.strftime("%y%m%d-%H%M",time.localtime())
    filename = input('输入视频路径 > ')
    if filename == '':
        print('跳过')
        continue
    else:
        filename = filename.strip('"')
    ts.output_xml(filename=filename, outfile=outfile)


