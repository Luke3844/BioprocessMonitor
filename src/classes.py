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
        """
        Creates and saves a dashboard figure for a single batch.

        Parameters
        ----------
        batch_id : int
            Batch identifier.
        filepath : str
            Output PNG image path.

        Dashboard Requirements
        ----------------------
        Create a 2 × 2 figure containing:

        Top-Left
            Glucose, biomass, and product concentrations versus time.
            - A different color and marker should be used for each substance.

        Top-Right
            Temperature versus time.
            - Measurements within the acceptable temperature range
              should be displayed as green circles.
            - Measurements outside the acceptable temperature range
              should be displayed as red X markers.

        Bottom-Left
            pH versus time.
            - Measurements within the acceptable pH range
              should be displayed as green circles.
            - Measurements outside the acceptable pH range
              should be displayed as red X markers.

        Bottom-Right
            Dissolved oxygen versus time.

        Additional Requirements
        -----------------------
        - Use scatter plots.
        - Add x-axis and y-axis labels.
        - Add legends where appropriate.
        - Apply consistent formatting across all subplots unless
          indicated otherwise.
        - Apply a tick spacing of 6 h on the x-axis for all subplots.
        - Save the figure to the provided filepath.
        - Close the figure after saving.
        """

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