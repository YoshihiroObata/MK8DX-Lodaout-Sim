# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:00:29 2021

@author: Yoshihiro Obata
"""
# %% importing packages
import tkinter as tk
from tkinter import Tk, Frame, Button, LabelFrame, Label
from PIL import ImageTk, Image
import glob
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from app_utils import plot_stats, get_data, get_names, getDetailsPlot, get_groups, get_similar
from functools import partial

# %% GUI
class MK8DX_Sim(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        img = tk.Image('photo', file='icon.png')
        self.title('Mario Kart 8 Deluxe Loadout Simul8or')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self._frame = None
        
        global loadout
        loadout = 1
        global compare
        compare = 'no'
        global details
        details = 'no'
        
        self.dfs = get_data()
        self.chars, self.vehicles, self.tires, self.gliders = get_names(self.dfs)
        
        stats = list(self.dfs[0].columns[1:])
        global option_groups
        option_groups = get_groups(self.dfs, stats)
        
        self.switch_frame(CharSelect)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class CharSelect(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        # style = ThemedStyle()
        # style.set_theme('aquativo')
        
        self.char_imgs = glob.glob('char_icons/*.png')
        charButtons = []
        imgs = []
        
        prompt = LabelFrame(self, text='Select your character:', 
                padx=10, pady=10, font=('Arial', 20))
        # prompt = ttk.LabelFrame(self, text='Select your character:')
        prompt.grid(row=0, column=0, columnspan=8)
        
        for i, char in enumerate(self.char_imgs):
            imgs.append(ImageTk.PhotoImage(Image.open(char)))
            name = master.chars[i]
            button = Button(prompt, image=imgs[i], height=100, width=100,
                            command=partial(self.command, master, name, imgs[i]))
            button.image = imgs[i]
            charButtons.append(button)
        
        global all_char_imgs
        all_char_imgs = imgs

        i = 0
        for row in range(6):
            for col in range(7):
                name = master.chars[i]
                charButtons[i].grid(row=row+1, column=col) 
                i += 1  
                
    def command(self, master, name, img):
        if loadout == 1:
            global char1
            global char1img
            char1 = name
            char1img = img
        elif loadout == 2:
            global char2
            global char2img
            char2 = name
            char2img = img
        master.switch_frame(VehicleSelect)

class VehicleSelect(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.ve_imgs = glob.glob('vehicle_icons/*.png')
        veButtons = []
        imgs = []
        
        prompt = LabelFrame(self, text='Select your vehicle:', 
                padx=10, pady=10, font=('Arial', 20))
        prompt.grid(row=0, column=0, columnspan=8)
        
        for i, ve in enumerate(self.ve_imgs):
            imgs.append(ImageTk.PhotoImage(Image.open(ve)))
            name = master.vehicles[i]
            button = Button(prompt, image=imgs[i], height=100, width=100,
                            text=master.vehicles[i], compound='top',
                            command=partial(self.command, master, name, imgs[i]))
            button.image = imgs[i]
            veButtons.append(button)
        
        global all_vehicle_imgs
        all_vehicle_imgs = imgs
        
        i = 0
        for row in range(5):
            for col in range(9):
                if row == 4:
                    col += 3
                # try except for uneven bottom row
                try:
                    veButtons[i].grid(row=row+1, column=col) 
                    i += 1
                except:
                    continue
                
        backButton = Button(prompt, text='Back', height=2, width=6,
                            font=('Arial', 20),
                            command=lambda: self.goBack(master))
        backButton.grid(row=5, column=2)
                
    def command(self, master, name, img):
        if loadout == 1:
            global vehicle1
            global vehicle1img
            vehicle1 = name
            vehicle1img = img
        elif loadout == 2:
            global vehicle2
            global vehicle2img
            vehicle2 = name
            vehicle2img = img
        master.switch_frame(TireSelect)
    
    def goBack(self, master):
        master.switch_frame(CharSelect)

class TireSelect(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.tire_imgs = glob.glob('tire_icons/*.png')
        tireButtons = []
        imgs = []
        
        prompt = LabelFrame(self, text='Select your tires:', 
                padx=10, pady=10, font=('Arial', 20))
        prompt.grid(row=0, column=0, columnspan=8)
        
        for i, tire in enumerate(self.tire_imgs):
            imgs.append(ImageTk.PhotoImage(Image.open(tire)))
            name = master.tires[i]
            button = Button(prompt, image=imgs[i], height=100, width=100,
                            text=master.tires[i], compound='top',
                            command=partial(self.command, master, name, imgs[i]))
            button.image = imgs[i]
            tireButtons.append(button)

        global all_tire_imgs
        all_tire_imgs = imgs

        i = 0
        for row in range(4):
            for col in range(6):
                if row == 3:
                    col += 2
                try:
                    tireButtons[i].grid(row=row+1, column=col) 
                    i += 1
                except:
                    continue
                
        backButton = Button(prompt, text='Back', height=2, width=6,
                            font=('Arial', 20),
                            command=lambda: self.goBack(master))
        backButton.grid(row=4, column=1)
                
    def command(self, master, name, img):
        if loadout == 1:
            global tire1
            global tire1img
            tire1 = name
            tire1img = img
        elif loadout == 2:
            global tire2
            global tire2img
            tire2 = name
            tire2img = img
        master.switch_frame(GliderSelect)
        
    def goBack(self, master):
        master.switch_frame(VehicleSelect)
                
class GliderSelect(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.glider_imgs = glob.glob('glider_icons/*.png')
        gliderButtons = []
        imgs = []
        
        prompt = LabelFrame(self, text='Select your glider:', 
                padx=10, pady=10, font=('Arial', 20))
        prompt.grid(row=0, column=0, columnspan=8)
        
        for i, glider in enumerate(self.glider_imgs):
            imgs.append(ImageTk.PhotoImage(Image.open(glider)))
            name = master.gliders[i]
            button = Button(prompt, image=imgs[i], 
                            text=master.gliders[i], compound='top',
                            height=100, width=100,
                            command=partial(self.command, master, name, imgs[i]))
            button.image = imgs[i]
            gliderButtons.append(button)

        global all_glider_buttons
        all_glider_buttons = imgs

        i = 0
        for row in range(4):
            for col in range(5):
                if row == 2:
                    col += 1
                try:
                    gliderButtons[i].grid(row=row+1, column=col) 
                    i += 1
                except:
                    continue
        backButton = Button(prompt, text='Back', height=2, width=6,
                            font=('Arial', 20),
                            command=lambda: self.goBack(master))
        backButton.grid(row=3, column=0)
                
    def command(self, master, name, img):
        if loadout == 1:
            global glider1
            global glider1img
            glider1 = name
            glider1img = img
        elif loadout == 2:
            global glider2
            global glider2img
            glider2 = name
            glider2img = img
        master.switch_frame(StatScreen)
        
    def goBack(self, master):
        master.switch_frame(TireSelect)
        
class StatScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        if loadout == 1:
            combo = [char1, vehicle1, tire1, glider1]
            charimg = char1img
            vehicleimg = vehicle1img
            tireimg = tire1img
            gliderimg = glider1img
        elif loadout == 2:
            combo = [char2, vehicle2, tire2, glider2]
            charimg = char2img
            vehicleimg = vehicle2img
            tireimg = tire2img
            gliderimg = glider2img
        
        # box around the stuff
        prompt = LabelFrame(self, text='Loadout Stats', padx=10, pady=10, 
                            font=('Arial', 20))
        prompt.grid(row=0, column=0, columnspan=4)
        
        # getting the figures
        if details == 'no':
            fig = plot_stats(combo, master.dfs, loadout)
        elif details == 'yes':
            fig = getDetailsPlot(combo, master.dfs)
        plot1 = FigureCanvasTkAgg(fig, prompt)
        plot1.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=2)
        
        charButton = Button(prompt, text='Reselect Character',
                            font=('Arial', 15),
                            command=lambda: self.reSelect(master, 'char'))
        vehicleButton = Button(prompt, text='Reselect Vehicle',
                               font=('Arial', 15),
                               command=lambda: self.reSelect(master, 'vehicle'))
        tireButton = Button(prompt, text='Reselect Tire',
                            font=('Arial', 15),
                            command=lambda: self.reSelect(master, 'tire'))
        gliderButton = Button(prompt, text='Reselect Glider',
                              font=('Arial', 15),
                              command=lambda: self.reSelect(master, 'glider'))
        
        # reselect buttons
        charButton.grid(row=2, column=0)
        vehicleButton.grid(row=2, column=1)
        tireButton.grid(row=2, column=2)
        gliderButton.grid(row=2, column=3)
        
        charLabel = Label(prompt, image=charimg)
        charLabel.image = charimg
        vehicleLabel = Label(prompt, image=vehicleimg)
        vehicleLabel.image = vehicleimg
        tireLabel = Label(prompt, image=tireimg)
        tireLabel.image = tireimg
        gliderLabel = Label(prompt, image=gliderimg)
        gliderLabel.image = gliderimg
        
        charLabel.grid(row=3, column=0)
        vehicleLabel.grid(row=3, column=1)
        tireLabel.grid(row=3, column=2)
        gliderLabel.grid(row=3, column=3)
        
        # more options button
        if compare == 'no':
            compareButton = Button(prompt, text='Compare\nLoadouts',
                                   font=('Arial', 15),
                                   command=lambda: self.newCompare(master, fig))
            compareButton.grid(row=0, column=4)
        elif compare == 'yes':
            swapButton = Button(prompt, text='Swap\nLoadouts',
                                font=('Arial', 15),
                                command=lambda: self.swapLoadout(master, fig))
            swapButton.grid(row=0, column=4)
        
        detailsButton = Button(prompt, text='Toggle\nDetails',
                               font=('Arial', 15),
                               command=lambda: self.loadoutDetails(master, fig))  
        detailsButton.grid(row=1, column=4)
        
        if details == 'yes':
            similar = get_similar(option_groups, combo)
            # getting images for similar things
            all_names = [master.chars, master.vehicles, master.tires, master.gliders]
            all_imgs = [all_char_imgs, all_vehicle_imgs, all_tire_imgs, all_glider_buttons]
            imgs = []
            for i, option in enumerate(similar):
                names = all_names[i]
                idx = []
                for j, name in enumerate(option):
                    idx += [k for k in range(len(names)) if name == names[k]]
                imgs.append([all_imgs[i][l] for l in idx])
            
            similar_window = LabelFrame(self, text='Similar Loadouts', padx=10, pady=10, 
                            font=('Arial', 20))
            similar_window.grid(row=0, column=4)
            
            labels = []
            for option in range(len(similar)):
                for i, choice in enumerate(similar[option]):
                    try:
                        similarLabel = Label(similar_window, image=imgs[option][i])
                        similarLabel.image = imgs[option][i]
                        labels.append(similarLabel)
                    except:
                        labels.append(Label(similar_window, text='', 
                                            font=('Arial', 20)))
            
            i = 0
            similar_rows = ['Character', 'Vehcile', 'Tire', 'Glider']
            for row in range(len(similar)):
                rowLabel = Label(similar_window, text=similar_rows[row], 
                                 font=('Arial', 15))
                rowLabel.grid(row=row*2+1, column=0)
                for col in range(len(similar[row])):
                    labels[i].grid(row=(row+1)*2, column=col)
                    i += 1
        
    def reSelect(self, master, where):
        if where == 'char':
            master.switch_frame(CharSelect)
        elif where == 'vehicle':
            master.switch_frame(VehicleSelect)
        elif where == 'tire':
            master.switch_frame(TireSelect)
        elif where == 'glider':
            master.switch_frame(GliderSelect)
        else:
            print('Error')
            
    def newCompare(self, master, fig):
        global loadout
        loadout = 2
        global compare
        compare = 'yes'
        plt.close(fig)
        master.switch_frame(CharSelect)
        
    def swapLoadout(self, master, fig):
        global loadout
        if loadout == 1:  
            loadout = 2
        elif loadout == 2:
            loadout = 1
        plt.close(fig)
        master.switch_frame(StatScreen)
        
    def loadoutDetails(self, master, fig):
        plt.close(fig)
        global details
        if details == 'no':
            details = 'yes'
        elif details == 'yes':
            details = 'no'
        master.switch_frame(StatScreen)
        
if __name__ == "__main__":
    app = MK8DX_Sim()
    app.mainloop()
