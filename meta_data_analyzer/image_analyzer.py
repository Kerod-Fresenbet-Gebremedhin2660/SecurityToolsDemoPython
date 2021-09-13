with open("/home/kpc/Pictures/1.png", "rb") as image:
    f = image.read()
    # b = bytearray(f, encoding="utf-8")
    print(bytes(f))

