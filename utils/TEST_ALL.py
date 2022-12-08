from .TEST_ONE import test


def test_all(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY,
             oY, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP):
    green = test(img, img_resized, lHG, lSG, lVG, hHG, hSG, hVG, eG, dG, cG, oG)
    yellow = test(img, img_resized, lHY, lSY, lVY, hHY, hSY, hVY, eY, dY, cY, oY)
    red = test(img, img_resized, lHR, lSR, lVR, hHR, hSR, hVR, eR, dR, cR, oR)
    purple = test(img, img_resized, lHP, lSP, lVP, hHP, hSP, hVP, eP, dP, cP, oP)

    return green, yellow, red, purple
