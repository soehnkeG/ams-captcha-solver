import cv2
import numpy as np
import pytesseract

image = cv2.imread('map.png')

templates = {
    0: [cv2.imread('templates/0/degrees.png')],
    1: [cv2.imread('templates/1/degrees.png')],
    2: [cv2.imread('templates/2/degrees.png')],
    3: [cv2.imread('templates/3/degrees.png')],
    4: [cv2.imread('templates/4/degrees.png')],
    5: [cv2.imread('templates/5/degrees.png')],
    6: [cv2.imread('templates/6/degrees.png')],
    7: [cv2.imread('templates/7/degrees.png')],
    8: [cv2.imread('templates/8/degrees.png')],
    9: [cv2.imread('templates/9/degrees.png')],
}
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)

im2 = image.copy()

text = ""
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cropped = im2[y:y + h, x:x + w]

    # if w > h:
    #     for (digit, digit_templates) in templates.items():
    #         for template in digit_templates:
    #             w, h = template.shape[::-1]  # Get width and height from the template
    #             result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    #             threshold = 0.8
    #             locations = np.where(result >= threshold)
    #
    #             for pt in zip(*locations[::-1]):
    #                 cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    #                 print(f"Detected Number: {digit}")
    #                 text.join(digit)
    # else:
    detected = pytesseract.image_to_string(cropped, lang='eng')
    print(f"Detected Text: {detected}")
    text.join(detected)

cv2.imshow('Detected Numbers', image)
print("Found Text: ", text)
cv2.waitKey(0)
