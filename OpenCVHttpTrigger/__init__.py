import logging
import azure.functions as func

import cv2
import numpy as np

# https://stackoverflow.com/a/37032551
def loadImageFromRequestBody (
        req: func.HttpRequest) -> [np.uint8]:
    """Load image as uint8 array from the request body."""
    img_bin = req.get_body()
    img_buffer = np.asarray(bytearray(img_bin), dtype=np.uint8)
    return img_buffer

# https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de
# cv.Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient]]]) -> edges
# cv.Canny(dx, dy, threshold1, threshold2[, edges[, L2gradient]]) -> edges
def extractEdges (
        buf: [np.uint8],
        threshold1: int,
        threshold2: int) -> [np.uint8]:
    """Tranform the input image to show its edges using the Canny algorithm."""
    img = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
    img_edges = cv2.Canny(img, threshold1, threshold2)
    return img_edges
    
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # CONSTANTS
    THRESHOLD1 = 20
    THRESHOLD2 = 60
    
    img_buffer = loadImageFromRequestBody(req)
    img_edges = extractEdges(
        img_buffer, THRESHOLD1, THRESHOLD2)

    img_encoded = cv2.imencode('.jpg', img_edges)
    img_response = img_encoded[1].tobytes()

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    headers = {
        'Content-Type': 'image/jpeg',
        'Content-Disposition': 'attachment; filename="image.jpg"',
        'Access-Control-Allow_Origin': '*'
    }

    return func.HttpResponse(
        body=img_response,
        headers=headers,
        status_code=200)
