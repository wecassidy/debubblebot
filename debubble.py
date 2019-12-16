import argparse

import cv2
import numpy as np

def debubble(image, masking=True):
    """
    Detect speech bubbles and produce a blob of white to cover the
    text.

    @param image: the page to debubble, as loaded by cv2.imread

    @param masking: if true, produce a transparent/white mask to
        overlay on the image; if false, draw directly onto the image.
    """
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bubbles = cv2.threshold(grey, 250, 255, cv2.THRESH_BINARY)

    _, contours, _ = cv2.findContours(
        bubbles,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if masking:
        mask = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        drawSurface = np.zeros_like(mask)
    else:
        drawSurface = image.copy()

    for i, c in enumerate(contours):
        # Discard rectangles and triangles
        if len(c) < 5:
            continue
        # Discard small blobs
        if cv2.contourArea(c) < 7.5e3:
            continue

        _, (major, minor), _ = cv2.fitEllipse(c)
        area = 3.14159 * major/2 * minor/2
        if area < 1e6:
            cv2.drawContours(drawSurface, contours, i, (255, 255, 255, 255), -1)

    return drawSurface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce a mask for Aurora webcomic speech bubbles")
    parser.add_argument("book", type=int)
    parser.add_argument("chapter", type=int)
    parser.add_argument("page", type=int)
    parser.add_argument("out")
    parser.add_argument("--overlay", action="store_true")
    args = parser.parse_args()

    page = cv2.imread(f"scrape/{args.book}/{args.chapter}/{args.page:0>3}.png")
    debubbled = debubble(page, not args.overlay)
    cv2.imwrite(args.out, debubbled)
