import math as m
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


def plot_yield_curve(user_maturity, selected_line):
    maturities = [2, 5, 10, 20, 30]
    yields = [0.0376, 0.0384, 0.0430, 0.0483, 0.0484]

    aa_maturities = [2, 5, 10, 20, 30]
    aa_yields = [0.0419, 0.0429, 0.0475, 0.0528, 0.0529]

    a_maturities = [2, 5, 10, 20, 30]
    a_yields = [0.0430, 0.0451, 0.0522, 0.0591, 0.0604]

    bbb_maturities = [2, 5, 10, 20, 30]
    bbb_yields = [0.0453, 0.0485, 0.0571, 0.0667, 0.0689]

    user_maturity = float(user_maturity)

    if user_maturity in maturities:
        index = maturities.index(user_maturity)
        user_yield = yields[index]
    else:
        user_yield = np.interp(user_maturity, maturities, yields)

    if selected_line == "AA":
        if user_maturity in aa_maturities:
            index = aa_maturities.index(user_maturity)
            selected_yield = aa_yields[index]
        else:
            selected_yield = np.interp(user_maturity, aa_maturities, aa_yields)
    elif selected_line == "A":
        if user_maturity in a_maturities:
            index = a_maturities.index(user_maturity)
            selected_yield = a_yields[index]
        else:
            selected_yield = np.interp(user_maturity, a_maturities, a_yields)
    elif selected_line == "BBB":
        if user_maturity in bbb_maturities:
            index = bbb_maturities.index(user_maturity)
            selected_yield = bbb_yields[index]
        else:
            selected_yield = np.interp(user_maturity, bbb_maturities, bbb_yields)

    # Calc the spread
    spread = (selected_yield - user_yield) * 10000

    today_date = datetime.now().strftime("%m/%d/%Y")

    # Plot original curve
    plt.figure(figsize=(10, 6))
    plt.plot(
        maturities,
        [y * 100 for y in yields],
        marker="o",
        label="US Treasury",
        color="blue",
    )

    # plot the selected curve
    if selected_line == "AA":
        plt.plot(
            aa_maturities,
            [y * 100 for y in aa_yields],
            marker="o",
            label="AA Corporate",
            color="orange",
        )
    elif selected_line == "A":
        plt.plot(
            a_maturities,
            [y * 100 for y in a_yields],
            marker="o",
            label="A Corporate",
            color="green",
        )
    elif selected_line == "BBB":
        plt.plot(
            bbb_maturities,
            [y * 100 for y in bbb_yields],
            marker="o",
            label="BBB Corporate",
            color="red",
        )

    # Plot the input point

    plt.scatter(
        user_maturity,
        user_yield * 100,
        color="black",
        zorder=5,
        label=f"Input ({selected_line})",
    )
    plt.annotate(
        f"{user_yield*100:.2f}%",
        (user_maturity, user_yield * 100),
        textcoords="offset points",
        xytext=(40, 0),
        ha="center",
        color="green",
    )

    # Marker for selected yield curve at user input
    plt.scatter(
        user_maturity,
        selected_yield * 100,
        color="purple",
        zorder=5,
        label=f"{selected_line} Yield",
    )
    plt.annotate(
        f"{selected_yield*100:.2f}%",
        (user_maturity, selected_yield * 100),
        textcoords="offset points",
        xytext=(40, 0),
        ha="center",
        color="purple",
    )

    # Dotted line between the two points
    plt.plot(
        [user_maturity, user_maturity],
        [user_yield * 100, selected_yield * 100],
        color="gray",
        linestyle="--",
        linewidth=1,
        label="Spread Line",
    )

    # Annotation for the spread
    plt.annotate(
        f"Spread: {spread:.2f} bps",
        (user_maturity, (user_yield + selected_yield) * 50),
        textcoords="offset points",
        xytext=(75, 0),
        ha="center",
        color="black",
        fontsize=10,
        fontweight="bold",
    )

    # Customize the plot
    plt.title(f"Yield Curve Comparison ({today_date})")
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield (%)")
    plt.legend()
    plt.show()


def on_submit():
    user_maturity = entry.get()
    selected_line = dropdown_var.get()
    try:
        plot_yield_curve(user_maturity, selected_line)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for maturity.")


# Create the main window
root = tk.Tk()
root.title("Yield Curve Interpolator")
root.geometry("400x300")

dropdown_var = tk.StringVar(root)
dropdown_var.set("AA")  # default value
dropdown_menu = tk.OptionMenu(root, dropdown_var, "AA", "A", "BBB")
dropdown_menu.config(width=10, font=("Arial", 14))
dropdown_menu.pack(pady=20)

# Create Label and Entry
label = tk.Label(root, text="Enter Maturity (Years):", font=("Arial", 14))
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

# Submit Button
submit_button = tk.Button(
    root, text="Plot Yield Curve", command=on_submit, font=("Arial", 14)
)
submit_button.pack(pady=20)

# Run the application
root.mainloop()
