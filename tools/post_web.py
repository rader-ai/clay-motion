"""Post for test renders: sensor noise (signal dependent, per pose), small vignette, then a web-video round trip
so renders are compared with the public clips on equal terms (those are VP9 web encodes)."""
import numpy as np, subprocess, os, tempfile, sys
from PIL import Image

def srgb_to_lin(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def lin_to_srgb(x): return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(np.clip(x, 0, None), 1 / 2.4) - 0.055)

def post(img, seed=0, a=1 / 70000, b=(8 / 70000) ** 2, vignette=0.12, chroma=0.6, gain=1.0, noise_mult=1.0):
    """a, b follow LOOK_DEV section 6 but rescaled to a 0..1 signal (an approximation: we work on
    sRGB-decoded display values, not the true scene-linear render)."""
    rng = np.random.default_rng(seed)
    d = np.asarray(img.convert('RGB')).astype(np.float64) / 255.0
    lin = srgb_to_lin(d) * gain
    H, W = lin.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]; r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    lin = lin * (1 - vignette * r2 / 2)[..., None]
    lum = lin.mean(-1, keepdims=True)
    sig = np.sqrt(np.clip(a * lum + b, 0, None))
    nl = rng.normal(0, 1, (H, W, 1)); nc = rng.normal(0, 1, (H, W, 3)) * chroma
    noise = (nl + nc) / np.sqrt(1 + chroma ** 2) * sig
    # blur the noise about 0.6 px so it reads like a demosaiced sensor
    from scipy.ndimage import gaussian_filter
    noise = np.stack([gaussian_filter(noise[..., c], 0.6) for c in range(3)], -1) * 1.6 * noise_mult
    out = lin_to_srgb(np.clip(lin + noise, 0, 1))
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))

def web_roundtrip(img, bitrate='2.5M'):
    with tempfile.TemporaryDirectory() as t:
        for i in range(6): img.save(f'{t}/{i:02d}.png')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '24', '-i', f'{t}/%02d.png', '-c:v', 'libvpx-vp9', '-b:v', bitrate, '-pix_fmt', 'yuv420p', f'{t}/o.webm'], check=True)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{t}/o.webm', '-vf', 'select=eq(n\\,3)', '-vframes', '1', f'{t}/f.png'], check=True)
        return Image.open(f'{t}/f.png').convert('RGB').copy()

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    im = Image.open(src)
    web_roundtrip(post(im)).save(dst)
