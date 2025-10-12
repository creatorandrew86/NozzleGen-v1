
################################################################################
# NozzleGen — Compiler
# --------------------
# Copyright (C) 2025 Your Name <you@example.com>
# Licensed under GPL-3.0-or-later
# See LICENSE file for full terms
#
# Description:
#   This file is the driver program of NozzleGen. It handles user input,
#   calls the nozzle generation routines, and exports the nozzle contour
#   data to a file. It also plots the nozzle contour.
#
# Requirements:
#   - Python 3.10 or higher
#   - Tkinter (usually comes with Python standard library)
#   - Matplotlib (for plotting nozzle contours)
#   - Pip (to install Matplotlib if not present: `pip install matplotlib`)
#
#
# Usage:
#   Run directly (Python) or "python complier.py".
#
# Notes:
#   - Ensure the LICENSE file is present in the repository root.
#   - This program is free software: you can redistribute and/or modify it
#     under the terms of the GNU General Public License version 3 or later.
#   - This program is distributed WITHOUT ANY WARRANTY; see LICENSE for details.
#
# Author: Andrew Toma
# Date:   2025-10-06
################################################################################


import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
import ModuleNozzleGenerator


def bellNozzle():
    # Untick the conical nozzle checkbutton
    conical_var.set(0)

    # Enable bell labels & entries
    for label in bell_frame_labels:
        label.config(state="normal")

    for entry in bell_frame_entries:
        entry.config(state="normal")


    # Disable conical labels & entries
    for label in conical_frame_labels:
        label.config(state="disabled")

    for entry in conical_frame_entries:
        entry.config(state="disabled")


    # Disable bell entries & labels (if it's the case)
    if not bell_var.get():
        for label in bell_frame_labels:
            label.config(state="disabled")

        for entry in bell_frame_entries:
            entry.config(state="disabled")


    


def conicalNozzle():
    # Untick the bell nozzle checkbutton
    bell_var.set(0)

    # Enable conical labels & entries
    for label in conical_frame_labels:
        label.config(state="normal")

    for entry in conical_frame_entries:
        entry.config(state="normal")


    # Disable bell labels & entries
    for label in bell_frame_labels:
        label.config(state="disabled")

    for entry in bell_frame_entries:
        entry.config(state="disabled")


    # Disable conical labels & entries (if it's the case)
    if not conical_var.get():
        for label in conical_frame_labels:
            label.config(state="disabled")

        for entry in conical_frame_entries:
            entry.config(state="disabled")





# Main function
def compile():
    # Define global lists
    global xList, yList, N

    # Enable export functions
    button2.config(state="normal")
    button3.config(state="normal")

    # Bell nozzle selection
    if bell_var.get():
        # Required entries
        Rt = float(Rt_entry.get())
        N = int(N_entry.get())
        eps = float(eps_entry.get())
        length_percentage = float(length_percentage_entry.get())
        r3 = float(r3_entry.get())


        # Handle optional entries
        if Cr_entry.get():
            Cr = float(Cr_entry.get())
        else:
            Cr = 0


        if Lstar_entry.get():
            Lstar = float(Lstar_entry.get())
        else:
            Lstar = 0


        if Cr_entry.get():
            Cr = float(Cr_entry.get())
        else:
            Cr = 0

        
        if r1_entry.get():
            r1 = float(r1_entry.get())
        else:
            r1 = 0

        
        if r2_entry.get():
            r2 = float(r2_entry.get())
        else:
            r2 = 0


        if thetae_entry.get():
            thetae = float(thetae_entry.get())
        else:
            thetae = -1


        # Check entries
        if (length_percentage < 55):
            print("Nozzle length cannot be smaller than 55% of conical nozzle length!")
            return

        # Run the main function
        start = time.perf_counter()
        xList, yList = ModuleNozzleGenerator.bellNozzleGenerator(Rt, N, eps, Cr, Lstar, r1, r2, r3, length_percentage, thetae)
        end = time.perf_counter()

        # Time the execution of the generator
        print(f"Execution Time: {end - start}")

    # Conical nozzle selection
    elif conical_var.get():
        # Required entries
        Rt = float(Rt_entry.get())
        N = int(N_entry.get())
        eps = float(eps_entry.get())
        theta_max = float(theta_entry.get())
        r3 = float(r3_entry.get())


        # Handle optional entries
        if Cr_entry.get():
            Cr = float(Cr_entry.get())
        else:
            Cr = 0


        if Lstar_entry.get():
            Lstar = float(Lstar_entry.get())
        else:
            Lstar = 0


        if Cr_entry.get():
            Cr = float(Cr_entry.get())
        else:
            Cr = 0

        
        if r1_entry.get():
            r1 = float(r1_entry.get())
        else:
            r1 = 0

        
        if r2_entry.get():
            r2 = float(r2_entry.get())
        else:
            r2 = 0


        # Run the function
        start = time.perf_counter()
        xList, yList = ModuleNozzleGenerator.conicalNozzleGenerator(Rt, N, eps, Cr, Lstar, r1, r2, r3, theta_max)
        end = time.perf_counter()

        # Time the execution of the generator
        print(f"Execution Time: {end - start}")

    # No nozzle selection case 
    else:
        print("Select at least one nozzle option!")

        button2.config(state="disabled")
        button3.config(state="disabled")

        return

    plot_nozzle()


def plot_nozzle():
    plt.plot(xList, yList, linestyle='-', color='black', label='Nozzle Contour')
    plt.title('Nozzle Contour')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')
    
    plt.show()


# Export .dat function
def export_dat():
    # Check if the main function ran
    if (xList == []):
        print("Generate the nozzle contour before exporting!")
        return
    
    filename = filedialog.asksaveasfilename(
        title="Save Nozzle Contour Data",
        defaultextension=".dat",
        filetypes=[("Data files", "*.dat"), ("All files", "*.*")]
    )

    if not filename:
        print("Select a file name!")
        return

    # Write data to the chosen file
    with open(filename, "w") as f:
        for i in range(N):
            f.write(f"{xList[i]} {yList[i]}\n")


# Export .dxf function
def export_dxf():
    import ezdxf

    # Check if the main function ran
    if (xList == []):
        print("Generate the nozzle contour before exporting!")
        return
    

    filename = filedialog.asksaveasfilename(
        defaultextension=".dxf",
        filetypes=[("DXF files", "*.dxf")],
        title="Save DXF file as..."
    )

    if not filename:
        print("Select a file name!")
        return

    # Create the DXF doc
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()

    # Combine points into tuples
    points = [(float(x), float(y)) for x, y in zip(xList, yList)]

    msp.add_lwpolyline(points, dxfattribs={"layer": "Geometry"})

    # Save file
    doc.saveas(filename)

# *************************************************************************************************************************************************
#                                                                     INTERFACE
# *************************************************************************************************************************************************


# Create the main interface
root = tk.Tk()
root.geometry("910x565")
root.title("NozzleGen v1")


# Interface Header
ttk.Label(root, text="Select Nozzle Type:").grid(row=0, column=0, padx=5, pady=3, sticky='W')

# Bell and Conical nozzle variables
bell_var = tk.IntVar(value=0)
conical_var = tk.IntVar(value=0)




# Main frame | Frames generation
main_frame = tk.Frame(root)
main_frame.grid(row=1, column=0, padx=7, pady=5)


# Bell nozzle checkbutton
bell_checkbutton = ttk.Checkbutton(main_frame, text="Bell Nozzle", variable=bell_var, command=bellNozzle)
bell_checkbutton.grid(row=0, column=0, padx=5, pady=5, sticky='W')

# Bell frame
bell_frame = tk.Frame(main_frame, borderwidth=0.5, relief="raised")
bell_frame.grid(row=1, column=0, padx=13, pady=0)


# Conical nozzle checkbutton
conical_checkbutton = ttk.Checkbutton(main_frame, text="Conical Nozzle", variable=conical_var, command=conicalNozzle)
conical_checkbutton.grid(row=0, column=1, padx=5, pady=5, sticky='W')

# Conical frame
conical_frame = tk.Frame(main_frame, borderwidth=0.5, relief="raised")
conical_frame.grid(row=1, column=1, padx=13, pady=0)




# Entries and Labels lists
bell_frame_labels, bell_frame_entries = [], []
conical_frame_labels, conical_frame_entries = [], []


# Entries/Labels are named entry/label for bell nozzle and entry2/label2 for conical nozzle respectively




# **************************************************************************************************************************************************
# Bell Nozzle
# **************************************************************************************************************************************************



# Throat Radius
Rt_label = ttk.Label(bell_frame, text="Rt (cm): *")
Rt_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')
Rt_label.config(state="disabled")
bell_frame_labels.append(Rt_label)

Rt_entry = ttk.Entry(bell_frame, width=10)
Rt_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')
Rt_entry.config(state="disabled")
bell_frame_entries.append(Rt_entry)


# Number of points
N_label = ttk.Label(bell_frame, text="Analysis Points: *")
N_label.grid(row=1, column=0, padx=5, pady=5, sticky='W')
N_label.config(state="disabled")
bell_frame_labels.append(N_label)

N_entry = ttk.Entry(bell_frame, width = 10)
N_entry.insert(0, "150")
N_entry.grid(row=1, column=1, padx=5, pady=5, sticky='W')
N_entry.config(state="disabled")
bell_frame_entries.append(N_entry)


# Area ratio
eps_label = ttk.Label(bell_frame, text="Area Ratio: *")
eps_label.grid(row=2, column=0, padx=5, pady=5, sticky='W')
eps_label.config(state="disabled")
bell_frame_labels.append(eps_label)

eps_entry = ttk.Entry(bell_frame, width = 10)
eps_entry.grid(row=2, column=1, padx=5, pady=5, sticky='W')
eps_entry.config(state="disabled")
bell_frame_entries.append(eps_entry)


# Length percentage
length_percentage_label = ttk.Label(bell_frame, text="Length %: *")
length_percentage_label.grid(row=3, column=0, padx=5, pady=5, sticky='W')
length_percentage_label.config(state="disabled")
bell_frame_labels.append(length_percentage_label)

length_percentage_entry = ttk.Entry(bell_frame, width = 10)
length_percentage_entry.insert(0, "80")
length_percentage_entry.grid(row=3, column=1, padx=5, pady=5, sticky='W')
length_percentage_entry.config(state="disabled")
bell_frame_entries.append(length_percentage_entry)


# Contraction ratio
Cr_label = ttk.Label(bell_frame, text="Contraction Ratio:")
Cr_label.grid(row=4, column=0, padx=5, pady=5, sticky='W')
Cr_label.config(state="disabled")
bell_frame_labels.append(Cr_label)

Cr_entry = ttk.Entry(bell_frame, width = 10)
Cr_entry.grid(row=4, column=1, padx=5, pady=5, sticky='W')
Cr_entry.config(state="disabled")
bell_frame_entries.append(Cr_entry)


# Characteristic length entry
Lstar_label = ttk.Label(bell_frame, text="Characteristic Length (cm):")
Lstar_label.grid(row=0, column=2, padx=5, pady=5, sticky='W')
Lstar_label.config(state="disabled")
bell_frame_labels.append(Lstar_label)

Lstar_entry = ttk.Entry(bell_frame, width = 10)
Lstar_entry.grid(row=0, column=3, padx=5, pady=5, sticky='W')
Lstar_entry.config(state="disabled")
bell_frame_entries.append(Lstar_entry)


# R1/Rt entry
r1_label = ttk.Label(bell_frame, text="R1/Rt:")
r1_label.grid(row=1, column=2, padx=5, pady=5, sticky='W')
r1_label.config(state="disabled")
bell_frame_labels.append(r1_label)

r1_entry = ttk.Entry(bell_frame, width=10)
r1_entry.insert(0, "0.7")
r1_entry.grid(row=1, column=3, padx=5, pady=5, sticky='W')
r1_entry.config(state="disabled")
bell_frame_entries.append(r1_entry)


# R2/Rt entry
r2_label = ttk.Label(bell_frame, text="R2/Rt:")
r2_label.grid(row=2, column=2, padx=5, pady=5, sticky='W')
r2_label.config(state="disabled")
bell_frame_labels.append(r2_label)

r2_entry = ttk.Entry(bell_frame, width=10)
r2_entry.insert(0, "1.5")
r2_entry.grid(row=2, column=3, padx=5, pady=5, sticky='W')
r2_entry.config(state="disabled")
bell_frame_entries.append(r2_entry)


# R3/Rt entry
r3_label = ttk.Label(bell_frame, text="R3/Rt: *")
r3_label.grid(row=3, column=2, padx=5, pady=5, sticky='W')
r3_label.config(state="disabled")
bell_frame_labels.append(r3_label)

r3_entry = ttk.Entry(bell_frame, width=10)
r3_entry.insert(0, "0.382")
r3_entry.grid(row=3, column=3, padx=5, pady=5, sticky='W')
r3_entry.config(state="disabled")
bell_frame_entries.append(r3_entry)


# Exit angle (thetae)
thetae_label = ttk.Label(bell_frame, text="Exit Angle:")
thetae_label.grid(row=4, column=2, padx=5, pady=5, sticky='W')
thetae_label.config(state="disabled")
bell_frame_labels.append(thetae_label)

thetae_entry = ttk.Entry(bell_frame, width=10)
thetae_entry.grid(row=4, column=3, padx=5, pady=5, sticky='W')
thetae_entry.config(state="disabled")
bell_frame_entries.append(thetae_entry)




# **************************************************************************************************************************************************
# Conical Nozzle
# **************************************************************************************************************************************************




# Throat Radius
Rt_label2 = ttk.Label(conical_frame, text="Rt (cm): *")
Rt_label2.grid(row=0, column=0, padx=5, pady=5, sticky='W')
Rt_label2.config(state="disabled")
conical_frame_labels.append(Rt_label2)

Rt_entry2 = ttk.Entry(conical_frame, width=10)
Rt_entry2.grid(row=0, column=1, padx=5, pady=5, sticky='W')
Rt_entry2.config(state="disabled")
conical_frame_entries.append(Rt_entry2)

# Number of points
N_label2 = ttk.Label(conical_frame, text="Analysis Points: *")
N_label2.grid(row=1, column=0, padx=5, pady=5, sticky='W')
N_label2.config(state="disabled")
conical_frame_labels.append(N_label2)

N_entry2 = ttk.Entry(conical_frame, width=10)
N_entry2.insert(0, "150")
N_entry2.grid(row=1, column=1, padx=5, pady=5, sticky='W')
N_entry2.config(state="disabled")
conical_frame_entries.append(N_entry2)

# Area ratio
eps_label2 = ttk.Label(conical_frame, text="Area Ratio: *")
eps_label2.grid(row=2, column=0, padx=5, pady=5, sticky='W')
eps_label2.config(state="disabled")
conical_frame_labels.append(eps_label2)

eps_entry2 = ttk.Entry(conical_frame, width=10)
eps_entry2.grid(row=2, column=1, padx=5, pady=5, sticky='W')
eps_entry2.config(state="disabled")
conical_frame_entries.append(eps_entry2)

# Nozzle angle "theta"
theta_label = ttk.Label(conical_frame, text="Nozzle Angle: *")
theta_label.grid(row=3, column=0, padx=5, pady=5, sticky='W')
theta_label.config(state="disabled")
conical_frame_labels.append(theta_label)

theta_entry = ttk.Entry(conical_frame, width=10)
theta_entry.insert(0, "15")
theta_entry.grid(row=3, column=1, padx=5, pady=5, sticky='W')
theta_entry.config(state="disabled")
conical_frame_entries.append(theta_entry)

# Contraction ratio
Cr_label2 = ttk.Label(conical_frame, text="Contraction Ratio:")
Cr_label2.grid(row=4, column=0, padx=5, pady=5, sticky='W')
Cr_label2.config(state="disabled")
conical_frame_labels.append(Cr_label2)

Cr_entry2 = ttk.Entry(conical_frame, width=10)
Cr_entry2.grid(row=4, column=1, padx=5, pady=5, sticky='W')
Cr_entry2.config(state="disabled")
conical_frame_entries.append(Cr_entry2)

# Characteristic length entry
Lstar_label2 = ttk.Label(conical_frame, text="Characteristic Length (cm):")
Lstar_label2.grid(row=0, column=2, padx=5, pady=5, sticky='W')
Lstar_label2.config(state="disabled")
conical_frame_labels.append(Lstar_label2)

Lstar_entry2 = ttk.Entry(conical_frame, width=10)
Lstar_entry2.grid(row=0, column=3, padx=5, pady=5, sticky='W')
Lstar_entry2.config(state="disabled")
conical_frame_entries.append(Lstar_entry2)


# R1/Rt entry
r1_label2 = ttk.Label(conical_frame, text="R1/Rt:")
r1_label2.grid(row=1, column=2, padx=5, pady=5, sticky='W')
r1_label2.config(state="disabled")
conical_frame_labels.append(r1_label2)

r1_entry2 = ttk.Entry(conical_frame, width=10)
r1_entry2.insert(0, "0.7")
r1_entry2.grid(row=1, column=3, padx=5, pady=5, sticky='W')
r1_entry2.config(state="disabled")
conical_frame_entries.append(r1_entry2)


# R2/Rt entry
r2_label2 = ttk.Label(conical_frame, text="R2/Rt:")
r2_label2.grid(row=2, column=2, padx=5, pady=5, sticky='W')
r2_label2.config(state="disabled")
conical_frame_labels.append(r2_label2)

r2_entry2 = ttk.Entry(conical_frame, width=10)
r2_entry2.insert(0, "1.5")
r2_entry2.grid(row=2, column=3, padx=5, pady=5, sticky='W')
r2_entry2.config(state="disabled")
conical_frame_entries.append(r2_entry2)


# R3/Rt entry
r3_label2 = ttk.Label(conical_frame, text="R3/Rt: *")
r3_label2.grid(row=3, column=2, padx=5, pady=5, sticky='W')
r3_label2.config(state="disabled")
conical_frame_labels.append(r3_label2)

r3_entry2 = ttk.Entry(conical_frame, width=10)
r3_entry2.insert(0, "0.382")
r3_entry2.grid(row=3, column=3, padx=5, pady=5, sticky='W')
r3_entry2.config(state="disabled")
conical_frame_entries.append(r3_entry2)


# Frame generation for the buttons - bottom of the panel
buttons_frame = ttk.Frame(root)
buttons_frame.grid(row=2, column=0, padx=312, pady=10, sticky='W')


# Run the main function
button1 = ttk.Button(buttons_frame, text='Run', command=compile)
button1.grid(row=0, column=0, padx=10, pady=10, sticky='W')

# Run the ".dat" file write function
button2 = ttk.Button(buttons_frame, text="Export .dat", command=export_dat)
button2.grid(row=0, column=1, padx=10, pady=10, sticky='W')

# Run the ".dxf" file write function
button3 = ttk.Button(buttons_frame, text="Export .dxf", command=export_dxf)
button3.grid(row=0, column=2, padx=10, pady=10, sticky='W')


# Disable the export buttons if the main function did not run
button2.config(state="disabled")
button3.config(state="disabled")


# Warning labels
ttk.Label(root, text="Note: * indicates mandatory field").grid(row=3, column=0, padx=10, pady=2, sticky='W')
ttk.Label(root, text="Default values are given for some of the entries. The curvature radii (R1, R2, R3) as well as the exit angle (θₑ) are represented in the images below (Not to scale!)").grid(
    row=4, column=0, padx=10, pady=2, sticky='W'
)


# Images

# Frame for both images
img_frame =tk.Frame(root)
img_frame.grid(row=5, column=0, padx=10, pady=10, sticky='W')

# Load and show image 1
image1_path = "Image1.png"  
image1 = Image.open(image1_path)
image1 = image1.resize((420, 200))
photo1 = ImageTk.PhotoImage(image1)

# Frame for image 1
img1_frame = tk.Frame(img_frame, borderwidth=1, relief="solid")
img1_frame.grid(row=5, column=0, padx=10, pady=5, sticky='W')

img_label1 = ttk.Label(img1_frame, image=photo1)
img_label1.image = photo1
img_label1.grid(row=0, column=0)


# Load and show image 2
image2_path = "Image2.png"  
image2 = Image.open(image2_path)
image2 = image2.resize((420, 200))
photo2 = ImageTk.PhotoImage(image2)

# Frame for image 1
img2_frame = tk.Frame(img_frame, borderwidth=1, relief="solid")
img2_frame.grid(row=5, column=1, padx=10, pady=5, sticky='W')

img_label2 = ttk.Label(img2_frame, image=photo2)
img_label2.image = photo2  
img_label2.grid(row=0, column=0)



# Run the interface
root.mainloop()