from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread
import threading, os, json
from tiktok_ai_core import generate_and_save_video, update_metrics_display

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_config(cfg):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(cfg, f)

class UI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=8, padding=12, **kwargs)
        self.add_widget(Label(text='TikTok AI Mobile Lite', font_size='20sp', size_hint=(1, .08)))
        self.theme_input = TextInput(text='curiosidades sobre ciência', size_hint=(1, .12))
        self.add_widget(self.theme_input)
        btn_layout = BoxLayout(size_hint=(1, .12))
        self.gen_btn = Button(text='🎥 Gerar Vídeo')
        self.gen_btn.bind(on_press=self.on_generate)
        self.open_folder_btn = Button(text='📁 Abrir pasta (placeholder)')
        btn_layout.add_widget(self.gen_btn)
        btn_layout.add_widget(self.open_folder_btn)
        self.add_widget(btn_layout)
        self.log = Label(text='Logs:', size_hint=(1, .68))
        scroll = ScrollView(size_hint=(1, .68))
        scroll.add_widget(self.log)
        self.add_widget(scroll)
        update_metrics_display(self.log)

    @mainthread
    def append_log(self, txt):
        self.log.text += '\n' + txt

    def on_generate(self, instance):
        theme = self.theme_input.text.strip() or 'curiosidades'
        threading.Thread(target=self._generate_thread, args=(theme,), daemon=True).start()

    def _generate_thread(self, theme):
        self.append_log('Iniciando geração de vídeo...')
        try:
            out = generate_and_save_video(theme)
            self.append_log('✅ Vídeo gerado: ' + out)
        except Exception as e:
            self.append_log('Erro: ' + str(e))

class TikTokApp(App):
    def build(self):
        return UI()

if __name__ == '__main__':
    TikTokApp().run()
