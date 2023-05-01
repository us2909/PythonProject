import tkinter as tk
import subprocess
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly.graph_objs import Scatter

# Function to run the Tic Tac Toe game
def run_tic_tac_toe_game():
    subprocess.Popen(["python", "tic_tac_toe_game.py"])

# Function to run the Connect Four game
def run_connect_four_game():
    subprocess.Popen(["python", "connect_four_game.py"])

# Function to create a data visualization window
def visualize_data():
    # Function to create a Dash app for data visualization
    def create_dash_app(data_file_path):
        # Read the data from the selected CSV file
        data = pd.read_csv(data_file_path)

        # Initialize the Dash app
        app = dash.Dash(__name__)

        # Set up the layout of the Dash app
        app.layout = html.Div([
            html.H1('Line Chart'),  # Title of the chart
            dcc.Dropdown(  # Dropdown menu to select columns
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in data.columns[1:]],
                value=data.columns[1]
            ),
            dcc.Graph(id='line-chart')  # Graph to display the line chart
        ])

        # Function to update the line chart based on the selected column
        @app.callback(
            Output('line-chart', 'figure'),
            [Input('xaxis-column', 'value')]
        )
        def update_graph(xaxis_column_name):
            return {
                'data': [Scatter(x=data[data.columns[0]], y=data[column], mode='lines', name=column) for column in data.columns[1:] if column != xaxis_column_name],
                'layout': {
                    'xaxis': {'title': data.columns[0]},
                    'yaxis': {'title': xaxis_column_name}
                }
            }

        # Run the Dash app
        app.run_server(debug=True)

    # Function to show the Dash app with the selected data file
    def show_visualization():
        option = data_choice.get()
        if option == 'Tic Tac Toe':
            data_file_path = 'data/tictactoe_data.csv'
        else:
            data_file_path = 'data/connect_four_data.csv'
        create_dash_app(data_file_path)

    # Create a new data visualization window
    data_window = tk.Toplevel(root)
    data_window.title("Data Visualization")

    # Create a dropdown menu to select the data file
    data_choice = tk.StringVar(data_window)
    data_choice.set("Tic Tac Toe")
    tk.Label(data_window, text="Choose data file:").pack()
    tk.OptionMenu(data_window, data_choice, "Tic Tac Toe", "Connect Four").pack()

    # Create a button to visualize the selected data
    tk.Button(data_window, text="Visualize", command=show_visualization).pack()

# Create the main window for selecting a game
root = tk.Tk()
root.title("Select a Game")
root.geometry("300x200")

# Add buttons for each game and data visualization
tk.Button(root, text="Tic Tac Toe", command=run_tic_tac_toe_game).pack()
tk.Button(root, text="Connect Four", command=run_connect_four_game).pack()
tk.Button(root, text="Visualize Data", command=visualize_data).pack()

# Start the main event loop of the tkinter application
root.mainloop()
