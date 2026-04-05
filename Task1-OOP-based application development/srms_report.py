import tkinter as tk
from tkinter import ttk
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def build_month_graph(parent: tk.Frame, months: list, amounts: list):
    """graph view """
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(9, 4), dpi=100)
    fig.patch.set_facecolor("#f9f9f9")


    if not months:
        ax.text(0.5, 0.5, "No paid invoices yet.",
                ha="center", va="center", fontsize=13, color="grey")
        ax.axis("off")
        
    else:
        # line
        ax.plot(months, amounts,
                color="#009821", linewidth=2.2,
                marker="o", markersize=7,
                markerfacecolor="white", markeredgewidth=2)

        # marker label
        for m, a in zip(months, amounts):
            ax.annotate(f"${a:,.0f}",
                        xy=(m, a), xytext=(0, 10),
                        textcoords="offset points",
                        ha="center", fontsize=8.5, color="#074a00")

        #x-axis and y-axis formatting
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.set_xlabel("Month", fontsize=10)
        ax.set_ylabel("Amount (HKD)", fontsize=10)

        ax.set_title("Monthly Payment Received", fontsize=13, fontweight="bold", pad=12)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.set_facecolor("#ffffff")

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)  
    plt.close(fig)