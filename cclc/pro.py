import os
import subprocess
import configparser
from os import path
from timer import Timer
from pynput import keyboard
from time import strftime, localtime


config = configparser.ConfigParser(interpolation=None)
config.read('config.ini', encoding='utf8')
start_key = config['options']['start_key'].upper()
end_key = config['options']['end_key'].upper()

FKEY = {
    'F1': keyboard.Key.f1,  'F2': keyboard.Key.f2,   'F3': keyboard.Key.f3,   'F4': keyboard.Key.f4,
    'F5': keyboard.Key.f5,  'F6': keyboard.Key.f6,   'F7': keyboard.Key.f7,   'F8': keyboard.Key.f8,
    'F9': keyboard.Key.f9, 'F10': keyboard.Key.f10, 'F11': keyboard.Key.f11, 'F12': keyboard.Key.f12
}


def _win32_event_filter_(msg, data):
    global listener
    suppress_map = { 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 107, 110 }
    if data.vkCode in suppress_map and msg == 256:
        listener.suppress_event()

def _release_event_(key):
    global _time
    try:
        keycode = key.vk
    except AttributeError:
        keycode = key.value.vk
    if key == FKEY[end_key]:
        return False
    elif key == FKEY[start_key]:
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
    # https://stackoverflow.com/questions/3646362/how-to-control-the-size-of-the-windows-shell-window-from-within-a-python-script

    _options, _time = config['options'], localtime()
    _modes = config.sections()
    _modes.remove('options')

    print('>>> CCLC')
    f_capture = input('是否启动录制程序? y/n [y]: ')
    if f_capture in ('1', 'y', 'Y'):
        _path = config['options']['capture_path']
        _dir, _ = path.split(_path)
        subprocess.Popen( _path, cwd=_dir )
        print('>> 正在启动录制程序')

    while True:
        ts = Timer()
        f_mode = input('选择当前的模式？\n{} [0]: '.format(_text_modes(_modes)) )
        f_mode = int(f_mode) if f_mode.isdigit() else 0
        print('>> 按 {} 开始计时，按 {} 停止计时'.format(start_key, end_key))
        with keyboard.Listener(
                on_release = _release_event_,
                win32_event_filter = _win32_event_filter_) as listener:
            listener.join()
        name = input('输出视频文件名 (q 跳过): ')
        if name in ('q', 'Q'):
            print('>> 跳过')
            continue
        else:
            if f_mode < len(_modes):
                conf = config[ _modes[f_mode] ]
                _path_r = path.join( conf['record_dir'], strftime( conf['record_name'], _time ))
                _path_p = path.join( conf['project_dir'], strftime( conf['project_name'], _time ))
            _pro_name = strftime( conf['project_name'], _time )
            _path_rec = path.join( conf['record_dir'], strftime( conf['record_name'], _time ))
            _path_pro = path.join( conf['project_dir'], strftime( conf['project_name'], _time ))
            _path_out = path.join( conf['output_dir'], conf['output_name'].format(name) )
            fstring = ts.generate(_path_rec, _path_out)
            with open( _path_pro, 'w', encoding='gbk' ) as f:
                f.write(fstring)
            print('>> 已保存档案'.format(_pro_name))
            f_open = input('是否打开剪辑软件？ y/n [y]: ')
            if f_open in ('y', 'Y', ''):
                subprocess.Popen([ _options['cutter_path'], _path_pro ])
