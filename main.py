from flask import Flask, render_template, request, send_file
import sqlite3
import os
from graphviz import Digraph

app = Flask(__name__)

# Verzeichnis für hochgeladene Dateien
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def create_er_model(database_file, output_file='er_model.png'):
    """Erstellt ein ER-Modell für die angegebene SQLite-Datenbank und speichert es als Bild."""
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    # Graphviz-Diagramm erstellen
    dot = Digraph()

    # Dictionary zur Speicherung der Fremdschlüsselbeziehungen
    foreign_keys = {}

    # Für jede Tabelle Informationen über Spalten abrufen und dem Diagramm hinzufügen
    for table in tables:
        table_name = table[0]
        dot.node(table_name, shape='rectangle', color='lightblue2', style='filled')
        
        # Spalten der Tabelle abrufen
        c.execute(f"PRAGMA table_info({table_name});")
        columns = c.fetchall()
        
        # Jede Spalte als Knoten im Diagramm hinzufügen
        for column in columns:
            column_name = column[1]
            dot.node(f"{table_name}.{column_name}", label=column_name, shape='ellipse')

            # Verbindung von Tabelle zu Spalte erstellen
            dot.edge(table_name, f"{table_name}.{column_name}")

        # Fremdschlüsselbeziehungen abrufen
        c.execute(f"PRAGMA foreign_key_list({table_name});")
        foreign_keys[table_name] = c.fetchall()

    # Fremdschlüsselbeziehungen als Kanten im Diagramm hinzufügen
    for table, fks in foreign_keys.items():
        for fk in fks:
            parent_table = fk[2]
            parent_column = fk[3]
            child_table = table
            child_column = fk[4]
            dot.edge(f"{parent_table}.{parent_column}", f"{child_table}.{child_column}", label='1..n')

    # ER-Modell als Graphviz-Dot-Datei speichern
    dot.render(output_file, format='png', cleanup=True)

    # Verbindung schließen
    conn.close()

    return output_file

# Route für den Index
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    er_model = None
    table_data = None

    if request.method == 'POST':
        # Überprüfen, ob eine Datei hochgeladen wurde
        if 'file' not in request.files:
            error = 'Keine Datei hochgeladen'
        else:
            file = request.files['file']

            # Überprüfen, ob eine Datei ausgewählt wurde
            if file.filename == '':
                error = 'Keine Datei ausgewählt'

            # Überprüfen, ob die Datei eine SQLite-Datenbank ist
            elif file.filename.endswith('.db'):
                # Datei speichern
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                # ER-Modell erstellen
                er_model_file = create_er_model(file_path)
                os.rename("er_model.png.png", "er_model.png")
                er_model = er_model_file

                # Tabellendaten abrufen
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                table_data = {}
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT * FROM {table_name};")
                    table_data[table_name] = cursor.fetchall()
                conn.close()

            else:
                error = 'Die hochgeladene Datei muss eine SQLite-Datenbankdatei sein'

    # HTML-Seite mit den Daten anzeigen
    return render_template('index.html', error=error, er_model=er_model, table_data=table_data)

# Route zum Anzeigen des ER-Modells
@app.route('/er_model/<filename>')
def show_er_model(filename):
    return send_file(os.path.abspath(filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
