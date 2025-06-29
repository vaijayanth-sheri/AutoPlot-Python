import sys
import pandas as pd
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QComboBox, QLabel, QFileDialog, QTextEdit, QStackedWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# --- Matplotlib Imports ---
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- Seaborn is used for better styling and more plot types ---
import seaborn as sns

# --- Plotly Imports ---
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.express as px
import plotly.io as pio


# --- Main Application Window ---
class PlotGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # --- Data Storage ---
        self.df = None
        self.figure = None
        self.plotly_fig = None
        self.current_plot_library = None

        # --- Initialize UI ---
        self.initUI()

    def initUI(self):
        # --- Window Properties ---
        self.setWindowTitle('Plot Generator')
        self.setGeometry(100, 100, 800, 700)

        # --- Layouts ---
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # --- UI Widgets ---

        # 1. File Upload
        self.upload_button = QPushButton("Upload Data File")
        self.upload_button.clicked.connect(self.upload_file)
        self.file_label = QLabel("No file selected.")

        # 2. Library Selection
        self.library_combo = QComboBox()
        self.library_combo.addItems(["matplotlib", "seaborn", "plotly"])
        self.library_combo.currentIndexChanged.connect(self.update_plot_types)

        # 3. Plot Type Selection
        self.plot_type_combo = QComboBox()

        # 4. Axis Selection
        self.x_axis_combo = QComboBox()
        self.y_axis_combo = QComboBox()

        # Add widgets to form layout
        form_layout.addRow(QLabel("Choose Data File:"), self.upload_button)
        form_layout.addRow("", self.file_label)
        form_layout.addRow(QLabel("Library:"), self.library_combo)
        form_layout.addRow(QLabel("Plot Type:"), self.plot_type_combo)
        form_layout.addRow(QLabel("X-axis:"), self.x_axis_combo)
        form_layout.addRow(QLabel("Y-axis:"), self.y_axis_combo)

        # --- Action Buttons ---
        self.plot_button = QPushButton("Plot")
        self.plot_button.setFont(QFont('Arial', 12, QFont.Bold))
        self.plot_button.clicked.connect(self.generate_plot)

        self.export_button = QPushButton("Export")
        self.export_button.setFont(QFont('Arial', 12))
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)  # Disabled until a plot is made

        button_layout.addWidget(self.plot_button)
        button_layout.addWidget(self.export_button)

        # --- Plot Area (using QStackedWidget to switch between Matplotlib and Plotly) ---
        self.plot_stack = QStackedWidget()

        # Matplotlib/Seaborn canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Plotly canvas
        self.plotly_view = QWebEngineView()

        self.plot_stack.addWidget(self.canvas)
        self.plot_stack.addWidget(self.plotly_view)

        # --- Message Box ---
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.message_box.setFixedHeight(80)
        self.message_box.setPlaceholderText("Process messages will appear here...")

        # --- Assemble Main Layout ---
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.message_box)
        main_layout.addWidget(self.plot_stack)  # Add plot area at the bottom

        self.setLayout(main_layout)

        # --- Initial State ---
        self.update_plot_types()
        self.x_axis_combo.setEnabled(False)
        self.y_axis_combo.setEnabled(False)

    def log_message(self, message):
        """Appends a message to the message box."""
        self.message_box.append(message)
        print(message)  # Also print to console for debugging

    def upload_file(self):
        """Opens a file dialog to select and load a data file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Data File", "", "Data Files (*.csv *.xlsx *.json);;All Files (*)", options=options
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.df = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                self.df = pd.read_json(file_path)
            else:
                raise ValueError("Unsupported file format.")

            self.file_label.setText(os.path.basename(file_path))
            self.log_message(f"Successfully loaded '{os.path.basename(file_path)}'.")

            # Populate axis dropdowns
            self.update_axis_options()

        except Exception as e:
            self.log_message(f"Error loading file: {e}")
            self.df = None
            self.file_label.setText("No file selected.")
            self.update_axis_options()

    def update_axis_options(self):
        """Updates the X and Y axis dropdowns based on the loaded dataframe."""
        self.x_axis_combo.clear()
        self.y_axis_combo.clear()

        if self.df is not None:
            columns = self.df.columns.tolist()
            self.x_axis_combo.addItems(columns)
            self.y_axis_combo.addItems(columns)
            self.x_axis_combo.setEnabled(True)
            self.y_axis_combo.setEnabled(True)
        else:
            self.x_axis_combo.setEnabled(False)
            self.y_axis_combo.setEnabled(False)

    def update_plot_types(self):
        """Updates the plot type dropdown based on the selected library."""
        library = self.library_combo.currentText()
        self.plot_type_combo.clear()

        plot_types = {
            "matplotlib": ["Line", "Bar", "Scatter", "Histogram"],
            "seaborn": ["Line", "Bar", "Scatter", "Histogram", "Box", "Violin"],
            "plotly": ["Line", "Bar", "Scatter", "Histogram", "Box"]
        }

        if library in plot_types:
            self.plot_type_combo.addItems(plot_types[library])

    def generate_plot(self):
        """Validates inputs and generates the selected plot."""
        # --- Input Validation ---
        if self.df is None:
            self.log_message("Error: No data file loaded.")
            return

        library = self.library_combo.currentText()
        plot_type = self.plot_type_combo.currentText()
        x_col = self.x_axis_combo.currentText()
        y_col = self.y_axis_combo.currentText()

        if not all([library, plot_type, x_col]):
            self.log_message("Error: Please select a library, plot type, and X-axis.")
            return

        # Histogram only needs X-axis
        if plot_type != "Histogram" and not y_col:
            self.log_message("Error: Please select a Y-axis for this plot type.")
            return

        self.log_message(f"Generating '{plot_type}' plot using '{library}'...")
        self.current_plot_library = library
        self.export_button.setEnabled(False)  # Disable until plot is successful

        try:
            if library in ["matplotlib", "seaborn"]:
                self.plot_stack.setCurrentIndex(0)  # Switch to Matplotlib canvas
                self.plot_with_matplotlib_seaborn(library, plot_type, x_col, y_col)
            elif library == "plotly":
                self.plot_stack.setCurrentIndex(1)  # Switch to Plotly view
                self.plot_with_plotly(plot_type, x_col, y_col)

            self.export_button.setEnabled(True)
            self.log_message("Plot generated successfully.")

        except Exception as e:
            self.log_message(f"Error generating plot: {e}")

    def plot_with_matplotlib_seaborn(self, library, plot_type, x_col, y_col):
        """Handles plotting for Matplotlib and Seaborn."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Use Seaborn for better aesthetics if selected
        sns.set_theme(style="whitegrid")

        if plot_type == "Line":
            sns.lineplot(data=self.df, x=x_col, y=y_col, ax=ax)
        elif plot_type == "Bar":
            sns.barplot(data=self.df, x=x_col, y=y_col, ax=ax)
        elif plot_type == "Scatter":
            sns.scatterplot(data=self.df, x=x_col, y=y_col, ax=ax)
        elif plot_type == "Histogram":
            sns.histplot(data=self.df, x=x_col, kde=True, ax=ax)
        elif plot_type == "Box" and library == "seaborn":
            sns.boxplot(data=self.df, x=x_col, y=y_col, ax=ax)
        elif plot_type == "Violin" and library == "seaborn":
            sns.violinplot(data=self.df, x=x_col, y=y_col, ax=ax)
        else:  # Fallback to matplotlib for its specific types if needed
            if plot_type == "Line":
                ax.plot(self.df[x_col], self.df[y_col])
            # Add other pure matplotlib plots if needed

        ax.set_title(f"{plot_type} Plot of {y_col} vs {x_col}")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col if plot_type != "Histogram" else "Frequency")
        self.figure.tight_layout()
        self.canvas.draw()

    def plot_with_plotly(self, plot_type, x_col, y_col):
        """Handles plotting for Plotly."""
        fig = None
        title = f"{plot_type} Plot of {y_col} vs {x_col}"

        if plot_type == "Line":
            fig = px.line(self.df, x=x_col, y=y_col, title=title)
        elif plot_type == "Bar":
            fig = px.bar(self.df, x=x_col, y=y_col, title=title)
        elif plot_type == "Scatter":
            fig = px.scatter(self.df, x=x_col, y=y_col, title=title)
        elif plot_type == "Histogram":
            fig = px.histogram(self.df, x=x_col, title=f"Histogram of {x_col}")
        elif plot_type == "Box":
            fig = px.box(self.df, x=x_col, y=y_col, title=title)

        if fig:
            self.plotly_fig = fig
            self.plotly_view.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def export_plot(self):
        """Exports the currently displayed plot to an image file."""
        if (self.current_plot_library in ["matplotlib", "seaborn"] and not self.figure.get_axes()) or \
                (self.current_plot_library == "plotly" and self.plotly_fig is None):
            self.log_message("Error: No plot to export.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Plot", "", "PNG Image (*.png);;JPEG Image (*.jpg)", options=options
        )
        if not file_path:
            return

        try:
            if self.current_plot_library in ["matplotlib", "seaborn"]:
                self.figure.savefig(file_path, dpi=300)
            elif self.current_plot_library == "plotly":
                self.plotly_fig.write_image(file_path, scale=2)

            self.log_message(f"Plot successfully exported to {file_path}")
        except Exception as e:
            self.log_message(f"Error exporting plot: {e}")
            self.log_message("Note: Exporting Plotly figures requires the 'kaleido' package.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotGenerator()
    ex.show()
    sys.exit(app.exec_())