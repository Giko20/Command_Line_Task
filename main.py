# import libraries
import sqlite3
import os
import subprocess
import random
import string

# if name is not presented this function generates random name
def get_random_string(length=8):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# function to create or connect to existing database
def create_connect_database(database):
    database_name = input("Enter SqLite Database name to create connection: ")
    if database_name != '':
        database = database_name
    else:
        database = get_random_string()

    # connect to SqLite database
    try:
        conn = sqlite3.connect(f'{database}.db')
        print(f'Succesfully connected!')
        c = conn.cursor()
        return c
    except Exception as e:
        print(e)

# function to execute sql queries
def execute_query(con, query):
    result = con.execute(query)
    return result.fetchall()

# function to display results
def display_results(results):
    for row in results:
        print(row)

def runner_code():
    # allowing user to run commands
    while True:
            command = input("Enter a Command ('quit' to exit or 'help' for usage hints ): ")
            if command == 'quit':
                break
            elif command == 'help':
                subprocess.run(['cat', 'help.txt'])
            else:
                # executing SQL queries
                if command.endswith(';'):
                    try:
                        results = execute_query(c,command)
                        display_results(results)
                    except sqlite3.Error as e:
                        print('Error executing query:', e)

                    if command.startswith('SELECT') or command.startswith('select'):
                        file_response = input("Do you want to store query results into the file?(y/n): ")
                        if file_response == 'y':
                            filename = input("Enter a filename to save the results: ")
                            if filename != '':
                                file = filename
                            else:
                                file = get_random_string()

                            with open(file, 'w') as f:
                                for row in results:
                                    f.write(str(row) + '\n')
                            print('result saved successfully!')

                            # ask if user wants to make manipulations
                            file_manipulates = input('Do you want to make manipulations on this file? (y/n): ')

                            if file_manipulates == 'y':
                                py_script = input('Enter a Python script to make manipulations on this file: ')

                                # Check if the user entered a Python script to execute
                                if py_script.endswith('.py'):
                                    try:
                                        # Execute the script using the subprocess module
                                        subprocess.run(['python', py_script, file])
                                    except Exception as sub_error:
                                        print('Error during manipulation ', sub_error)
                            else:
                                pass

                        else: pass

                # to run any python script
                elif command.endswith('.py'):
                    subprocess.run(['python', command])

                # to run linux commands
                else:
                    os.system(command)


if __name__ == '__main__':
    runner_code()
# commit executed commands and close database connection
    conn.commit()
    conn.close()

