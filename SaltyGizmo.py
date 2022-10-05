from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivymd.app import MDApp
import bcrypt


class MainScreen(Screen):
    store = JsonStore("assets/saved_salts.json")

    def flip(self):
        self.ids.salt.text = ""
        self.ids.password.text = ""
        self.ids.enc_password.text = ""

    def gen_salt(self):
        # print("gen_salt working")
        salt = bcrypt.gensalt().decode()
        self.ids.salt.text = str(salt)

    def remove(self):
        salt = self.ids.enc_password.text[:29]
        if len(self.ids.enc_password.text) > 31:
            self.ids.enc_password.text = self.ids.enc_password.text.replace(salt, "")

    def save_salt(self):
        # print("save_salt working")
        if self.store.exists('salt'):
            self.store.delete('salt')
        salt = self.ids.salt.text
        self.store.put('salt', name=salt)

    def get_salt(self):
        # print("get_salt working")
        if self.store.exists('salt'):
            salt = str(self.store.get('salt')['name'])
            self.ids.salt.text = salt
        else:
            self.saltgen.text = "You don't have a salt saved"

    def encrypt(self):
        # print("Encrypt working")
        user_pass = self.ids.password.text.encode()
        salt = self.ids.salt.text.encode()
        try:
            encrypted_pass = bcrypt.hashpw(user_pass, salt).decode()
            self.ids.enc_password.text = encrypted_pass
        except:
            self.ids.enc_password.text = "Invalid salt"

    def note_screen(self):
        self.parent.current = 'note'

    pass


class NoteScreen(Screen):
    store = JsonStore("assets/saved_notes.json")

    def get_notes(self):
        saved_notes = str(self.store.get('notes')['name'])
        self.ids.notes.text = saved_notes

    def save_notes(self):
        notes = self.ids.notes.text
        self.store.put("notes", name=notes)

    def main_screen(self):
        self.parent.current = 'main'

    pass


class SaltyGizmoApp(MDApp):
    icon = "assets/salttitle.png"

    def build(self):
        Builder.load_file('assets/my.kv')
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(NoteScreen(name="note"))

        return sm


if __name__ == '__main__':
    SaltyGizmoApp().run()
