import psycopg2
import sys


# In this function the database connection is created. And that connection object is returned.
# In first database creation we don't have database of given pdf name.
# So using defalut database we create connection and execute the code. (so there defalut value is "postgres")


def getConnection(databaseName='postgres'):
    conn = None
    try:
        conn = psycopg2.connect(
            database=databaseName.lower(), user='postgres', password='root', host='localhost', port='5432'
        )
        return conn
    except Exception as error:
        print(error)


# Here in this function the database is created and the databaseName is set as the name of the new database.


def createDatabase(databaseName):
    conn = None
    cursor = None
    try:
        # The following function call will return the conn object.
        conn = getConnection()
        cursor = conn.cursor()
        conn.autocommit = True

        # Closes all the previous sessions and removes them by exectuing the following query.
        cursor.execute(
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = '{str(databaseName).lower()}';")

        # Checks for the database is already present or not and if present and drops that database.
        droping_database_query = 'DROP DATABASE  IF EXISTS {}'.format(
            databaseName.lower())
        cursor.execute(droping_database_query)

        # New database is created here.
        sql = 'CREATE database {}'.format(databaseName)
        cursor.execute(sql)
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# This function is for inserting the text per page into the database.
# In this function the text_table is created for the text insert.
# Function accepts databaseName and the list of objects for insert.


def insertTextData(databaseName, listOfTextDataObjects):

    # print(type(listOfTextDataObjects[0].text))
    conn = None
    cursor = None
    try:
        conn = getConnection(databaseName)
        cursor = conn.cursor()
        conn.autocommit = True

        # Here the text table is created inside the given databaseName the table mainly have 3 columns "id", "page_number", "text"

        sql = 'CREATE TABLE text_table (id serial ,page_number int PRIMARY KEY, text TEXT)'
        cursor.execute(sql)

        # Here the objects from the list are taken and inserted one by one.

        for obj in listOfTextDataObjects:
            query = 'insert into text_table (page_number, text) values (%s,%s)'
            insert_values = (obj.pageNumber, obj.text)
            cursor.execute(query, insert_values)

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# This function is for inserting the images found per page into the database.
# In this function the image_table is created for the image insert.
# Function accepts databaseName and the list of ImageData objects for insert.


def insertImageData(databaseName, listOfImageDataObjects):
    conn = None
    cursor = None
    try:
        conn = getConnection(databaseName)
        cursor = conn.cursor()
        conn.autocommit = True

        # Here the image_table is created inside the given databaseName the table mainly have 3 columns "id", "page_number", "image_blob"
        # In this table the page_number is foreign key which is refering the page number from the text_table

        sql = '''CREATE TABLE image_table (
        id          serial PRIMARY KEY,
        page_number int  references text_table(page_number),
        image_blob   bytea
        )'''
        cursor.execute(sql)

        # Here the objects from the list are taken and inserted one by one.

        for obj in listOfImageDataObjects:
            query = 'insert into image_table (page_number, image_blob) values (%s,%s)'
            insert_values = (obj.pageNumber, obj.image)
            cursor.execute(query, insert_values)
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# This function is written for a cross check of the image bytes stored in the database

def fetchAndStoreImages(databaseName):
    try:
        # Connecting to database using the PostgreSQL adapter
        con = getConnection(databaseName)
        # Creating the cursor object to run queries
        cur = con.cursor()
        cur.execute("SELECT image_blob FROM image_table")
        for i in range(1, 4):

            # fetchone method returns a tuple object of next row of query result set
            # image data is in first column after Select query execution, so [0] index
            image = cur.fetchone()[0]

        # the image data is written to file using db_img() for viewing
            db_img(image, i)
    except (Exception, psycopg2.Error) as e:
        # Print exception
        print(e)
    finally:
        # print("in the conn finally")
        con.close()

# This function is for saving the cross checked images in the folder.


def db_img(data, num):
    # out variable set to null
    out = None

    try:
        # creating files in output folder for writing in binary mode
        out = open(
            r'C:\Users\vaibhav_talap\Desktop\Assisgnments\extracted images\out'+str(num)+'.jpg', 'wb')

        # writing image data
        out.write(data)

    # if exception raised
    except IOError:
        sys.exit(1)

    # closing output file object
    finally:
        # print("in the out finally")
        out.close()
