import os
import subprocess
import configparser
from os import path
from timer import Timer
from pynput import keyboard
from time import strftime, localtime


config = configparser.ConfigParser(interpolation=None)
config.read('config.ini', encoding='utf8')


def _win32_event_filter_(msg, data):
    global listener
    suppress_map = { 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 110 }
    if data.vkCode in suppress_map and msg == 256:
        listener.suppress_event()

def _release_event_(key):
    try:
        keycode = key.vk
    except AttributeError:
        keycode = key.value.vk
    if key == keyboard.Key.f12:
        return False
    elif key == keyboard.Key.f9:
        ts.start()
        _time = localtime()
        ts.logger(0, text="计时开始", type=0)
    elif key == keyboard.KeyCode.from_char('+'):
        ts.select()
    else:
        if 96 < keycode < 106:
            second = keycode - 96
            ts.backout(second)
        elif keycode == 96:
            ts.remove()
        elif keycode == 110:
            ts.mark()

def _text_modes(modes):
    string = []
    for i, mode in enumerate(modes):
        string.append( '{}-{}'.format(i, config[mode]['mode_name'] ))
    return '；'.join(string)


if __name__ == '__main__':
    os.system('mode con: cols=80 lines=15')

    _options, _time = config['options'], localtime()
    _modes = config.sections()
    _modes.remove('options')

    print('>>> CCLC')
    f_capture = input('是否启动录制程序? [y]: ')
    if f_capture in ('1', 'y', 'Y'):
        _path = config['options']['capture_path']
        _dir, _ = path.split(_path)
        subprocess.Popen( _path, cwd=_dir )
        print('>> 正在启动录制程序')

    while True:
        ts = Timer()
        f_mode = input('选择当前的模式？\n{} [0]: '.format(_text_modes(_modes)) )
        f_mode = int(f_mode) if f_mode.isdigit() else 0
        if f_mode < len(_modes):
            conf = config[ _modes[f_mode] ]
            _path_r = path.join( conf['record_dir'], strftime( conf['record_name'], _time ))
            _path_p = path.join( conf['project_dir'], strftime( conf['project_name'], _time ))

        print('>> 按 {} 开始计时'.format(_options['start_key']))
        with keyboard.Listener(
                on_release = _release_event_,
                win32_event_filter = _win32_event_filter_) as listener:
            listener.join()
        name = input('输出视频文件名 (q 跳过): ')
        if name == 'q':
            print('>> 跳过')
            continue
        else:
            _pro_name = strftime( conf['project_name'], _time )
            _path_rec = path.join( conf['record_dir'], strftime( conf['record_name'], _time ))
            _path_pro = path.join( conf['project_dir'], strftime( conf['project_name'], _time ))
            _path_out = path.join( conf['output_dir'], conf['output_name'].format(name) )
            fstring = ts.generate(_path_rec, _path_out)
            with open( _path_pro, 'w', encoding='gbk' ) as f:
                f.write(fstring)
            print('>> 已保存档案'.format(_pro_name))
            f_open = input('是否打开剪辑软件？ y/n [n]: ')
            if f_open in ('y', 'Y', ''):
                subprocess.Popen([ _options['cutter_path'], _path_pro ])
