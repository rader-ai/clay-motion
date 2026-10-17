// Frame-by-frame measurement of public clay clips, as used for research/16.
// Run in a browser tab on https://commons.wikimedia.org (same-origin API access; the video files
// on upload.wikimedia.org allow canvas reads). Paste into the console, then:
//   const L = await analyzeClip('Threadwood - Flumpy.webm', 5);   // title, start second
//   const r = Object.assign(cadence(L, 0.002), lookStats(cropSamples(L.samples)));
// Playback runs at half speed from a downloaded blob so frames aren't dropped.

async function fileUrl(title) {
  const q = new URLSearchParams({ action: 'query', titles: 'File:' + title, prop: 'imageinfo', iiprop: 'url', format: 'json', formatversion: '2' });
  const r = await fetch('/w/api.php?' + q).then(r => r.json());
  return r.query.pages[0].imageinfo[0].url;
}

async function analyzeClip(title, start = 5, maxSec = 24, rate = 0.5) {
  const W = 128, H = 72, SW = 320, SH = 180;
  const blob = await fetch(await fileUrl(title)).then(r => r.blob());
  const src = URL.createObjectURL(blob);
  const v = document.createElement('video'); v.muted = true; v.preload = 'auto'; v.src = src;
  try {
    await new Promise((res, rej) => { v.onloadedmetadata = res; v.onerror = () => rej('load error'); });
    const t0 = Math.min(start, Math.max(0, v.duration - 3)), t1 = Math.min(v.duration - 0.2, t0 + maxSec);
    v.currentTime = t0; await new Promise(r => (v.onseeked = r));
    const c = Object.assign(document.createElement('canvas'), { width: W, height: H }), ctx = c.getContext('2d', { willReadFrequently: true });
    const c2 = Object.assign(document.createElement('canvas'), { width: SW, height: SH }), ctx2 = c2.getContext('2d', { willReadFrequently: true });
    const lum = d => { const g = new Float32Array(d.length / 4); for (let i = 0, j = 0; i < d.length; i += 4, j++) g[j] = 0.2126 * d[i] + 0.7152 * d[i + 1] + 0.0722 * d[i + 2]; return g; };
    let prev = null, n = 0; const frames = [], times = [], samples = [];
    v.playbackRate = rate;
    await new Promise((resolve, reject) => {
      const wd = setTimeout(() => { v.pause(); reject('watchdog'); }, (maxSec / rate) * 2500 + 20000);
      const cb = (now, md) => {
        times.push(md.mediaTime);
        ctx.drawImage(v, 0, 0, W, H); const g = lum(ctx.getImageData(0, 0, W, H).data);
        if (prev) { let s = 0, big = 0; for (let i = 0; i < g.length; i++) { const d = Math.abs(g[i] - prev[i]); s += d; if (d > 10) big++; } frames.push([s / g.length, big / g.length]); }
        prev = g; n++;
        if (n % 12 === 6) { ctx2.drawImage(v, 0, 0, SW, SH); samples.push(ctx2.getImageData(0, 0, SW, SH).data); }
        if (md.mediaTime >= t1 || v.ended) { clearTimeout(wd); v.pause(); resolve(); } else v.requestVideoFrameCallback(cb);
      };
      v.requestVideoFrameCallback(cb); v.play();
    });
    return { title, frames, times, samples, w: v.videoWidth, h: v.videoHeight };
  } finally { v.removeAttribute('src'); v.load(); URL.revokeObjectURL(src); }
}

// A frame is a new pose when more than bthr of its pixels changed by more than 10 levels (of 255).
// 'G' marks a playback gap, 'C' a cut. Runs of identical images give the hold lengths.
function cadence(L, bthr = 0.002) {
  const dt = []; for (let i = 1; i < L.times.length; i++) dt.push(L.times[i] - L.times[i - 1]);
  const nom = [...dt].sort((a, b) => a - b)[Math.floor(dt.length / 2)], fps = 1 / nom;
  const cls = L.frames.map(([m, b], i) => dt[i] > 1.5 * nom ? 'G' : (m > 25 && b > 0.5) ? 'C' : b > bthr ? (b > 0.3 ? 'M' : 'm') : '=');
  const runs = []; let cur = 1, valid = true;
  for (const c of cls) { if (c === '=') { cur++; continue; } if (c === 'G' || c === 'C') { cur = 1; valid = false; continue; } if (valid) runs.push([cur, c]); cur = 1; valid = true; }
  let anim = 0, nr = 0, hold = 0; const f = { 1: 0, 2: 0, 3: 0, 4: 0 };
  for (const [k] of runs) { if (k <= 4) { anim += k; nr++; f[k] += k; } else hold += k; }
  const pct = x => anim ? +(100 * x / anim).toFixed(1) : null;
  return { fps: +fps.toFixed(2), posesPerSec: anim ? +(nr / (anim / fps)).toFixed(1) : null, ones: pct(f[1]), twos: pct(f[2]), threes: pct(f[3]), fours: pct(f[4]),
           holdShare: +(hold / (L.frames.length + 1)).toFixed(2), cuts: cls.filter(c => c === 'C').length, gaps: cls.filter(c => c === 'G').length };
}

// Crop black letterbox or pillarbox borders from the 320x180 samples.
function cropSamples(samples) {
  const W = 320, H = 180, rowM = new Float32Array(H), colM = new Float32Array(W);
  for (const d of samples) for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = 4 * (y * W + x), v = (d[i] + d[i + 1] + d[i + 2]) / 3; rowM[y] += v; colM[x] += v; }
  const n = samples.length || 1; let y0 = 0, y1 = H - 1, x0 = 0, x1 = W - 1;
  while (y0 < H / 3 && rowM[y0] / (n * W) < 12) y0++; while (y1 > 2 * H / 3 && rowM[y1] / (n * W) < 12) y1--;
  while (x0 < W / 3 && colM[x0] / (n * H) < 12) x0++; while (x1 > 2 * W / 3 && colM[x1] / (n * H) < 12) x1--;
  const tmp = Object.assign(document.createElement('canvas'), { width: W, height: H }), tx = tmp.getContext('2d');
  const out = Object.assign(document.createElement('canvas'), { width: W, height: H }), ox = out.getContext('2d', { willReadFrequently: true });
  return samples.map(d => { tx.putImageData(new ImageData(new Uint8ClampedArray(d), W, H), 0, 0); ox.drawImage(tmp, x0, y0, x1 - x0 + 1, y1 - y0 + 1, 0, 0, W, H); return ox.getImageData(0, 0, W, H).data; });
}

// Same formulas as tools/look_stats.py.
function lookStats(samples) {
  const W = 320, H = 180, lums = [], sats = [], warm = [], cf = [], sharp = [], ratio = []; let lo = 0, hi = 0, tot = 0;
  for (const d of samples) {
    const g = new Float32Array(W * H); let rg = 0, yb = 0, rg2 = 0, yb2 = 0, sS = 0, wS = 0;
    for (let i = 0, j = 0; i < d.length; i += 4, j++) {
      const r = d[i], G = d[i + 1], b = d[i + 2], y = 0.2126 * r + 0.7152 * G + 0.0722 * b; g[j] = y; if (j % 7 === 0) lums.push(y);
      const mx = Math.max(r, G, b), mn = Math.min(r, G, b); sS += mx ? (mx - mn) / mx : 0; wS += r - b;
      const a1 = r - G, a2 = 0.5 * (r + G) - b; rg += a1; yb += a2; rg2 += a1 * a1; yb2 += a2 * a2; if (y < 8) lo++; if (y > 247) hi++; tot++;
    }
    const N = W * H, mrg = rg / N, myb = yb / N;
    sats.push(sS / N); warm.push(wS / N); cf.push(Math.hypot(Math.sqrt(rg2 / N - mrg * mrg), Math.sqrt(yb2 / N - myb * myb)) + 0.3 * Math.hypot(mrg, myb));
    let sc = 0, sc2 = 0, nc = 0, se = 0, se2 = 0, ne = 0;
    for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
      const k = y * W + x, l = 4 * g[k] - g[k - 1] - g[k + 1] - g[k - W] - g[k + W];
      if (x > W * 0.3 && x < W * 0.7 && y > H * 0.25 && y < H * 0.75) { sc += l; sc2 += l * l; nc++; } else { se += l; se2 += l * l; ne++; }
    }
    const vc = sc2 / nc - (sc / nc) ** 2, ve = se2 / ne - (se / ne) ** 2; sharp.push(Math.sqrt((vc * nc + ve * ne) / (nc + ne))); ratio.push(vc / (ve + 1e-6));
  }
  lums.sort((a, b) => a - b); const q = p => +lums[Math.floor(p * (lums.length - 1))].toFixed(1);
  const med = a => +[...a].sort((x, y) => x - y)[Math.floor(a.length / 2)].toFixed(3);
  return { lum: { p5: q(0.05), p50: q(0.5), p95: q(0.95) }, sat: med(sats), warm: med(warm), colorfulness: med(cf),
           clipLoPct: +(100 * lo / tot).toFixed(2), clipHiPct: +(100 * hi / tot).toFixed(2), sharp: med(sharp), centerEdgeRatio: med(ratio) };
}
