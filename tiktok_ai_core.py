import os, random, sqlite3, textwrap, time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

PROJECT_DIR = os.path.dirname(__file__)
TEMP_DIR = os.path.join(PROJECT_DIR, 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)
DB_PATH = os.path.join(PROJECT_DIR, 'banco_videos.db')

# Lightweight local script generator: templates + synonym substitution
TEMPLATES = [
    'Você sabia que {fact}?',
    'Curiosidade: {fact}.',
    'Fato interessante: {fact}.',
    'Sabia que {fact}? Veja!'
]

SAMPLE_FACTS = [
    'o Sol é tão grande que caberiam 1.3 milhão de Terras dentro dele',
    'as formigas conseguem carregar até 50 vezes o seu peso',
    'o Polvo tem três corações',
    'a Lua se afasta da Terra 3.8 cm por ano',
    'o mel não estraga, foi encontrado em tumbas egípcias comestível'
]

def generate_script(theme, blocks=4):
    # lightweight approach: pick or synthesize facts based on theme keywords
    facts = []
    words = theme.lower().split()
    # try to pick theme-matching sample facts
    for s in SAMPLE_FACTS:
        if any(w in s for w in words):
            facts.append(s)
    # fill remaining with random samples
    while len(facts) < blocks:
        facts.append(random.choice(SAMPLE_FACTS))
    script = []
    for i in range(blocks):
        tpl = random.choice(TEMPLATES)
        fact = facts[i]
        script.append(tpl.format(fact=fact))
    return script

def make_image_with_text(text, out_path, size=(1080,1920), bgcolor=(18,18,30)):
    img = Image.new('RGB', size, bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 48)
    except:
        font = ImageFont.load_default()
    # wrap text
    lines = textwrap.wrap(text, width=25)
    y = 300
    for ln in lines:
        w,h = draw.textsize(ln, font=font)
        draw.text(((size[0]-w)/2, y), ln, font=font, fill=(230,230,230))
        y += h + 20
    img.save(out_path)
    return out_path

def tts_save(text, out_path, lang='pt'):
    tts = gTTS(text=text, lang=lang)
    tts.save(out_path)
    return out_path

def make_block_clip(text, index):
    audio_path = os.path.join(TEMP_DIR, f'audio_{index}.mp3')
    img_path = os.path.join(TEMP_DIR, f'image_{index}.png')
    tts_save(text, audio_path, lang='pt')
    make_image_with_text(text, img_path)
    audio = AudioFileClip(audio_path)
    img_clip = ImageClip(img_path).set_duration(audio.duration).set_audio(audio)
    return img_clip.set_duration(audio.duration)

def assemble_video(script_lines, out_filename=None):
    if out_filename is None:
        out_filename = os.path.join(PROJECT_DIR, 'video_final_{}.mp4'.format(int(time.time())))
    clips = [make_block_clip(t, i) for i,t in enumerate(script_lines)]
    final = concatenate_videoclips(clips, method='compose', padding=-0.2)
    final.write_videofile(out_filename, fps=24, codec='libx264', audio_codec='aac', threads=2)
    return out_filename

def record_video(theme, filename):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, theme TEXT, filename TEXT, post_time TEXT
    )''')
    cur.execute('INSERT INTO videos(theme,filename,post_time) VALUES (?,?,?)', (theme, filename, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def generate_and_save_video(theme='curiosidades'):
    script = generate_script(theme, blocks=4)
    out = assemble_video(script)
    record_video(theme, out)
    return out

def update_metrics_display(label_widget):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT theme, filename, post_time FROM videos ORDER BY id DESC LIMIT 5')
        rows = cur.fetchall()
        conn.close()
        s = '\n'.join([f'Tema: {r[0]} - {os.path.basename(r[1])} - {r[2]}' for r in rows])
        if hasattr(label_widget, 'text'):
            label_widget.text = label_widget.text + '\n\nÚltimos vídeos:\n' + s
    except Exception as e:
        print('update_metrics_display error', e)
