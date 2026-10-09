# yuvplayer

Lightweight YUV/RGB raw data viewer with OpenGL rendering.  
Supports 36 color formats, multiple bit depths, color matrix selection, and real-time pixel inspection.

---

## Supported Formats

### YUV Planar
* YUV444 8-bit, YUV422 8-bit, YUV420 8-bit, YV12 8-bit
* YUV420 10-bit LE/BE, YUV444 10-bit LE/BE
* YUV420 12-bit LE/BE
* YUV420 16-bit LE/BE

### YUV Packed / Semi-planar
* YUV444 (Packed)
* UYVY, YUYV, YVYU, VYUY
* NV12, NV21 (420SP)
* NV16, NV61 (422SP)
* NV24, NV42 (444SP)

### RGB / BGR (8-bit)
* RGB24 (RGB888), RGB32 (RGBA8888), RGB16 (RGB565)
* RGB555 (XRGB1555), RGBA5551
* BGR24 (BGR888), BGR32 (BGRA8888), BGR16 (BGR565), BGR555

### RGB High Bit-depth
* RGB48 (16-bit/channel, LE)
* RGBA64 (16-bit/channel, LE)

### Grayscale
* Y (8-bit), Gray16 (16-bit, LE)

---

## Features

* **Color Range**: Limited (16-235) / Full (0-255)
* **Color Matrix**: BT.601 (SD), BT.709 (HD), BT.2020 (UHD)
* **Zoom**: 4:1 ~ 1:8
* **Vertical Flip**: toggle for bottom-up formats
* **Real-time Pixel Info**: mouse hover shows (x,y) and [R,G,B] in title bar
* **Frame Navigation**: menu (Frame menu), slider, keyboard (`→`/`←`, `d`/`f`), goto dialog
* **Playback**: play/pause at 30 fps
* **Segment Overlay**: 64x64 / 32x32 / 16x16 grid markers
* **Save**: frame as YUV444/422/420 or BMP
* **Auto Size Detection**: from filename patterns (CIF, VGA, 1080p, 4K, etc.)
* **Drag & Drop**: open file by dropping onto the window

---

## Hot Keys

| Key | Action |
|-----|--------|
| `→` / `f` | Next frame |
| `←` / `d` | Previous frame |
| `↑` | Zoom in |
| `↓` | Zoom out |
| `p` / `Space` | Play / Pause toggle |
| `o` | Open file |
| `g` | Go to frame |
| `x` | Exit |

---

## Build

Requires Visual Studio 2022 with **Desktop development with C++** workload and **MFC for x86** component.

```powershell
# Open "Developer Command Prompt for VS 2022"
msbuild yuvplayer.sln /p:Configuration=Release /p:Platform=Win32
```

Output: `Release\yuvplayer.exe`
