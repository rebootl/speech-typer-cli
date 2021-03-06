#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr

from pynput.keyboard import Key, Controller

keyboard = Controller()

mode = 'TEXT'

special_emojis = {
    'sleeping_relax': ':sleeping: :relaxed:',
    'pog': ':minchePog:',
    'park': ':minchePog:',
    'pug': ':minchePog:',
    'thinking_face': ':mincheThink:',
}

keys = {
    'enter': Key.enter,
    'center': Key.enter,
    'hunter': Key.enter,
    'wetter': Key.enter,
    'space': Key.space,
    'keyspace': Key.space,
    'backspace': Key.backspace,
    'delete': Key.delete,
    'arrow left': Key.left,
    'arrow right': Key.right,
    'arrow write': Key.right,
    'arrow up': Key.up,
    'arrow down': Key.down,
    'tab': Key.tab,
    'tabulator': Key.tab,
    'page up': Key.page_up,
    'page down': Key.page_down,
}

key_combos = {
    'alt-tab': (Key.alt, Key.tab),
    'desktop 1': (Key.cmd, '1'),
    'desktop one': (Key.cmd, '1'),
    'desktop phone': (Key.alt_l, '1'),
    'desktop two': (Key.alt_l, '2'),
    'desktop to' : (Key.alt_l, '2'),
    'desktop 3' : (Key.alt_l, '3'),
    'desktop for' : (Key.alt_l, '4'),
    'desktop 5' : (Key.alt_l, '5'),
    'desktop 6' : (Key.alt_l, '6'),
    'desktop sex' : (Key.alt_l, '6'),
    'tabulator back' : (Key.shift, Key.tab),
    'control c' : (Key.ctrl, 'c'),
    'control x' : (Key.ctrl, 'x'),
    'control v' : (Key.ctrl, 'v'),
    'ctrl-v' : (Key.ctrl, 'v'),
    'control s' : (Key.ctrl, 's'),
    'control z' : (Key.ctrl, 'z'),
    'control r' : (Key.ctrl, 'r'),
    'control are' : (Key.ctrl, 'r'),
}

modifier_keys = {
    'alternate': Key.alt,
    'control': Key.ctrl,
    'shift': Key.shift
}

special_keys = {
    'equal': '=',
    'equals': '=',
    'equal spaced': ' = ',
    'dash': '-',
    'backtick': '`',
    'dollar sign': '$',
}

numbers = {
    'one': 1,
    'two': 2,
    'to': 2,
    'three': 3,
    'tree': 3,
    'free': 3,
    'for': 4,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'twenty': 20,
    'twentyfive': 25,
}

def get_number(n):
    try:
        i = int(n)
        return i
    except ValueError:
        if (n in numbers):
            return numbers[n]
        return False

def press_key(k, n = 1):
    for c in range(n):
        keyboard.press(k)
        keyboard.release(k)

def press_key_combo(ks):
    with keyboard.pressed(ks[0]):
        keyboard.press(ks[1])
        keyboard.release(ks[1])

def get_words_without_number(words):
    n = get_number(words[-1:][0])
    if n:
        r = ' '.join(words[:-1])
    else:
        r = ' '.join(words)
    return r, n

def on_recognize(r):

    global mode

    words = r.lower().split(' ')
    words_without_number, repeats = get_words_without_number(words)
    # print(words_without_number, repeats)

    if words[0] == 'mode':
        if words[1] == 'text':
            mode = 'TEXT'
        elif words[1] == 'programming':
            mode = 'PROG'
    elif words[0] == 'emoji':
        p = '_'.join(words[1:])
        if p in special_emojis:
            keyboard.type(special_emojis[p])
        else:
            e = ':' + p + ':'
            keyboard.type(e)
        press_key(Key.enter)
    elif words_without_number in keys:
        if repeats:
            press_key(keys[words_without_number], repeats)
        else:
            press_key(keys[words_without_number])
    elif r.lower() in key_combos:
        press_key_combo(key_combos[r.lower()])
    elif r.lower() in special_keys:
        keyboard.type(special_keys[words[0]])
    elif words[0] == 'letter':
        keyboard.type(words[1])
    elif words[0] == 'number':
        keyboard.type(str(get_number(words[1])))
    else:
        if mode == 'TEXT':
            keyboard.type(r.lower() + ' ')
        elif mode == 'PROG':
            keyboard.type(r.lower())

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print('~~~')
        result = recognizer.recognize_google(audio)
        print('Result: ' + result)
        on_recognize(result)
        print(mode + ' >>>')
    except sr.UnknownValueError:
        print('...')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))

def start_typer(device):
    r = sr.Recognizer()
    m = None
    if device:
        m = sr.Microphone()
    else:
        m = sr.Microphone(device)
    with m as source:
        #r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
        r.energy_threshold = 300  # we only need to calibrate once, before we start listening
        r.dynamic_energy_threshold = False

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    print('listening')
    # `stop_listening` is now a function that, when called, stops background listening

    # do some unrelated computations for 5 seconds
    #for _ in range(50): time.sleep(1)  # we're still listening even though the main thread is doing other things

    # calling this function requests that the background listener stop listening
    #stop_listening(wait_for_stop=False)

    # do some more unrelated things
    while True: time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping

def list_devices():
    import pyaudio
    p = pyaudio.PyAudio()
    print('Devices:')
    for i in range(p.get_device_count()):
        d = p.get_device_info_by_index(i)
        print(f"{d['index']}: {d['name']}")

def main(ARGS):
    if ARGS.list_devices:
        list_devices()
    else:
        start_typer(ARGS.device)

if __name__ == '__main__':
    DEFAULT_SAMPLE_RATE = 16000

    import argparse
    parser = argparse.ArgumentParser(description="Stream from microphone to DeepSpeech using VAD")

    parser.add_argument('-l', '--list_devices', action='store_true',
                        help="List input device indexes.")
    parser.add_argument('-d', '--device', type=int, default=None,
                        help="Device input index (Int) as listed by -l.")

    ARGS = parser.parse_args()
    main(ARGS)
