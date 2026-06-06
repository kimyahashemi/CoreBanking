from ttkbootstrap import Window as TTKWindow

class Window(TTKWindow):
    def __init__(self, app_title):
        super().__init__(themename="lumen")

        self.title(app_title)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
    def change_theme(self, mode: str):
        # Map Dark/Light to real ttkbootstrap themes
        theme_map = {
            "Light": "lumen",
            "Dark": "darkly"
        }
        new_theme = theme_map.get(mode)
        self.style.theme_use(new_theme)
        self.current_theme = new_theme
    
    def window_resize(self, value):
        self.geometry(value)
    
    def show(self):
        self.mainloop() 
