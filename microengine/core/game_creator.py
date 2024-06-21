import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
import os
import sys
from PIL import Image, ImageTk
import json


class BaseClass:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name}


class ObjectClass(BaseClass):
    def __init__(self, name):
        super().__init__(name)


class ScreenClass(BaseClass):
    def __init__(self, name):
        super().__init__(name)
        self.image_path = None

    def to_dict(self):
        return {"name": self.name, "image_path": self.image_path}


class ScriptClass(BaseClass):
    def __init__(self, name):
        super().__init__(name)


class UIClass(BaseClass):
    def __init__(self, name):
        super().__init__(name)


class App:
    def __init__(self, root, project_path):
        self.root = root
        self.project_path = project_path
        self.config_path = os.path.join(project_path, "config.json")
        self.root.title("Micro Engine - Game Creator")
        self.root.geometry('1280x720')
        self.root.iconbitmap(r"C:\Users\Admin\Desktop\microengine\assets\micro engine logo.ico")
        self.root.configure(bg='#2E2E2E')
        self.current_screen = None
        self.data = {
            "Objects": [],
            "Screens": [],
            "Scripts": [],
            "UI": []
        }

        self.create_menu()
        self.create_main_frame()
        self.create_tool_bar()
        self.create_hierarchy_panel()
        self.create_inspector_panel()
        self.create_project_panel()
        self.create_viewport()

        self.load_config()
        self.populate_hierarchy()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        project_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Project", menu=project_menu)
        project_menu.add_command(label="Save", command=self.save_project)
        project_menu.add_separator()
        project_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help", command=self.help)
        help_menu.add_command(label="About Micro Engine", command=self.about)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def create_tool_bar(self):
        toolbar = tk.Frame(self.main_frame, bg='#3C3C3C', height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        select_button = tk.Button(toolbar, text="Select", command=self.create_selected_class)
        select_button.pack(side=tk.LEFT, padx=2, pady=2)

    def create_hierarchy_panel(self):
        left_panel = tk.Frame(self.main_frame, bg='#3C3C3C', width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.left_panel_label = tk.Label(left_panel, text="Hierarchy", bg='#3C3C3C', fg='white')
        self.left_panel_label.pack(side=tk.TOP, pady=2)

        self.hierarchy_tree = ttk.Treeview(left_panel)
        self.hierarchy_tree.pack(fill=tk.BOTH, expand=True)

        self.hierarchy_tree.bind("<Button-3>", self.show_context_menu)

        self.objects_category = self.hierarchy_tree.insert("", "end", text="Objects")
        self.screens_category = self.hierarchy_tree.insert("", "end", text="Screens")
        self.scripts_category = self.hierarchy_tree.insert("", "end", text="Scripts")
        self.ui_category = self.hierarchy_tree.insert("", "end", text="UI")

    def create_inspector_panel(self):
        right_panel = tk.Frame(self.main_frame, bg='#3C3C3C', width=200)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.right_panel_label = tk.Label(right_panel, text="Inspector", bg='#3C3C3C', fg='white')
        self.right_panel_label.pack(side=tk.TOP, pady=2)

        self.inspector_frame = tk.Frame(right_panel, bg='#3C3C3C')
        self.inspector_frame.pack(fill=tk.BOTH, expand=True)

    def create_project_panel(self):
        bottom_panel = tk.Frame(self.main_frame, bg='#3C3C3C', height=150)
        bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.bottom_panel_label = tk.Label(bottom_panel, text="Project", bg='#3C3C3C', fg='white')
        self.bottom_panel_label.pack(side=tk.TOP, pady=2)

        self.project_tree = ttk.Treeview(bottom_panel)
        self.project_tree.pack(fill=tk.BOTH, expand=True)

        self.populate_project_tree()

    def create_viewport(self):
        self.viewport = tk.Canvas(self.main_frame, bg='#1E1E1E')
        self.viewport.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.viewport_label = tk.Label(self.viewport, text="Viewport", bg='#1E1E1E', fg='white')
        self.viewport_label.pack()

    def help(self):
        messagebox.showinfo("Help", "Help documentation.")

    def about(self):
        messagebox.showinfo("About Micro Engine", "Micro Engine v1.0\nA simple game engine creator.")

    def create_selected_class(self):
        selected_item = self.hierarchy_tree.focus()
        if selected_item:
            item_text = self.hierarchy_tree.item(selected_item, "text")
            if item_text == "Objects":
                self.create_object()
            elif item_text == "Screens":
                self.create_screen()
            elif item_text == "Scripts":
                self.create_script()
            elif item_text == "UI":
                self.create_ui()

    def create_object(self):
        name = self.create_dialog("Object")
        if name:
            new_object = ObjectClass(name)
            self.data["Objects"].append(new_object.to_dict())
            self.add_to_hierarchy(self.objects_category, new_object.name)

    def create_screen(self):
        name = self.create_dialog("Screen")
        if name:
            new_screen = ScreenClass(name)
            self.data["Screens"].append(new_screen.to_dict())
            self.add_to_hierarchy(self.screens_category, new_screen.name)

    def create_script(self):
        name = self.create_dialog("Script")
        if name:
            new_script = ScriptClass(name)
            self.data["Scripts"].append(new_script.to_dict())
            self.add_to_hierarchy(self.scripts_category, new_script.name)

    def create_ui(self):
        name = self.create_dialog("UI")
        if name:
            new_ui = UIClass(name)
            self.data["UI"].append(new_ui.to_dict())
            self.add_to_hierarchy(self.ui_category, new_ui.name)

    def create_dialog(self, class_name):
        return simpledialog.askstring(f"Create {class_name}", f"Enter {class_name} name:")

    def add_to_hierarchy(self, parent, name):
        self.hierarchy_tree.insert(parent, "end", text=name)
        self.save_config()

    def save_project(self):
        save_path = os.path.join(self.project_path, "project_data.txt")
        with open(save_path, "w") as f:
            for category in [self.objects_category, self.screens_category, self.scripts_category, self.ui_category]:
                for child in self.hierarchy_tree.get_children(category):
                    item_text = self.hierarchy_tree.item(child, "text")
                    f.write(f"{self.hierarchy_tree.item(category, 'text')} - {item_text}\n")
        messagebox.showinfo("Save", "Project saved successfully!")

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.data = json.load(f)

    def populate_hierarchy(self):
        for category, items in self.data.items():
            parent = getattr(self, f"{category.lower()}_category")
            for item in items:
                self.hierarchy_tree.insert(parent, "end", text=item["name"])

    def populate_project_tree(self):
        def add_items(parent, path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = self.project_tree.insert(parent, "end", text=item, open=True)
                    add_items(node, item_path)
                else:
                    self.project_tree.insert(parent, "end", text=item)

        add_items("", self.project_path)

    def show_context_menu(self, event):
        selected_item = self.hierarchy_tree.identify_row(event.y)
        if not selected_item:
            return

        item_text = self.hierarchy_tree.item(selected_item, "text")
        parent_text = self.hierarchy_tree.item(self.hierarchy_tree.parent(selected_item), "text")

        if parent_text == "Screens":
            self.hierarchy_tree.selection_set(selected_item)
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Выбрать изображение",
                                     command=lambda: self.select_image_for_screen(selected_item))
            context_menu.post(event.x_root, event.y_root)

    def select_image_for_screen(self, item):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            screen_name = self.hierarchy_tree.item(item, "text")
            for screen in self.data["Screens"]:
                if screen["name"] == screen_name:
                    screen["image_path"] = file_path
                    break
            self.current_screen = ScreenClass(screen_name)
            self.current_screen.image_path = file_path
            self.display_image_in_viewport(file_path)
            self.save_config()

    def display_image_in_viewport(self, image_path):
        image = Image.open(image_path)
        image = image.resize((self.viewport.winfo_width(), self.viewport.winfo_height()), Image.LANCZOS)
        self.viewport_image = ImageTk.PhotoImage(image)
        self.viewport.create_image(0, 0, anchor=tk.NW, image=self.viewport_image)


def main():
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "No project path provided.")
        return

    project_path = sys.argv[1]
    root = tk.Tk()
    app = App(root, project_path)
    root.mainloop()


if __name__ == "__main__":
    main()
