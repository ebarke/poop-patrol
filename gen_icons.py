#!/usr/bin/env python3
import subprocess, sys

def make_icon_svg(size):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <rect width="{size}" height="{size}" rx="{size//5}" fill="#2d5a1b"/>
  <text x="{size//2}" y="{int(size*0.67)}" font-size="{int(size*0.55)}" text-anchor="middle" dominant-baseline="middle">💩</text>
</svg>"""

for sz in [192, 512]:
    svg = make_icon_svg(sz)
    svg_path = f"/home/claude/poop-patrol/icon-{sz}.svg"
    png_path = f"/home/claude/poop-patrol/icon-{sz}.png"
    with open(svg_path, 'w') as f:
        f.write(svg)
    try:
        result = subprocess.run(['convert', '-background', 'none', svg_path, png_path],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Generated icon-{sz}.png via ImageMagick")
        else:
            # Try rsvg-convert
            result2 = subprocess.run(['rsvg-convert', '-w', str(sz), '-h', str(sz), svg_path, '-o', png_path],
                                     capture_output=True, text=True)
            if result2.returncode == 0:
                print(f"Generated icon-{sz}.png via rsvg-convert")
            else:
                # Use cairosvg via pip
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'cairosvg', '--break-system-packages', '-q'])
                import cairosvg
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=sz, output_height=sz)
                print(f"Generated icon-{sz}.png via cairosvg")
    except Exception as ex:
        print(f"Icon generation fallback for {sz}: {ex}")
        # Fallback: write a simple colored PNG using pure Python
        import struct, zlib
        def png_solid(w, h, r, g, b):
            def chunk(name, data):
                c = zlib.crc32(name + data) & 0xffffffff
                return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)
            ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
            raw = b''
            for _ in range(h):
                raw += b'\x00' + bytes([r,g,b]*w)
            idat = zlib.compress(raw)
            return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')
        with open(png_path, 'wb') as f:
            f.write(png_solid(sz, sz, 45, 90, 27))
        print(f"Generated icon-{sz}.png (solid color fallback)")
