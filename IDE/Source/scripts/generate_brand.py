"""Generate the same blue forge artwork for the web, Windows executable and Setup."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<defs><linearGradient id="b" x2="1" y2="1"><stop stop-color="#102e53"/><stop offset="1" stop-color="#061322"/></linearGradient>
<linearGradient id="f" x2="0" y2="1"><stop stop-color="#b8efff"/><stop offset="1" stop-color="#42b8ff"/></linearGradient></defs>
<rect x="8" y="8" width="240" height="240" rx="58" fill="url(#b)" stroke="#368dd1" stroke-width="3"/>
<path d="M168 50h30v57h-30z" fill="#64c9ff"/><path d="M163 46h40v12h-40z" fill="#b8efff"/>
<path d="M43 123l85-65 85 65-13 17-72-54-72 54z" fill="#83d6ff"/>
<path d="M61 135l67-50 67 50v68H61z" fill="#2d8fd5"/>
<path d="M87 203v-45a41 41 0 0 1 82 0v45" fill="#071d33" stroke="#a0e3ff" stroke-width="9"/>
<path d="M128 120c9 26-14 32-9 47 9-3 10-11 13-17 23 24 26 44-4 44-29 0-32-25-16-43-1 12 2 15 5 15-9-20 12-26 11-46z" fill="url(#f)"/>
<path d="M51 206h154" stroke="#a6e5ff" stroke-width="12" stroke-linecap="round"/>
<path d="M175 30l-3-10m18 11 5-12" stroke="#6dcfff" stroke-width="5" stroke-linecap="round"/>
</svg>'''


def main():
    assets = ROOT / 'assets'
    public = ROOT / 'frontend' / 'public'
    assets.mkdir(exist_ok=True)
    (assets / 'forge.svg').write_text(SVG, encoding='utf-8')
    (public / 'forge.svg').write_text(SVG, encoding='utf-8')
    scale = 4
    image = Image.new('RGBA', (256*scale, 256*scale))
    draw = ImageDraw.Draw(image)
    def box(coords, color, radius=0, outline=None, width=1):
        draw.rounded_rectangle(tuple(int(v*scale) for v in coords), radius=radius*scale, fill=color, outline=outline, width=width*scale)
    def polygon(points, color):
        draw.polygon([(int(x*scale),int(y*scale)) for x,y in points], fill=color)
    box((8,8,248,248), '#0b213a',58,'#368dd1',3)
    box((168,50,198,107),'#64c9ff')
    box((163,46,203,58),'#b8efff')
    polygon([(43,123),(128,58),(213,123),(200,140),(128,86),(56,140)],'#83d6ff')
    polygon([(61,135),(128,85),(195,135),(195,203),(61,203)],'#2d8fd5')
    box((83,113,173,220),'#a0e3ff',45)
    box((93,123,163,220),'#071d33',35)
    polygon([(128,133),(139,158),(134,170),(145,162),(151,183),(144,195),(116,196),(105,182),(111,165),(115,181),(122,171),(120,158)],'#7fdcff')
    polygon([(130,162),(139,183),(132,195),(120,190),(122,180)],'#def8ff')
    box((45,200,211,212),'#a6e5ff',6)
    draw.line([(175*scale,30*scale),(172*scale,20*scale)],fill='#6dcfff',width=5*scale)
    draw.line([(190*scale,31*scale),(195*scale,19*scale)],fill='#6dcfff',width=5*scale)
    image=image.resize((256,256),Image.Resampling.LANCZOS)
    image.save(assets/'forge.png')
    image.save(assets/'forge.ico',sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
    image.save(public/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(256,256)])
    print('Blue forge SVG, PNG and multi-resolution ICO generated.')


if __name__ == '__main__':main()
