"""
YUVplayer 测试数据生成器
生成各种格式的测试图像，用于验证 RGB/BGR/YUV 显示是否正确
"""
import struct
import os

WIDTH = 352
HEIGHT = 288

def create_test_pattern_rgb(w, h):
    """Create a recognizable RGB test pattern (color bars + gradient)"""
    pixels = []
    for y in range(h):
        for x in range(w):
            # Color bars at top, gradient below
            if y < h // 3:
                # Color bars (8 vertical bars)
                bar_idx = (x * 8) // w
                colors = [
                    (255, 255, 255),  # White
                    (255, 255, 0),    # Yellow
                    (0, 255, 255),    # Cyan
                    (0, 255, 0),      # Green
                    (255, 0, 255),    # Magenta
                    (255, 0, 0),      # Red
                    (0, 0, 255),      # Blue
                    (0, 0, 0),        # Black
                ]
                r, g, b = colors[bar_idx]
            elif y < h * 2 // 3:
                # RGB gradient
                r = int(255 * x / w)
                g = int(255 * y / h)
                b = int(255 * (1 - x / w))
            else:
                # Checkerboard
                cell_size = 32
                cx = x // cell_size
                cy = y // cell_size
                if (cx + cy) % 2 == 0:
                    r, g, b = 200, 200, 200
                else:
                    r, g, b = 50, 50, 50
            pixels.append((r, g, b))
    return pixels

def save_rgb24(filename, pixels):
    """Save as RGB888 (R at byte 0, G at 1, B at 2)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            f.write(struct.pack('BBB', r, g, b))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_bgr24(filename, pixels):
    """Save as BGR888 (B at byte 0, G at 1, R at 2)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            f.write(struct.pack('BBB', b, g, r))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_rgb32(filename, pixels):
    """Save as RGBA8888 (R at byte 0, G at 1, B at 2, A at 3)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            f.write(struct.pack('BBBB', r, g, b, 255))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_bgr32(filename, pixels):
    """Save as BGRA8888 (B at byte 0, G at 1, R at 2, A at 3)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            f.write(struct.pack('BBBB', b, g, r, 255))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_rgb565(filename, pixels):
    """Save as RGB565 (R high 5 bits, G middle 6, B low 5)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            val = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
            f.write(struct.pack('<H', val))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_bgr565(filename, pixels):
    """Save as BGR565 (B high 5 bits, G middle 6, R low 5)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            val = ((b >> 3) << 11) | ((g >> 2) << 5) | (r >> 3)
            f.write(struct.pack('<H', val))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_rgb48(filename, pixels):
    """Save as RGB48 (16-bit per channel RGB, LE)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            # Scale 8-bit to 16-bit
            r16 = r * 257  # 255 -> 65535
            g16 = g * 257
            b16 = b * 257
            f.write(struct.pack('<HHH', r16, g16, b16))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_rgba64(filename, pixels):
    """Save as RGBA64 (16-bit per channel RGBA, LE)"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            r16 = r * 257
            g16 = g * 257
            b16 = b * 257
            f.write(struct.pack('<HHHH', r16, g16, b16, 65535))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_yuv444_planar(filename, pixels):
    """Save as planar YUV444 (8-bit)"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h)
    u_plane = bytearray(w * h)
    v_plane = bytearray(w * h)
    for idx, (r, g, b) in enumerate(pixels):
        # BT.601 limited range
        y_plane[idx] = max(0, min(255, ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16))
        u_plane[idx] = max(0, min(255, ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128))
        v_plane[idx] = max(0, min(255, ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128))
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_yuv420_planar(filename, pixels):
    """Save as planar YUV420 (8-bit), nearest-neighbor subsampling"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h)
    u_plane = bytearray(((w + 1) // 2) * ((h + 1) // 2))
    v_plane = bytearray(((w + 1) // 2) * ((h + 1) // 2))
    
    # Track which UV positions have been set
    uv_done = set()
    
    for idx, (r, g, b) in enumerate(pixels):
        x = idx % w
        y = idx // w
        y_plane[idx] = max(0, min(255, ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16))
        # Subsample U and V (nearest neighbor - use top-left of each 2x2 block)
        if (x % 2 == 0) and (y % 2 == 0):
            u_idx = (y // 2) * ((w + 1) // 2) + (x // 2)
            u_plane[u_idx] = max(0, min(255, ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128))
            v_plane[u_idx] = max(0, min(255, ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128))
    
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_yuv420_10le(filename, pixels):
    """Save as YUV420 10-bit LE (2 bytes per sample, little-endian)"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h * 2)
    uv_w = (w + 1) // 2
    uv_h = (h + 1) // 2
    u_plane = bytearray(uv_w * uv_h * 2)
    v_plane = bytearray(uv_w * uv_h * 2)
    
    for idx, (r, g, b) in enumerate(pixels):
        x = idx % w
        y = idx // w
        y10 = ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16
        y10 = max(0, min(1023, y10 << 2))
        struct.pack_into('<H', y_plane, idx * 2, y10)
        
        # Subsample UV at top-left of each 2x2 block
        if (x % 2 == 0) and (y % 2 == 0):
            u_idx = (y // 2) * uv_w + (x // 2)
            u10 = ((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128
            u10 = max(0, min(1023, u10 << 2))
            v10 = ((112 * r - 94 * g - 18 * b + 128) >> 8) + 128
            v10 = max(0, min(1023, v10 << 2))
            struct.pack_into('<H', u_plane, u_idx * 2, u10)
            struct.pack_into('<H', v_plane, u_idx * 2, v10)
    
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def save_yuv420_12le(filename, pixels):
    """Save as YUV420 12-bit LE"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h * 2)
    uv_w = (w + 1) // 2
    uv_h = (h + 1) // 2
    u_plane = bytearray(uv_w * uv_h * 2)
    v_plane = bytearray(uv_w * uv_h * 2)

    for idx, (r, g, b) in enumerate(pixels):
        x = idx % w
        y = idx // w
        y12 = (((66 * r + 129 * g + 25 * b + 128) >> 8) + 16) << 4
        y12 = max(0, min(4095, y12))
        struct.pack_into('<H', y_plane, idx * 2, y12)
        if (x % 2 == 0) and (y % 2 == 0):
            u_idx = (y // 2) * uv_w + (x // 2)
            u12 = (((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128) << 4
            v12 = (((112 * r - 94 * g - 18 * b + 128) >> 8) + 128) << 4
            struct.pack_into('<H', u_plane, u_idx * 2, max(0, min(4095, u12)))
            struct.pack_into('<H', v_plane, u_idx * 2, max(0, min(4095, v12)))
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")


def save_yuv420_16le(filename, pixels):
    """Save as YUV420 16-bit LE"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h * 2)
    uv_w = (w + 1) // 2
    uv_h = (h + 1) // 2
    u_plane = bytearray(uv_w * uv_h * 2)
    v_plane = bytearray(uv_w * uv_h * 2)

    for idx, (r, g, b) in enumerate(pixels):
        x = idx % w
        y = idx // w
        y16 = (((66 * r + 129 * g + 25 * b + 128) >> 8) + 16) << 8
        struct.pack_into('<H', y_plane, idx * 2, y16)
        if (x % 2 == 0) and (y % 2 == 0):
            u_idx = (y // 2) * uv_w + (x // 2)
            u16 = (((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128) << 8
            v16 = (((112 * r - 94 * g - 18 * b + 128) >> 8) + 128) << 8
            struct.pack_into('<H', u_plane, u_idx * 2, u16)
            struct.pack_into('<H', v_plane, u_idx * 2, v16)
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")


def save_yuv444_10le(filename, pixels):
    """Save as YUV444 10-bit LE"""
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h * 2)
    u_plane = bytearray(w * h * 2)
    v_plane = bytearray(w * h * 2)
    for idx, (r, g, b) in enumerate(pixels):
        y10 = (((66 * r + 129 * g + 25 * b + 128) >> 8) + 16) << 2
        u10 = (((-38 * r - 74 * g + 112 * b + 128) >> 8) + 128) << 2
        v10 = (((112 * r - 94 * g - 18 * b + 128) >> 8) + 128) << 2
        struct.pack_into('<H', y_plane, idx * 2, max(0, min(1023, y10)))
        struct.pack_into('<H', u_plane, idx * 2, max(0, min(1023, u10)))
        struct.pack_into('<H', v_plane, idx * 2, max(0, min(1023, v10)))
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(u_plane)
        f.write(v_plane)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")


def save_yv12(filename, pixels):
    """Save as YV12 (Y plane, then V plane, then U plane)"""
    # Same as YUV420 but V and U swapped
    w, h = WIDTH, HEIGHT
    y_plane = bytearray(w * h)
    uv_plane = bytearray(((w + 1) // 2) * ((h + 1) // 2))
    for idx, (r, g, b) in enumerate(pixels):
        y_plane[idx] = max(0, min(255, ((66 * r + 129 * g + 25 * b + 128) >> 8) + 16))
    # Store dummy V and U (we'll just copy Y for simplicity)
    with open(filename, 'wb') as f:
        f.write(y_plane)
        f.write(uv_plane)  # V plane (empty/dummy)
        f.write(uv_plane)  # U plane (empty/dummy)
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")


def save_gray16(filename, pixels):
    """Save as 16-bit grayscale LE"""
    with open(filename, 'wb') as f:
        for r, g, b in pixels:
            gray = (r * 77 + g * 150 + b * 29) >> 8
            gray16 = gray * 257  # Scale to 16-bit
            f.write(struct.pack('<H', gray16))
    print(f"  Created: {filename} ({os.path.getsize(filename)} bytes)")

def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Generating test data in: {output_dir}")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    print()
    
    pixels = create_test_pattern_rgb(WIDTH, HEIGHT)
    
    # RGB formats
    print("--- RGB / BGR Formats ---")
    save_rgb24(os.path.join(output_dir, "test_rgb24_352x288.raw"), pixels)
    save_bgr24(os.path.join(output_dir, "test_bgr24_352x288.raw"), pixels)
    save_rgb32(os.path.join(output_dir, "test_rgb32_352x288.raw"), pixels)
    save_bgr32(os.path.join(output_dir, "test_bgr32_352x288.raw"), pixels)
    save_rgb565(os.path.join(output_dir, "test_rgb16_352x288.raw"), pixels)
    save_bgr565(os.path.join(output_dir, "test_bgr16_352x288.raw"), pixels)
    save_rgb48(os.path.join(output_dir, "test_rgb48_352x288.raw"), pixels)
    save_rgba64(os.path.join(output_dir, "test_rgba64_352x288.raw"), pixels)
    
    # YUV formats
    print()
    print("--- YUV Formats ---")
    save_yuv444_planar(os.path.join(output_dir, "test_yuv444_352x288.yuv"), pixels)
    save_yuv420_planar(os.path.join(output_dir, "test_yuv420_352x288.yuv"), pixels)
    save_yuv420_10le(os.path.join(output_dir, "test_yuv420_10le_352x288.yuv"), pixels)
    save_yuv420_12le(os.path.join(output_dir, "test_yuv420_12le_352x288.yuv"), pixels)
    save_yuv420_16le(os.path.join(output_dir, "test_yuv420_16le_352x288.yuv"), pixels)
    save_yuv444_10le(os.path.join(output_dir, "test_yuv444_10le_352x288.yuv"), pixels)
    save_yv12(os.path.join(output_dir, "test_yv12_352x288.yuv"), pixels)
    
    # Grayscale
    print()
    print("--- Grayscale Formats ---")
    save_gray16(os.path.join(output_dir, "test_gray16_352x288.raw"), pixels)
    
    print()
    print("Done! Open these files in YUVplayer and select the appropriate format.")
    print("Expected: Color bars at top, RGB gradient in middle, checkerboard at bottom.")

if __name__ == "__main__":
    main()
