import mysql.connector
config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'preguntas_tcgp',
        'port': 3306
    }


def connectDB():   
    try:
        connectionBBDD = mysql.connector.connect(**config)
        print("Conexión exitosa a la base de datos.")
        return connectionBBDD
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
