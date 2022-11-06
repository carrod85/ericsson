
import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import connection_details


def import_csv():
    titanicData = pd.read_csv('tested.csv')
    values = {"Age": 0, "Cabin": 'None', "Fare":0}
    titanicDataClean = titanicData.fillna(value=values)
    #print(titanicData.head())
    return titanicDataClean


def connection():
    try:
        global conn
        conn = msql.connect(
            host=connection_details.HOST,
            user=connection_details.USER,
            password=connection_details.PASSWORD,
            auth_plugin='mysql_native_password'
        )

        if conn.is_connected():
            print("Connection established")
    except Error as e:
        print("Error while connecting to MySQL", e)

def create_database():
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS titanic; ")


def create_table(database):
    cursor = conn.cursor()
    cursor.execute("USE " + database + ";")
    cursor.execute('DROP TABLE IF EXISTS passengers;')
    cursor.execute("CREATE TABLE passengers (PassengerId SMALLINT NOT NULL, Survived BOOLEAN NOT NULL,\
Pclass TINYINT, Name VARCHAR(100) NOT NULL,Sex CHAR(50), Age FLOAT(5,2), SibSp TINYINT, Parch TINYINT,\
Ticket VARCHAR(50),Fare FLOAT(6,2), Cabin VARCHAR(50), Embarked CHAR(1), PRIMARY KEY (PassengerId))")
    print("table passengers created.")
    for i,row in import_csv().iterrows():
        #print(row)
        sql_statement = "INSERT INTO titanic.passengers VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql_statement,tuple(row))
        print("Record inserted "+ str(i))
        conn.commit()


def create_new_column_cities(database):
    cursor = conn.cursor()
    cursor.execute("USE " + database + ";")
    # create a procedure to drop column. if exists drop column
    cursor.callproc('schema_change')
    query_1 = "ALTER TABLE passengers ADD COLUMN cities CHAR(20) Default 'None';"
    cursor.execute(query_1)
    #query_2 ="UPDATE passengers SET cities = 'Cobh' WHERE embarked='Q';"
    query_2 = "UPDATE passengers SET cities = CASE WHEN embarked ='Q' THEN 'Cobh'\n\
WHEN embarked ='S' THEN 'Southampton'\n\
WHEN embarked='C' THEN 'Cherbourg'\n\
else cities\n\
end;"
    cursor.execute(query_2)
    conn.commit()


def close():
    conn.close()


if __name__ == '__main__':
    #connect
    connection()
    #create database
    create_database()
    #create table. database titanic and insert data.
    database = 'titanic'
    create_table(database)
    #add a new column
    create_new_column_cities(database)
    #close connection
    close()



