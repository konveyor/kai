# Install and Configure Apache Tomcat 11

## Step 1: Download and Install Apache Tomcat 11

1. Download the latest Apache Tomcat 11 binary from the official website:
   - [Apache Tomcat Downloads](https://tomcat.apache.org/download-11.cgi)
2. Extract the downloaded archive:

   ```bash
   tar -xvzf apache-tomcat-11*.tar.gz
   cd apache-tomcat-11*
   ```

3. Make the bin scripts executable:
   ```bash
   chmod +x bin/*.sh
   ```

## Step 2: Change the Manager Password

1. Open the `conf/tomcat-users.xml` file in a text editor:

   ```bash
   vim conf/tomcat-users.xml
   ```

2. Add or update the manager user with a new password within the `<tomcat-users>` config(replace yourpassword with a secure one):

   ```xml
   <role rolename="manager-gui"/>
   <user username="tomcat" password="yourpassword" roles="manager-gui"/>
   ```

3. Save and exit the file.

## Step 3: Start the Tomcat Server

1. Run the startup script:

   ```bash
   cd bin && ./startup.sh
   ```

2. To verify Tomcat is running, open your browser and go to `http://localhost:8080`.
