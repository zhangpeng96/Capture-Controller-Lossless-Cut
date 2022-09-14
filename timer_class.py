import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.start_shift = 0
        self.map = {}

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

    def output_xml_view(self):
        # self.map = {55122330: {'mark': True, 'select': False}, 101845370: {'mark': False, 'select': False}, 135145370: {'mark': False, 'select': True}, 185193016: {'mark': False, 'select': True}, 225269716: {'mark': False, 'select': False}}
        self.map = {0: {'mark': False, 'select': True}, 1156148218: {'mark': False, 'select': False}, 1206148218: {'mark': False, 'select': True}, 1637590810: {'mark': False, 'select': False}, 1867422496: {'mark': False, 'select': True}, 2151581016: {'mark': False, 'select': False}, 2161581016: {'mark': False, 'select': True}, 2220064314: {'mark': False, 'select': False}, 2240064314: {'mark': False, 'select': True}, 2360138308: {'mark': False, 'select': False}, 2440138308: {'mark': False, 'select': True}, 2435574738: {'mark': False, 'select': False}, 2525574738: {'mark': False, 'select': True}, 2498542458: {'mark': False, 'select': False}, 2588542458: {'mark': False, 'select': True}, 2648533602: {'mark': False, 'select': True}, 2712935276: {'mark': False, 'select': False}, 2776300862: {'mark': False, 'select': False}, 2806300862: {'mark': False, 'select': True}}
        lines = ['<view>', '\t<markers>']
        for timeline, flag in sorted(self.map.items(), key=lambda x:x[0]):
            if flag['select']:
                lines.append( '\t\t<marker time="{}" timeFormat="100ns_units" flags="select_interval"/>'.format(timeline) )
            else:
                lines.append( '\t\t<marker time="{}" timeFormat="100ns_units" />'.format(timeline) )
        lines += ['\t</markers>', '\t<preview_streams video="0" audio="0" text="-1" />', '</view>']
        print('\n'.join(lines))



        
t = Timer()
# t.start()
# time.sleep(5.5)
# t.mark()
# time.sleep(3)
# t.backout(3.33)
# time.sleep(5)
# t.select()
# time.sleep(4)
# t.remove()
# t.print()
t.output_xml_view()


