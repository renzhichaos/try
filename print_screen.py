import time
try:
    import Image
except ImportError:
    from PIL import ImageGrab


i = 1
while i <= 10:
    im = ImageGrab.grab()
    im.save("static\\"+str(i)+".jpg")
    print("screen...")
    time.sleep(10)
    i = i + 1