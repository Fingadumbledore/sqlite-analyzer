# SQLite Analyzer

This project is a simple web service that allows generating and displaying an ER model for a SQLite database. The ER model is created as a PNG image to visualize the relationships between tables in the database.

## Requirements

To run this project, you need:

- Python 3 installed on your system.
- The Python libraries Flask and Graphviz. You can install them via pip:

    ```bash
    pip install Flask graphviz
    ```

## Usage

1. Clone or download the project to your local computer.
2. Navigate to the project directory.
3. Start the application by running the `main.py` file:

    ```bash
    python main.py
    ```

4. Open a web browser and go to the URL [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
5. Upload a SQLite database file (`.db` file extension).
6. The ER model will be automatically generated and displayed along with table data.

## Features

- **ER Model Generation**: The ER model is automatically generated from the uploaded SQLite database and displayed as a PNG image.
- **Display of Table Data**: The data of each table in the uploaded SQLite database is displayed to facilitate quick data inspection.

## File Structure

- `main.py`: The main application that creates the web service using Flask.
- `uploads/`: The directory where uploaded SQLite database files are stored.
- `templates/`: The directory containing HTML templates for the web pages.
- `static/`: The directory containing static files such as CSS or images.

## Contributors

- **Author**: fingadumbledore
## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

