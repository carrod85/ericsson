# Project Challenge Ericsson.
1. Configuration file has been created to avoid uploading credentials details to github, by adding 
file to gitignore.

## Steps followed to carry on task
1. First, it has been selected database. In this case has been elected Titanic dataset from kaggle.com, https://github.com/dsindy/kaggle-titanic/blob/master/data/test.csv.
This database consist in only one table.

2. Then, for the task of inserting the data in database, it has been chosen MySQL. Also a Virtual env has been created using conda and the package mysql connector has been installed on the Venv.

3. At the beginning a localhost connection has been used to move the data into the database. Here **first challenge** has been faced, in order to make a valid connection with database 
from the script. The default authentication method in mysql is "mysql_caching_sha2_password", but the python's mysql.connector was not supporting this authentication method. For practical purposes, it has been decided to change auth. method to mysql_native_password (more insecure).
With the new authentication method the connection has been established and I was ready now to pull in my data.

4. For the automation script, the following approach has been followed:

    4.1 One function for import data from csv and fill empty data with pandas fillna method, so all entries are recognized by MySQL.
    
    4.2 Function for connection.
    
    4.3 Function to create new database (if it exists don't create it).
    
    4.4 Function for creation the table( the table is drop every time the scrip is run to avoid errors). Also the data is inserted.
    
    4.5 Function for creation of new column and update it with the names of the cities so it can be recognized by tableau later on and build the map.
    For this feature a Procedure has been written inside mysql.
    ```mysql
      begin
      /* delete columns if they exist */
    
       if exists (select * from information_schema.columns where table_name = 'passengers' and column_name = 'cities') then
          alter table passengers drop column cities;
       end if;
      end
   ```
   The procedure has been chosen because I check input and if the table and column exist then drop it, to create it once again, so there is no need to comment in any code **small challenge**.
   
   4.6 Last function is used to close connection with database.
   
5. The next task has been to create a tableau desktop dashboard where the data coming from the database can be used to show informative charts and graphs.
Here a **new challenge** has been faced. My computer software is not compatible anymore with tableau, so I reckoned which possibilities 
I had to make direct connection with tableau and database.
I considered making it in cloud but then the mysql's ip would have to be public and would have to bypass firewall restrictions and open 
ports to the external world, so I discarded it 
and created a windows virtual machine installing windows 10, then I could install there tableau. Then I created a new connection in mysql
to accept incoming connections from any ip (0.0.0.0:3306) and allow the user connections from any ips inside mysql with the wildcard %.
With all this set up, I was able to connect tableau and MySQL.:)

6. The rest has been to create a dashboard with different sheets from the data contained in the table. Here another **small challenge** has been faced.
I had planned to create 3 sheets, one of them was to visualize a map with the different departure locations picked up by titanic passengers.
For that I created a new column with the name of the cities and then since their names are ambiguous(for instance
Southampton can be related to different locations) I had to specify Latitude and Longitud or select the correct city from list.

7. I used some parameters like the count function in tableau for counting the passengers for every location. Then 2 more charts, one for the distribution of age,
where I filtered the data where the age for particular passengers didn't exist(default 0) with the help of table. The other for the distribution by sex.

8. As an additional task and because of the importance I am giving to documentation (to avoid forgetting things), I decided to explain the process and 
upload it all in github.
   
    

