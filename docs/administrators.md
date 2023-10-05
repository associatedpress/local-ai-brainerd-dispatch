# Administration Guide

## Configuring AWS EC2
-	Login to AWS and create an AWS EC2 instance.
-	SSH into the instance and clone the GitHub repo.
-	Navigate to the `docker-compose.yml` file.
-	We are going to deploy the application using docker containers.
-	Install the Docker inside the machine and follow the commands to run the Server, UI containers for the application.

## Installing Docker
Update your existing list of packages.
```sh
sudo apt update
```

Install pre-requisite packages.
```sh
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

Add the GPC key for official Docker repository.
```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Add Docker repository to APT sources.
```sh 
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Update the existing packages again.
```sh
sudo apt update
```

Install from Docker repo instead of Ubuntu repo.
```sh
apt-cache policy docker-ce
```

Install Docker.
```sh
sudo apt install docker-ce
```

Check the status.
```sh
sudo systemctl status docker
```

Run Docker without sudo option.
```sh
sudo usermod -aG docker ${USER}
su - ${USER}
groups
sudo usermod -aG docker username
```

## Configuring the MySQL Database
We maintain the database outside the container for managing the admin services better. Create a MySQL RDS instance in AWS and connect to the database machine using any DB client. 

Execute the SQL script named `db.sql` in the database-scripts directory to build the default database. 
The initial username is set as `admin` and the password is `LoveLocalNews2023!`

> Note: Change the initial username and passsword as soon as possible to maintain security

## Running the Application
Both the Server and UI applications are run using docker-compose.yml file.
- Clone the GitHub repository into the system.
- Navigate to the `docker-compose.yml` file and adjust as needed.
- Navigate inside `react-ui` directory and open the `.env` file and replace the localhost with EC2 public IP.
- Navigate inside the `flask-server` directory and open the `config.py` file and fill in the AWS RDS database host URI.
- Run the container.
```sh
docker compose build
docker compose up
```
- The following commands are only needed when you want to relaunch the application.
```sh
docker compose down --rmi all -v
docker compose build
docker compose up
```
- Access the application at: `http://IP_ADDRESS/loginpage`
