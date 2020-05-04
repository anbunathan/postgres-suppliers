import psycopg2
from config import config

class postgressql:
    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def create_tables(self):
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE vendors (
                vendor_id SERIAL PRIMARY KEY,
                vendor_name VARCHAR(255) NOT NULL
            )
            """,
            """ CREATE TABLE parts (
                    part_id SERIAL PRIMARY KEY,
                    part_name VARCHAR(255) NOT NULL
                    )
            """,
            """
            CREATE TABLE part_drawings (
                    part_id INTEGER PRIMARY KEY,
                    file_extension VARCHAR(5) NOT NULL,
                    drawing_data BYTEA NOT NULL,
                    FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE vendor_parts (
                    vendor_id INTEGER NOT NULL,
                    part_id INTEGER NOT NULL,
                    PRIMARY KEY (vendor_id , part_id),
                    FOREIGN KEY (vendor_id)
                        REFERENCES vendors (vendor_id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (part_id)
                        REFERENCES parts (part_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
        conn = None
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_vendor(self, vendor_name):
        """ insert a new vendor into the vendors table """
        sql = """INSERT INTO vendors(vendor_name)
                 VALUES(%s) RETURNING vendor_id;"""
        conn = None
        vendor_id = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (vendor_name,))
            # get the generated id back
            vendor_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return vendor_id

    def insert_vendor_list(self, vendor_list):
        """ insert multiple vendors into the vendors table  """
        sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.executemany(sql, vendor_list)
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def update_vendor(self,vendor_id, vendor_name):
        """ update vendor name based on the vendor id """
        sql = """ UPDATE vendors
                    SET vendor_name = %s
                    WHERE vendor_id = %s"""
        conn = None
        updated_rows = 0
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(sql, (vendor_name, vendor_id))
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows

    def add_part(self, part_name, vendor_list):
        # statement for inserting a new row into the parts table
        insert_part = "INSERT INTO parts(part_name) VALUES(%s) RETURNING part_id;"
        # statement for inserting a new row into the vendor_parts table
        assign_vendor = "INSERT INTO vendor_parts(vendor_id,part_id) VALUES(%s,%s)"

        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # insert a new part
            cur.execute(insert_part, (part_name,))
            # get the part id
            part_id = cur.fetchone()[0]
            # assign parts provided by vendors
            for vendor_id in vendor_list:
                cur.execute(assign_vendor, (vendor_id, part_id))
            # commit changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_vendors(self):
        """ query data from the vendors table """
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
            print("The number of vendors: ", cur.rowcount)
            row = cur.fetchone()
            while row is not None:
                print(row)
                row = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_parts(self):
        """ query parts from the parts table """
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT part_id, part_name FROM parts ORDER BY part_name")
            rows = cur.fetchall()
            print("The number of parts: ", cur.rowcount)
            for row in rows:
                print(row)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def iter_row(self, cursor, size=10):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def get_part_vendors(self):
        """ query part and vendor data from multiple tables"""
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("""
                SELECT part_name, vendor_name
                FROM parts
                INNER JOIN vendor_parts ON vendor_parts.part_id = parts.part_id
                INNER JOIN vendors ON vendors.vendor_id = vendor_parts.vendor_id
                ORDER BY part_name;
            """)
            for row in self.iter_row(cur, 10):
                print(row)
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def delete_part(self, part_id):
        """ delete part by part id """
        conn = None
        rows_deleted = 0
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute("DELETE FROM parts WHERE part_id = %s", (part_id,))
            # get the number of updated rows
            rows_deleted = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return rows_deleted