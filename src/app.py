from flask import Flask, request, jsonify, g, abort
import numpy as np
from src import pipe 
import sqlite3

# Creating our Flask App
app=Flask(__name__)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('src/devices.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table with the specified columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    battery_power FLOAT,
    blue FLOAT,
    clock_speed FLOAT,
    dual_sim FLOAT,
    fc FLOAT,
    four_g FLOAT,
    int_memory FLOAT,
    m_dep FLOAT,
    mobile_wt FLOAT,
    n_cores FLOAT,
    pc FLOAT,
    px_height FLOAT,
    px_width FLOAT,
    ram FLOAT,
    sc_h FLOAT,
    sc_w FLOAT,
    talk_time FLOAT,
    three_g FLOAT,
    touch_screen FLOAT,
    wifi FLOAT,
    price_range FLOAT
)
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

# Our Database file
DATABASE='src/devices.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn



# Teardown function to close database connection
@app.teardown_appcontext
def close_db_connection(exception=None):
    db = g.pop('db_connection', None)
    if db is not None:
        db.close()



# Endpoint to retrieve a list of all devices
@app.route('/api/devices/', methods=['POST'])
def get_devices():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices')
    devices = cursor.fetchall()
    
    conn.close()
    
    # Convert the query results to a list of dictionaries
    devices_list = [dict(row) for row in devices]
    
    return jsonify(devices_list)



# Endpoint to retrieve details of a specific device by ID
@app.route('/api/devices/<int:id>', methods=['GET'])
def get_device(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE id = ?', (id,))
    device = cursor.fetchone()
    
    conn.close()
    
    if device is None:
        abort(404, description="Device not found")
    
    # Convert the row to a dictionary
    device_dict = dict(device)
    
    return jsonify(device_dict)



# Endpoint to add a new device
@app.route('/api/devices', methods=['POST'])
def add_device():
    # Get data from the request
    data = request.json
    
    # Check if all required fields are present
    required_fields = ['battery_power', 'blue', 'clock_speed', 'dual_sim', 'fc', 'four_g',
                       'int_memory', 'm_dep', 'mobile_wt', 'n_cores', 'pc', 'px_height',
                       'px_width', 'ram', 'sc_h', 'sc_w', 'talk_time', 'three_g',
                       'touch_screen', 'wifi']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")
    
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert new device into the database
    cursor.execute('''
        INSERT INTO devices (battery_power, blue, clock_speed, dual_sim, fc, four_g,
                             int_memory, m_dep, mobile_wt, n_cores, pc, px_height,
                             px_width, ram, sc_h, sc_w, talk_time, three_g,
                             touch_screen, wifi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(data[field] for field in required_fields))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Device added successfully"}), 201



# Endpoint to predict data for a specific device
@app.route('/api/predict/<int:id>', methods=['POST'])
def predict_device_data(id):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch device data from the database
    cursor.execute('SELECT  battery_power, blue, clock_speed, dual_sim, fc, four_g, '
               'int_memory, m_dep, mobile_wt, n_cores, pc, px_height, px_width, '
               'ram, sc_h, sc_w, talk_time, three_g, touch_screen, wifi '
               'FROM devices WHERE id = ?', (id,))
    device = cursor.fetchone()
    
    
    # Check if the device exists
    if device is None:
        abort(404, description="Device not found")
    
    # Convert device data to a NumPy array
    device_data = dict(device)  
    price=pipe.predict(device_data)

    # Update the price_range column in the database
    cursor.execute('UPDATE devices SET price_range = ? WHERE id = ?', (float(price), id))
    conn.commit()
    
    conn.close()

    return jsonify({"predicted_price": str(price)})


# Running our APP
if __name__ == '__main__':
    app.run(debug=True)