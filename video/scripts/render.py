"""Renderiza o pitch do PIPHPO em MP4 1080p30.

Uso (a partir de video/):
  python3 scripts/render.py                        # sem áudio, com capa
  python3 scripts/render.py --audio out/marcha.wav # com trilha
  python3 scripts/render.py --page src/variantes_pitch_15bpm_claro.html --cover "" --out out/claro.mp4

Requisitos: npm install (fontes), pip install playwright, ffmpeg no PATH, Chromium do Playwright.
A página expõe window.render(t) e é capturada quadro a quadro (determinístico).
"""
import argparse, subprocess, pathlib
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('--page', default='src/pitch.html')
ap.add_argument('--cover', default='src/cover.html', help='página da capa (vazio = sem capa)')
ap.add_argument('--out', default='out/PIPHPO_pitch.mp4')
ap.add_argument('--audio', default='')
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--duration', type=float, default=80.0)
a = ap.parse_args()
root = pathlib.Path(__file__).resolve().parent.parent
raw = root / 'out' / '_raw.mp4'
cover_png = root / 'out' / 'capa.png'

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    if a.cover:
        pg.goto((root / a.cover).as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        pg.screenshot(path=str(cover_png))
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(a.fps),
                           '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
                           '-preset', 'medium', str(raw)], stdin=subprocess.PIPE)
    pg.goto((root / a.page).as_uri()); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    n = int(a.fps * a.duration)
    for i in range(n):
        pg.evaluate(f'render({i / a.fps})')
        ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        if i % 300 == 0: print(f'{i}/{n}', flush=True)
    b.close(); ff.stdin.close(); ff.wait()

cmd = ['ffmpeg', '-y', '-v', 'error']
if a.cover:
    cmd += ['-loop', '1', '-t', '2.0', '-framerate', str(a.fps), '-i', str(cover_png), '-i', str(raw)]
    fc = ('[0:v]fps=30,format=yuv420p,setsar=1,settb=AVTB[c];[1:v]fps=30,format=yuv420p,setsar=1,settb=AVTB[m];'
          '[c][m]xfade=transition=fade:duration=0.8:offset=1.2[v]')
    delay = 1200
else:
    cmd += ['-i', str(raw)]; fc = '[0:v]null[v]'; delay = 0
maps = ['-map', '[v]']
if a.audio:
    idx = 2 if a.cover else 1
    cmd += ['-i', str(root / a.audio)]
    fc += f';[{idx}:a]adelay={delay}|{delay},apad[a]'
    maps += ['-map', '[a]', '-c:a', 'aac', '-b:a', '192k', '-shortest']
cmd += ['-filter_complex', fc] + maps + ['-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                                         '-movflags', '+faststart', str(root / a.out)]
subprocess.run(cmd, check=True); raw.unlink(missing_ok=True)
print('ok ->', a.out)
