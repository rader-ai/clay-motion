"""Look statistics, same formulas as the in-browser lookStats used on the public clips.
Input: RGB uint8 images. Each image is resized to 320x180 first."""
import numpy as np
from PIL import Image

def prep(img):
    im = img.convert('RGB').resize((320, 180), Image.BILINEAR)
    return np.asarray(im).astype(np.float64)

def look_stats(imgs):
    lums, sats, warm, cf, sharp, ratio = [], [], [], [], [], []
    lo = hi = tot = 0
    hue = np.zeros(12)
    for img in imgs:
        d = prep(img); r, g, b = d[..., 0], d[..., 1], d[..., 2]
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        lums.append(y.ravel()[::7])
        mx = d.max(-1); mn = d.min(-1); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
        sats.append(s.mean()); warm.append((r - b).mean())
        a1 = r - g; a2 = 0.5 * (r + g) - b
        cf.append(np.hypot(a1.std(), a2.std()) + 0.3 * np.hypot(a1.mean(), a2.mean()))
        lo += (y < 8).sum(); hi += (y > 247).sum(); tot += y.size
        m = (s > 0.15) & (mx > 40) & (mx > mn)
        rr, gg, bb, mxx, mnn = r[m], g[m], b[m], mx[m], mn[m]
        h = np.where(mxx == rr, np.mod((gg - bb) / (mxx - mnn), 6), np.where(mxx == gg, (bb - rr) / (mxx - mnn) + 2, (rr - gg) / (mxx - mnn) + 4))
        h = np.mod(h * 60 + 360, 360)
        np.add.at(hue, (h // 30).astype(int) % 12, s[m])
        lap = 4 * y[1:-1, 1:-1] - y[1:-1, :-2] - y[1:-1, 2:] - y[:-2, 1:-1] - y[2:, 1:-1]
        H, W = y.shape; yy, xx = np.mgrid[1:H - 1, 1:W - 1]
        c = (xx > W * 0.3) & (xx < W * 0.7) & (yy > H * 0.25) & (yy < H * 0.75)
        vc, ve = lap[c].var(), lap[~c].var()
        sharp.append(np.sqrt((vc * c.sum() + ve * (~c).sum()) / c.size)); ratio.append(vc / (ve + 1e-6))
    L = np.sort(np.concatenate(lums)); q = lambda p: round(float(L[int(p * (len(L) - 1))]), 1)
    med = lambda a: round(float(np.sort(a)[len(a) // 2]), 3)
    ht = hue.sum() or 1
    return {'lum': {'p5': q(.05), 'p25': q(.25), 'p50': q(.5), 'p75': q(.75), 'p95': q(.95)}, 'sat': med(sats), 'warm': round(med(warm), 1),
            'colorfulness': round(med(cf), 1), 'clipLoPct': round(100 * lo / tot, 2), 'clipHiPct': round(100 * hi / tot, 2),
            'sharp': round(med(sharp), 2), 'centerEdgeRatio': med(ratio), 'hue12': [int(round(100 * x / ht)) for x in hue]}

def crop_stats(img):
    """Surface statistics on a clay crop (any size): local contrast, highlight shape, fine detail energy."""
    d = np.asarray(img.convert('RGB')).astype(np.float64) / 255.0
    y = 0.2126 * d[..., 0] + 0.7152 * d[..., 1] + 0.0722 * d[..., 2]
    p = np.percentile(y, [5, 50, 95, 99.5])
    # fine detail: energy in the top octave of the power spectrum, relative to total
    f = np.abs(np.fft.fftshift(np.fft.fft2(y - y.mean()))) ** 2
    H, W = y.shape; yy, xx = np.mgrid[-H // 2:H - H // 2, -W // 2:W - W // 2]; rad = np.hypot(yy / (H / 2), xx / (W / 2))
    hf = f[(rad > 0.5) & (rad <= 1)].sum() / max(f[(rad > 0.02)].sum(), 1e-12)
    mf = f[(rad > 0.12) & (rad <= 0.5)].sum() / max(f[(rad > 0.02)].sum(), 1e-12)
    # highlight: share of pixels within 90% of the 99.5th percentile (small = tight specular)
    hl = float((y > 0.9 * p[3]).mean())
    mx = d.max(-1); mn = d.min(-1); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    return {'p5': round(p[0], 3), 'p50': round(p[1], 3), 'p95': round(p[2], 3), 'contrast_p95_p5': round(p[2] / max(p[0], 1e-3), 2),
            'hf_energy': round(float(hf), 4), 'mf_energy': round(float(mf), 4), 'highlight_area': round(hl, 4), 'sat': round(float(s.mean()), 3)}
