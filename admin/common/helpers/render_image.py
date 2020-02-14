def render_image(image):
    yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
