import time
from datetime import datetime
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
            print( '[WARN] {} 还未开始\a'.format(abstime) )
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
        _time = time.localtime()

    def mark(self):
        key = self.series()
        self.marked[key] = True
        self.logger(key, '！')

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
        self.logger(remove_end, '×┛')

    def refresh(self):
        self.segment = sorted(self.segment.items(), key=lambda x:x[0])

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
