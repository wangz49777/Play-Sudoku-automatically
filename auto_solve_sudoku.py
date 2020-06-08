import cv2
import numpy as np
import pyautogui
import sudoku99

left = 731
top = 120
width = 82


def read_img(image):
    sudoku = np.zeros([9, 9], dtype=np.int)
    img_gray = np.array(image.convert('L'))
    for i in range(1, 10):
        template = cv2.imread('img/{}.png'.format(i), 0)
        h, w = template.shape[:2]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        out_pts = [(-30, -30)]
        for pt in zip(*loc[::-1]):
            add_flag = True
            for out_pt in out_pts:
                if abs(pt[0] - out_pt[0]) + abs(pt[1] - out_pt[1]) < 30:
                    add_flag = False
                    break
            if add_flag:
                out_pts.append(pt)
        del out_pts[0]
        for pt in out_pts:
            sudoku[(pt[1] - top) // width][(pt[0] - left) // width] = i
            cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    return sudoku


def complete_sudoku(original_sudoku, sudoku):
    for i in range(9):
        for j in range(9):
            if original_sudoku[i][j] == 0:
                pyautogui.moveTo(left + width * (j + 1), top + width * (i + 1))
                pyautogui.click()
                pyautogui.press(str(sudoku[i][j]))


if __name__ == '__main__':
    taskbar = pyautogui.screenshot(region=(0, 1030, 1920, 50))
    taskbar_gray = np.array(taskbar.convert('L'))
    sudoku_ico = cv2.imread('img/sudoku.png', 0)
    loc = cv2.matchTemplate(taskbar_gray, sudoku_ico, cv2.TM_CCOEFF_NORMED)
    pt = np.unravel_index(loc.argmax(), loc.shape)
    pyautogui.moveTo(pt[1] + 25, 1050)
    pyautogui.click()
    pyautogui.sleep(0.5)
    pos = pyautogui.locateCenterOnScreen('img/resume.png', grayscale=False)
    if pos != None:
        pyautogui.moveTo(pos)
        pyautogui.click()
    pyautogui.sleep(0.5)
    screen = pyautogui.screenshot()
    print('开始读取')
    original_sudoku = read_img(screen)
    sum = sum(sum(original_sudoku))
    if sum == 0:
        print("读取sudoku失败")
        exit()
    sudoku = original_sudoku.tolist()
    sudoku = [i for row in sudoku for i in row]
    pointList = sudoku99.initPoint(sudoku)
    sudoku99.showSudoku(sudoku)
    print('开始计算')
    p = pointList.pop()
    sudoku99.tryInsert(p, sudoku, pointList)
    print('计算完毕：')
    sudoku99.showSudoku(sudoku)
    print('自动填充')
    sudoku = np.asarray(sudoku)
    sudoku.resize([9, 9])
    print(original_sudoku)
    print(sudoku)
    complete_sudoku(original_sudoku, sudoku)
    print('自动填充完毕')
