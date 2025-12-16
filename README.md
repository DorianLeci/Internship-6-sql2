# Internship-6-sql2

<b>Steps to install project</b>

```
git clone git@github.com:DorianLeci/Internship-6-sql2.git
cd Internship-6-sql2
```
After positioning inside project folder you will see the folder SqlFiles whose file contents you must open in PgAdmin.</br>
Inside there is 
</br>
1)<b>TableCreation.sql</b> for creating database tables and adding constraints.
</br>
2) <b>SqlQuery.sql</b> for running queries to databsase.
</br>
3)<b>Index.sql</b> for creating indexes on table attributes.
</br>
4)<b>DropIndex.sql</b> for deleteing created indexes.This is useful for running query with and without index to compare execution time and other stats.
</br>

Before creating any of tables or inserting data,you must create database with name 
```
Internship-6-sql2
```
You can create tables and insert data into database in two ways

1)After creating database with given name,right click on it then find Restore in the menu.After clicking on Restore,in folder <b>Backup</b> find file "Internship-6-sql2-backup.sql" which is database backup and click Select.
(If you can not find file-in file explorer click on SQL File so it searches for right file type).This step is done in PgAdmin.
</br>

2)After creating database and running "TableCreation.sql" you must create python virtual enviroment in root repository folder(after cd Internship-6-sql2) so you can install requirements for running "main.py" inside PythonScripts folder.This script automatically inserts data from json files to created database.

Steps:

On windows:
```
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macos/linux:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then type 
```
cd PythonScripts
python3 Main.py
```

After running python script or loading database backup you can create indexes and run sql queries.



