import struct, zlib

BG = (0x0f, 0x12, 0x10)
ACCENT = (0x9b, 0xc5, 0x3d)


def png(path, size):
    px = [[BG for _ in range(size)] for _ in range(size)]

    # Drei Balken wie die Fortschrittsbalken der App, zentriert im inneren 80%
    bar_w = int(size * 0.13)
    gap = int(size * 0.07)
    heights = [0.30, 0.46, 0.62]
    total_w = 3 * bar_w + 2 * gap
    x0 = (size - total_w) // 2
    base = int(size * 0.72)

    for i, h in enumerate(heights):
        bx = x0 + i * (bar_w + gap)
        top = base - int(size * h)
        for y in range(top, base):
            for x in range(bx, bx + bar_w):
                if 0 <= x < size and 0 <= y < size:
                    px[y][x] = ACCENT

    raw = b"".join(b"\x00" + b"".join(struct.pack("3B", *px[y][x]) for x in range(size)) for y in range(size))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(raw, 9))
    out += chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(out)
    print(path, size, "ok")


png(r"C:\Users\yurrg\fitness\icon-192.png", 192)
png(r"C:\Users\yurrg\fitness\icon-512.png", 512)
