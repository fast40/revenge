import cv2

image = cv2.imread('chars.png')

cols = 2
rows = 94 // cols

x_step = image.shape[1] // cols
y_step = image.shape[0] // rows


chars = []
i = 33

for y in range(0, image.shape[0], y_step):
    for x in range(0, image.shape[1], x_step):
        roi = image[y:y+y_step, x:x+x_step].repeat(20, axis=0).repeat(20, axis=1)

        chars.append([i, roi])
        i += 1

# uncomment the rest of this commented code to manually step through character images:
#         cv2.imshow('roi', roi)

#         key = cv2.waitKey(0)

#         if key == ord('q'):
#             cv2.destroyAllWindows()
#             quit()

# cv2.destroyAllWindows()


chars = sorted(chars, key=lambda x: x[1].sum())

print('\n\n\n\n\n\n')

for char in chars:
    print(chr(char[0]), end='')

print('\n\n\n\n\n\n')