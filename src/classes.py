# =======================================================================
# CLASSES
# Define custom classes in this file.
# =======================================================================
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class BioprocessMonitor:
    def __init__(self, filepath, ph_lims, temperature_lims):
        """
        Utility class used to monitor bioprocesses by
        generating dashboards and summaries.

        Parameters
        ----------
        filepath : str
            Input CSV dataset path.
        ph_lims : tuple[float, float]
            Lower and upper acceptable pH limits.
        temperature_lims : tuple[float, float]
            Lower and upper acceptable temperature limits.
        """
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)
        self.ph_lims = ph_lims
        self.temperature_lims = temperature_lims

    def extract_batch(self, batch_id):
        """
        Extracts data corresponding to a single batch.

        Parameters
        ----------
        batch_id : int
            Batch identifier.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing only rows associated with
            the requested batch.
        """
        df = pd.read_csv(self.filepath)
        batch_number = df.loc[batch_id, :]
        return batch_number

    def optimal_ph_mask(self, df_batch):
        """
        Determines whether each pH measurement falls within
        the acceptable operating range.

        Parameters
        ----------
        df_batch : pandas.DataFrame
            Batch-specific DataFrame.

        Returns
        -------
        array-like of bool
            A mask whereby True indicates that the measurement
            is within the acceptable operating range.
        """
        ph_vals = df_batch.loc[:, "ph"]
        ph_vals_acidic = ph_vals < self.ph_lims[0]
        ph_vals_basic = ph_vals > self.ph_lims[1]
        ph_vals_suboptimal = ph_vals_basic + ph_vals_acidic
        ph_ok = ~ph_vals_suboptimal
        return ph_ok

    def optimal_temperature_mask(self, df_batch):
        """
        Determines whether each temperature measurement falls
        within the acceptable operating range.

        Parameters
        ----------
        df_batch : pandas.DataFrame
            Batch-specific DataFrame.

        Returns
        -------
        array-like of bool
            A mask whereby True indicates that the measurement
            is within the acceptable operating range.
        """
        temp_vals = df_batch.loc[:, "temperature_C"]
        temp_vals_low = temp_vals < self.temperature_lims[0]
        temp_vals_high = temp_vals > self.temperature_lims[1]
        temp_vals_suboptimal = temp_vals_low + temp_vals_high
        temp_ok = ~temp_vals_suboptimal
        return temp_ok

    def get_n_batches(self):
        """
        Determines the number of unique batches present
        in the dataset.

        Returns
        -------
        int
            Total number of distinct batch identifiers.
        """
        "Returns the number of batches in the dataset"
        get_n_batches = self.df['batch_id'].nunique()
        print(get_n_batches)

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
        """
        Generates a batch summary table and exports it to a CSV file.

        Parameters
        ----------
        filepath : str
            Output CSV table path.

        Summary Table Columns
        ---------------------
        batch_id
            Batch identifier.

        ph_optimal_percent
            Percentage of measurements in a batch within the
            acceptable pH range, rounded to 2 decimal places.

        temperature_optimal_percent
            Percentage of measurements in a batch within the
            acceptable temperature range, rounded to 2 decimal places.

        C_product_g_L^-1_final
            Final product concentration for the batch.
        """

        column_names = ["batch_id", "ph_optimal_percent", "temperature_optimal_percent", "C_product_g_L^-1_final"]
        filepath_export = pd.DataFrame(record, columns=column_names)
        filepath_export_location = os.path.join("tables", "summary.csv")
        filepath_export.to_csv(filepath_export_location, index=False)