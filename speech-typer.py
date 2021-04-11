#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr

from pynput.keyboard import Key, Controller

keyboard = Controller()

keys = {
    'enter': Key.enter,
    'space': Key.space,
    'backspace': Key.backspace,
    'delete': Key.delete,
    'left': Key.left,
    'right': Key.right,
    'up': Key.up,
    'down': Key.down,
    'tab': Key.tab,
}

numbers = {
    'one': 1,
    'two': 2,
    'three': 3,
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
        return 1

def press_key(k, n = 1):
    for c in range(n):
        keyboard.press(k)
        keyboard.release(k)

def on_recognize(r):

    words = r.split(' ')

    if words[0].lower() in keys:
        n = 1
        if (len(words) > 1):
            n = get_number(words[1].lower())
        press_key(keys[words[0].lower()], n)
    else:
        keyboard.type(r + ' ')


# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print('>>>')
        result = recognizer.recognize_google(audio)
        print("Result: " + result)
        on_recognize(result)
    except sr.UnknownValueError:
        print("...")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

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
    print("Devices:")
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