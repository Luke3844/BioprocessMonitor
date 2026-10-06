# =======================================================================
# CLASSES
# Define custom classes in this file.
# =======================================================================
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.functions import calculate_average

class BioprocessMonitor:
    def __init__(self, filepath, ph_lims, temperature_lims):

        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)
        self.ph_lims = ph_lims
        self.temperature_lims = temperature_lims

    def extract_batch(self, batch_id):

        df = self.df
        batch_number_mask = df['batch_id'] == batch_id
        batch_numbered = df[batch_number_mask]
        return batch_numbered

    def optimal_ph_mask(self, df_batch):

        ph_vals = df_batch["pH"]
        ph_ok = (ph_vals >= self.ph_lims[0]) & (ph_vals <= self.ph_lims[1])
        return ph_ok

    def optimal_temperature_mask(self, df_batch):

        temp_vals = df_batch["temperature_C"]
        temp_ok = (temp_vals >= self.temperature_lims[0]) & (temp_vals <= self.temperature_lims[1])
        return temp_ok

    def get_n_batches(self):

        n_batches = self.df['batch_id'].nunique()
        return n_batches

    def export_dashboard(self, batch_id, filepath):
        batch = pd.read_csv(filepath)
        time = batch["time_h"]

        fig, axes = plt.subplots(2, 2, figsize=[12, 8])

        # Top-left: concentrations vs time

        ax = axes[0,0]
        ax.scatter(time, batch["C_product_g_L^-1"],
                   color="tab:blue", marker = "o", label="Product")
        ax.scatter(time, batch["C_glucose_g_L^-1"],
                   color="tab:red", marker = "s", label="Glucose")
        ax.scatter(time, batch["C_biomass_g_L^-1"],
                   color="tab:green", marker = "^", label="Biomass")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("Concentration (g/L)")
        ax.legend()
        ax.grid(alpha=0.0)

        # Top-right: temperature vs time
        ax = axes[0, 1]
        temp_ok = self.optimal_temperature_mask(batch)
        ax.scatter(time[temp_ok], batch.loc[temp_ok, "temperature_C"],
                   color="green", marker="o", label="Optimal")
        ax.scatter(time[~temp_ok], batch.loc[~temp_ok, "temperature_C"],
                   color="red", marker="x", label="Out of range")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature")
        ax.legend()
        ax.grid(alpha=0.3)

        # Bottom-left: pH vs time
        ax = axes[1, 0]
        ph_ok = self.optimal_ph_mask(batch)
        ax.scatter(time[ph_ok], batch.loc[ph_ok, "pH"],
                   color="green", marker="o", label="Optimal")
        ax.scatter(time[~ph_ok], batch.loc[~ph_ok, "pH"],
                   color="red", marker="x", label="Out of range")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("pH")
        ax.set_title("pH")
        ax.legend()
        ax.grid(alpha=0.3)

        # Bottom-right: dissolved oxygen vs time
        ax = axes[1, 1]
        ax.scatter(time, batch["dissolved_oxygen_percent"],
                   color="tab:cyan", marker="o", label="DO")
        ax.set_xlabel("Time (h)")
        ax.set_ylabel("Dissolved oxygen (%)")
        ax.set_title("Dissolved oxygen")
        ax.legend()
        ax.grid(alpha=0.3)

        # X-axis tick spacing
        for ax in axes.flat:
            ax.xaxis.set_major_locator(plt.MultipleLocator(6))

        fig.suptitle(f"Batch {batch_id} — Bioprocess Dashboard",
                     fontweight="bold")
        fig.tight_layout()

        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)


    def export_summary(self, filepath):


        summaries = []
        batch_ids = sorted(self.df['batch_id'].unique().tolist())

        for batch_id in batch_ids:
            batch = self.extract_batch(batch_id=batch_id)

            ph_ok = self.optimal_ph_mask(batch)
            temp_ok = self.optimal_temperature_mask(batch)

            ph_percentage = round(100*ph_ok.mean(), 2)
            temp_percentage = round(100*temp_ok.mean(), 2)
            final_product = batch["C_product_g_L^-1"].iloc[-1]

            summary = (batch_id, ph_percentage, temp_percentage, final_product)
            summaries.append(summary)

        print(summaries)

        column_names = ["batch_id", "ph_optimal_percent", "temperature_optimal_percent", "C_product_g_L^-1_final"]
        summary_table = pd.DataFrame(summaries, columns=column_names)

        summary_table_location = filepath
        summary_table.to_csv(summary_table_location, index=False)