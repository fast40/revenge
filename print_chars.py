# print all 94 visible ascii characters in rows of 2 to allow for a screenshot
for i in range(0, 94, 2):
    print(f'{chr(i + 33)}  {chr(i + 34)}')