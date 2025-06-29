***AutoPlot-Python / Dynamic Plot Generator***:

A user-friendly desktop application built with Python and PyQt5 that empowers users to load, visualize, and export data from various file formats without writing a single line of code. This tool bridges the gap between raw data and insightful visualizations by providing an intuitive interface for a powerful plotting backend.

**Features**:

Multi-Format Data Loading: Seamlessly upload and parse data from .csv, .xlsx (Excel), and .json files.

Choice of Plotting Libraries: Generate plots using your preferred library:

Matplotlib: For classic, publication-quality static plots.

Seaborn: For statistically-focused and aesthetically pleasing visualizations.

Plotly: For fully interactive, web-based plots displayed directly in the app.

Diverse Plot Types: Supports a wide range of common plot types, including Line, Bar, Scatter, Histogram, Box, and Violin plots.

Dynamic UI: The interface intelligently updates dropdowns for plot types and axes based on the selected library and loaded data.

Interactive Plotting: View, zoom, and pan interactive Plotly charts within the application window.

One-Click Export: Export your generated plots as high-quality .png or .jpg images for use in reports and presentations.

Live Feedback: An integrated message box provides real-time status updates, success messages, and clear error notifications.

**Technology Stack**:

-GUI Framework: Python 3, PyQt5

-Data Handling: Pandas

-Plotting Engines: Matplotlib, Seaborn, Plotly

**Dependencies**:

-PyQtWebEngine for rendering Plotly charts.

-openpyxl for reading Excel files.

-kaleido for exporting Plotly charts to static images.

-Setup and Installation


Follow these steps to get the application running on your local machine.

**Prerequisites**

Python 3.6 or newer

**How to Use**

-Launch the application by running AutoPlot_V3.py.

-Upload Data: Click the Upload Data File button and select your .csv, .xlsx, or .json file. A success message will confirm the upload.

-Select Library: Choose your desired plotting library (matplotlib, seaborn, or plotly) from the first dropdown.

-Select Plot Type: The "Plot Type" dropdown will update with options available for the chosen library. Select one.

-Choose Axes: Select the columns from your data to serve as the X and Y axes. (The Y-axis is not required for a Histogram).

-Generate Plot: Click the Plot button. The visualisation will appear in the main window.

-Export Plot: Once a plot is generated, click the Export button to save it as a .png or .jpg file.


**Architectural Highlights**:

-This project was built with a focus on maintainability and scalability.

-Modular Design: The application logic is separated into distinct concerns: the GUI (PyQt5), data manipulation (Pandas), and plotting logic. This makes the codebase easier to understand, debug, and extend.

-Plotting Adapter: The code uses an adapter-like pattern to handle requests for different plotting libraries, allowing new libraries or plot types to be added with minimal changes to the core application.

-Dynamic Canvas: A QStackedWidget is used to seamlessly switch between the FigureCanvasQTAgg (for Matplotlib/Seaborn) and QWebEngineView (for Plotly), providing the correct canvas for each type of plot without cluttering the UI.

**License**

This project is licensed under the MIT License - see the LICENSE.md file for details.
