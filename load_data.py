import pandas as pd  
import psycopg2      

conn = psycopg2.connect(database="ecom", user="user", password="pass", host="localhost", port="5432")  # Connect to DB
cur = conn.cursor()  

df = pd.read_csv('products.csv')  # Read CSV file
for _, row in df.iterrows():  # Iterate over rows
    cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s)", (row['id'], row['name'], row['price']))  # Insert data

conn.commit()  
cur.close()    
conn.close()   
