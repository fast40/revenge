import cv2

CHARS = '`.\',_-:~;"!^+/\><)(|=Lv?[]Ttr7}{izlcxfIYjnuJsF14*yoVaehk2PZ96CAEXU3qpwHmbKd5SO#D@RGNg&8B0W%QM$'
IMAGE_SIZE = (80, 24)

cap = cv2.VideoCapture('revenge.mov')

with open('frames.py', 'w') as file:
    file.write('frames = [\n')

    while True:
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, IMAGE_SIZE)

        for row in frame:
            string = ''

            for pixel in row:
                string += CHARS[int(pixel / 255 * (len(CHARS) - 1))]
            
            string = string.replace('\'', '\' + r\"\'\" + r\'')

            file.write('r\'' + string + '\',\n')

    file.write(']\n')