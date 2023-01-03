import time
from datetime import datetime
from pynput import keyboard
from collections import OrderedDict


class Timer:
    def __init__(self):
        self.start_time = 0
        self.start_shift = 0
        self.segment = OrderedDict({ 0: True })
        self.marked = OrderedDict({ 0: False })

    def stamp(self):
        return int(time.time() * 10000000)

    def logger(self, timeline, text, type=1):
        reltime = datetime.fromtimestamp(timeline / 10000000).strftime("%M:%S.%f")
        abstime = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if not self.start_time:
            print( '[WARN] {} 还未开始'.format(abstime) )
        else:
            if type == 0:
                print( '[HINT] {} {}'.format(abstime, text) )
            elif type == 1:
                print( '[INFO] {} {}'.format(reltime, text) )

    def series(self, shift=0):
        if shift:
            ans = self.stamp() - self.start_time + int(shift * 10000000)
            if ans > 0:
                return ans
            else:
                return 0
        else:
            return self.stamp() - self.start_time

    def start(self):
        self.start_time = self.stamp()
        self.segment = OrderedDict({ 0: True })
        self.marked = OrderedDict({ 0: False })

    def mark(self):
        key = self.series()
        self.marked[key] = True

    def select(self):
        key = self.series()
        self.segment[key] = True
        self.logger(key, '√')

    def remove(self):
        key = self.series()
        self.segment[key] = False
        self.logger(key, '×')

    def backout(self, second):
        remove_start, remove_end = self.series(-1 * second), self.series()
        self.segment[remove_start] = False
        self.segment[remove_end] = True
        self.logger(remove_start, '×┓')
        self.logger(remove_end, '√┛')

    def refresh(self):
        # point = True
        self.segment = sorted(self.segment.items(), key=lambda x:x[0])
        # for timeline, flag in self.segment.items():
        #     if flag == point:
        #         start = timeline
        #         point = not point
        #     else:

    def generate(self, source='', output=''):
        clipline, markline = [], []
        clipline.append( '\t\t\t\t<clip src="{}" start="0" stop="{}" timeFormat="100ns_units" />'.format(source, self.series()) )
        for timeline, flag in self.segment.items():
            if flag:
                markline.append( '\t\t\t\t<marker time="{}" timeFormat="100ns_units" flags="select_interval"/>'.format(timeline) )
            else:
                markline.append( '\t\t\t\t<marker time="{}" timeFormat="100ns_units" />'.format(timeline) )
        template = """<timelines version="2" >
    <timeline>
        <group output="{}" >
            <track video="1" audio="1" text="0" accuracy="frame" flags="interlaced_fields_alignment,keep_mpeg_closedcaptions,keep_rtp_hint_tracks" >
{}
            </track>
        </group>
        <view>
            <markers>
{}
            </markers>
            <preview_streams video="0" audio="0" text="-1" />
        </view>
    </timeline>
</timelines>
""".format( output, clipline[0], '\n'.join(markline) )
        return template


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
        ts.logger(0, text="计时开始", type=0)
        # print(key)
    elif key == keyboard.KeyCode.from_char('+'):
        ts.select()
        # print(key, '+')
    else:
        if 96 < keycode < 106:
            second = keycode - 96
            ts.backout(second)
            # print('Num {}'.format(keycode))
        elif keycode == 96:
            ts.remove()
            # print('Zero')
        elif keycode == 110:
            ts.mark()
            # print('Dot')


if __name__ == '__main__':
    while True:
        print('按 F9/F12 开始计时 ')
        ts = Timer()

        with keyboard.Listener(
                on_release = on_release,
                win32_event_filter = __win32_event_filter__) as listener:
            listener.join()

        outfile = time.strftime("%y%m%d-%H%M",time.localtime())
        filename = input('输入视频路径 > ')
        if filename == '':
            print('跳过')
            continue
        else:
            dest = 'C:\\Users\\MowChan\\Desktop\\初中物理-{}.mp4'.format(input('初中物理 > '))
            fstring = ts.generate(filename.strip('"'), dest)
            with open('{}.ssp'.format(outfile), 'w', encoding='gbk') as f:
                f.write(fstring)
            print('已保存档案 {}.ssp'.format(outfile))
