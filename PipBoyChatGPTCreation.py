import tkinter as tk
from tkinter import ttk, filedialog
import pygame
# Define the main application window
class PipBoyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pip-Boy 3000")
        self.geometry("800x600")
        self.configure(bg="black")

        # Load custom font
        self.font = ("Courier", 12)
        try:
            self.font = ("monofonto", 12)  # Use the custom font if available
        except tk.TclError:
            pass  # Fall back to Courier if the custom font is not found

        # Create a style for the green text
        style = ttk.Style()
        style.configure("TLabel", foreground="lime", background="black", font=self.font)
        style.configure("TFrame", background="black")
        style.configure("TNotebook", background="black", borderwidth=0)
        style.configure("TNotebook.Tab", foreground="lime", background="black", font=self.font)
        style.map("TNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "lime")])

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Create the notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill='both')
        
        # Create Stats tab with sub-tabs
        self.create_stats_tab()

        # Create Inventory tab
        self.create_inventory_tab()

        # Create Data tab
        self.create_data_tab()

        

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(inventory_frame, text="Inventory")

        # Example label (replace with actual content)
        inventory_label = ttk.Label(inventory_frame, text="Inventory Content", style="TLabel")
        inventory_label.pack(pady=10)
        inventory_notebook = ttk.Notebook(inventory_frame)
        inventory_notebook.pack(expand=1, fill='both')

        # Inventory categories and items with stats
        self.categories = {
            "Weapons": {
                "9mm Pistol": {"Damage": "25", "Weight": "2", "Value": "50"},
                "Laser Rifle": {"Damage": "30", "Weight": "5", "Value": "120"},
                "Dynamite": {"Damage": "40", "Weight": "1", "Value": "25"}
            },
            "Apparel": {
                "Merc Adventurer Outfit": {"DT": "8", "Weight": "5", "Value": "40"},
                "Leather Armor": {"DT": "10", "Weight": "15", "Value": "100"},
                "Radiation Suit": {"DT": "2", "Weight": "8", "Value": "60"}
            },
            "Aid": {
                "Stimpak": {"Effect": "+30 HP", "Weight": "0.5", "Value": "75"},
                "RadAway": {"Effect": "-150 rads", "Weight": "0.5", "Value": "20"},
                "Purified Water": {"Effect": "+15 HP", "Weight": "1", "Value": "10"}
            },
            "Misc": {
                "Bobby Pin": {"Weight": "0.1", "Value": "1"},
                "Scrap Metal": {"Weight": "1", "Value": "5"},
                "Pre-War Money": {"Weight": "0", "Value": "10"}
            },
            "Ammo": {
                "9mm Round": {"Weight": "0.04", "Value": "2"},
                "Energy Cell": {"Weight": "0.1", "Value": "4"},
                "Dynamite": {"Weight": "1", "Value": "25"}
            }
        }

        # Dictionary to hold stats labels for each category
        self.stats_labels = {}

        for category, items in self.categories.items():
            category_frame = ttk.Frame(inventory_notebook, style="TFrame")
            inventory_notebook.add(category_frame, text=category)

            item_listbox = tk.Listbox(category_frame, bg="black", fg="lime", font=self.font, selectbackground="lime", selectforeground="black")
            item_listbox.pack(side="left", fill="both", expand=True)
            item_listbox.bind('<<ListboxSelect>>', self.on_item_select)

            for item in items:
                item_listbox.insert(tk.END, item)

            stats_frame = ttk.Frame(category_frame, style="TFrame")
            stats_frame.pack(side="right", fill="both", expand=True, padx=10)

            stats_title = ttk.Label(stats_frame, text="Item Stats", style="TLabel", font=self.font)
            stats_title.pack(pady=5)

            self.stats_labels[category] = {}
            for stat in ["Damage", "DT", "Effect", "Weight", "Value"]:
                stat_label = ttk.Label(stats_frame, text=f"{stat}: ", style="TLabel")
                stat_label.pack(anchor='w')
                self.stats_labels[category][stat] = stat_label

            item_listbox.stats_frame = stats_frame
            item_listbox.category = category  # Save category information in the listbox

    def on_item_select(self, event):
        listbox = event.widget
        selected_index = listbox.curselection()
        if not selected_index:
            return
        selected_item = listbox.get(selected_index)
        category = listbox.category

        # Clear existing stats
        for label in self.stats_labels[category].values():
            label.config(text="")

        # Update stats for the selected item
        item_stats = self.categories[category].get(selected_item, {})

        for stat, value in item_stats.items():
            if stat in self.stats_labels[category]:
                self.stats_labels[category][stat].config(text=f"{stat}: {value}")

    def create_data_tab(self):
        data_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(data_frame, text="Data")

        # Create sub-tabs under Data tab
        sub_notebook = ttk.Notebook(data_frame)
        sub_notebook.pack(expand=1, fill='both')

        # Create Radio sub-tab
        self.create_radio_sub_tab(sub_notebook)

        # Create Map sub-tab
        self.create_map_sub_tab(sub_notebook)
    def create_radio_sub_tab(self, notebook):
        radio_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(radio_frame, text="Radio")

        # MP3 player controls
        self.play_button = ttk.Button(radio_frame, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = ttk.Button(radio_frame, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.stop_button = ttk.Button(radio_frame, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)
        
        # Shuffle toggle button
        self.shuffle_button = ttk.Button(radio_frame, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack(pady=10)

        # File selection and playback status label
        self.music_label = ttk.Label(radio_frame, text="No music loaded", style="TLabel")
        self.music_label.pack(pady=10)

        # Browse button to select MP3 file
        self.browse_button = ttk.Button(radio_frame, text="Browse", command=self.load_music)
        self.browse_button.pack(pady=10)

    def play_music(self):
        pygame.mixer.music.unpause()
        self.music_label.config(text="Music playing...")

    def pause_music(self):
        pygame.mixer.music.pause()
        self.music_label.config(text="Music paused.")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_label.config(text="Music stopped.")

    def load_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            pygame.mixer.music.load(file_path)
            self.music_label.config(text=f"Now playing: {file_path}")
            pygame.mixer.music.play()
            
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.shuffle_button.config(text="Shuffle (ON)")
        else:
            self.shuffle_button.config(text="Shuffle (OFF)")

    def create_map_sub_tab(self, notebook):
        map_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(map_frame, text="Map")

        # Example label (replace with actual content)
        map_label = ttk.Label(map_frame, text="Map Content", style="TLabel")
        map_label.pack(pady=10)

    def create_stats_tab(self):
        stats_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(stats_frame, text="Stats")

        # Create sub-tabs under Stats tab
        sub_notebook = ttk.Notebook(stats_frame)
        sub_notebook.pack(expand=1, fill='both')

        # Create Status sub-tab
        self.create_status_sub_tab(sub_notebook)

        # Create S.P.E.C.I.A.L. sub-tab
        self.create_special_sub_tab(sub_notebook)

        # Create Skills sub-tab
        self.create_skills_sub_tab(sub_notebook)

        # Create Perks sub-tab
        self.create_perks_sub_tab(sub_notebook)

        # Create General sub-tab
        self.create_general_sub_tab(sub_notebook)

    def create_status_sub_tab(self, notebook):
        status_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(status_frame, text="Status")

        # Health and Radiation Labels
        health_label = ttk.Label(status_frame, text="Health: 100%", style="TLabel")
        health_label.pack(pady=5, anchor='w')

        radiation_label = ttk.Label(status_frame, text="Radiation: 0 rads", style="TLabel")
        radiation_label.pack(pady=5, anchor='w')
        # Experience Counter with adjustable increments
        self.experience = tk.IntVar(value=1500)  # Initial value for experience

        experience_frame = ttk.Frame(status_frame, style="TFrame")
        experience_frame.pack(pady=10)

        experience_label = ttk.Label(experience_frame, text="Experience:", style="TLabel")
        experience_label.grid(row=0, column=0, padx=10, pady=5)

        # Buttons for adjusting experience
        button_texts = ["-1", "-10","-100","-1000","+1", "+10", "+100", "+1000"]
        increments = [-1,-10,-100, -1000, 1, 10, 100, 1000]

        for idx, text in enumerate(button_texts):
            button = ttk.Button(experience_frame, text=text, style="PlusMinus.TButton",
                                command=lambda incr=increments[idx]: self.adjust_experience(incr))
            button.grid(row=0, column=idx+1, padx=5, pady=5)

        # Label to display current experience
        self.experience_label = ttk.Label(experience_frame, textvariable=self.experience, style="TLabel")
        self.experience_label.grid(row=0, column=len(button_texts)+1, padx=10, pady=5)

    def adjust_experience(self, increment):
        new_value = self.experience.get() + increment
        self.experience.set(new_value)

    def create_special_sub_tab(self, notebook):
        special_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(special_frame, text="S.P.E.C.I.A.L.")

        # Example labels (replace with actual content)
        self.special_vars = {
            "Strength": tk.IntVar(value=5),
            "Perception": tk.IntVar(value=6),
            "Endurance": tk.IntVar(value=7),
            "Charisma": tk.IntVar(value=8),
            "Intelligence": tk.IntVar(value=6),
            "Agility": tk.IntVar(value=7),
            "Luck": tk.IntVar(value=5)
        }

        row = 0
        for stat, var in self.special_vars.items():
            label = ttk.Label(special_frame, text=f"{stat}:", style="TLabel")
            label.grid(row=row, column=0, padx=10, pady=5, sticky='w')

            minus_button = ttk.Button(special_frame, text="-", style="PlusMinus.TButton",
                                      command=lambda v=var: self.adjust_stat(v, -1))
            minus_button.grid(row=row, column=1, padx=5, pady=5)

            value_label = ttk.Label(special_frame, textvariable=var, style="TLabel")
            value_label.grid(row=row, column=2, padx=5, pady=5)

            plus_button = ttk.Button(special_frame, text="+", style="PlusMinus.TButton",
                                     command=lambda v=var: self.adjust_stat(v, 1))
            plus_button.grid(row=row, column=3, padx=5, pady=5)

            row += 1

    def adjust_stat(self, var, increment):
        new_value = var.get() + increment
        if 1 <= new_value <= 10:  # Ensure values stay within valid range (1-10)
            var.set(new_value)

    def create_skills_sub_tab(self, notebook):
        skills_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(skills_frame, text="Skills")

        # Example labels (replace with actual content)
        small_guns_label = ttk.Label(skills_frame, text="Small Guns: 80%", style="TLabel")
        small_guns_label.pack(pady=5, anchor='w')

        repair_label = ttk.Label(skills_frame, text="Repair: 60%", style="TLabel")
        repair_label.pack(pady=5, anchor='w')

        medicine_label = ttk.Label(skills_frame, text="Medicine: 70%", style="TLabel")
        medicine_label.pack(pady=5, anchor='w')

        sneak_label = ttk.Label(skills_frame, text="Sneak: 50%", style="TLabel")
        sneak_label.pack(pady=5, anchor='w')

        speech_label = ttk.Label(skills_frame, text="Speech: 90%", style="TLabel")
        speech_label.pack(pady=5, anchor='w')

    def create_perks_sub_tab(self, notebook):
        perks_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(perks_frame, text="Perks")

        # Example list of perks (replace with your actual perks data)
        self.perks = {
            "Perk 1": "Description of Perk 1.",
            "Perk 2": "Description of Perk 2.",
            "Perk 3": "Description of Perk 3.",
            "Perk 4": "Description of Perk 4."
        }

        # Perk selection listbox
        self.perk_listbox = tk.Listbox(perks_frame, selectmode=tk.SINGLE, font=self.font, bg="black", fg="lime")
        for perk in self.perks:
            self.perk_listbox.insert(tk.END, perk)
        self.perk_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.perk_listbox.bind("<<ListboxSelect>>", self.on_perk_selected)

        # Frame for perk description
        self.perk_description_frame = ttk.Frame(perks_frame, style="TFrame")
        self.perk_description_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_perk_selected(self, event):
        # Clear previous description
        for widget in self.perk_description_frame.winfo_children():
            widget.destroy()

        # Get selected perk
        selected_index = self.perk_listbox.curselection()
        if selected_index:
            selected_perk = self.perk_listbox.get(selected_index)
            description = self.perks[selected_perk]

            # Display description label
            description_label = ttk.Label(self.perk_description_frame, text=description, style="TLabel")
            description_label.pack(padx=10, pady=10, anchor='w')

    def create_general_sub_tab(self, notebook):
        general_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(general_frame, text="General")

        # Example labels (replace with actual content)
        level_label = ttk.Label(general_frame, text="Level: 15", style="TLabel")
        level_label.pack(pady=5, anchor='w')

        experience_label = ttk.Label(general_frame, text="Experience: 1500/2000", style="TLabel")
        experience_label.pack(pady=5, anchor='w')

        money_label = ttk.Label(general_frame, text="Caps: 500", style="TLabel")
        money_label.pack(pady=5, anchor='w')

    

if __name__ == "__main__":
    app = PipBoyApp()
    app.mainloop()
