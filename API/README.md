# LiveDataLab API
The LiveDataLab API is a generalized infrastructure which integrates with webhook triggers from Github and Gitlab for running code with custom datasets on an autoscaling cloud infrastructure.

The API is hosted on Microsoft Azure and leverages Jenkins for job scheduling, scaling, and worker lifecycle management.

## Development
### Setup
The API is written in Python 3 using Flask with MongoDB as the persistent data store.

#### Virtual Environment
* A Python  virtual environment should be used during development. The virtual env can be initially created with `$ python3 -m venv venv`, where the second `venv` is the name of the virtual environment. If a name other than `venv` is chosen, the new name should also be added to the `.gitignore`.
* The virtual environment can be activated with `$ source venv/bin/activate` and de-activated with the command `$ deactivate`.
* Once within the virtual environment, dependencies should be installed by running `$ pip3 install -r requirements.txt`
* Before finalizing a pull request, any new dependencies should be added to `requirements.txt` by running `$ pip3 freeze > requirements.txt` when the virtual environment is activated.

#### MongoDB Data Source
* At the top-level of `API/` within your cloned repository, create a directory called `data` and a sub-directory called `db`. If done correctly, the path should be `API/data/db`. This is the location where data stored in Mongo during development and testing will exist.

#### Mongo Config File
* Create a file in the top-level of `API/` called `mongo_config.json`. Add the following contents to the file:
```
{
    "development": {
        "host": "127.0.0.1:27017",
        "db": "main"
    },
    "testing": {
        "host": "127.0.0.1:27017",
        "db": "test"
    }
}
```
* This file will already be under the `.gitignore` and is used for connecting from the API to Mongo during development and automated tests

#### Jenkins Config File
* Create a file in the top-level of `API/` called `jenkins_config.json`. Add the following contents to the file:
```
{
    "url": "http://jenkins-testvirtuallab.centralus.cloudapp.azure.com",
    "username": "YOUR USERNAME",
    "password": "YOUR PASSWORD"
}
```
* This file will already be under the `.gitignore` and is used for connecting from the API to Jenkins during development

### Running
* Activate your virtual environment
* Start your local MongoDB instance with the command `$ mongod --dbpath data/db`
* Start the API with the command `$ export FLASK_ENV=development && python3 server.py`

### Automated Tests
* Activate your virtual environment
* Start your local MongoDB instance with the command `$ mongod --dbpath data/db`
* Run `$ python3 -m unittest` from the top-level API directory

### Testing with Webhooks
* Install [ngrok](https://ngrok.com/)
* Follow the `Running` section above to get your API up and running.
* In a different terminal window, run `./ngrok http 5000`. This opens up your computer to the internet through ngrok and forwards traffic to `localhost:5000`. Copy the public ngrok URL outputted from running the command.
* Go to your desired repository on Github and click on the `Settings` tab. Click on `Webhooks`, then select `Add Webhook`.
* Paste the public ngrok URL that you copied in the previous step into the `Payload URL` field. 
* Change the `Content type` to `application/json`
* Then click `Add webhook`
* The webhook should now be properly set up to trigger and forward to your local API when you push to the repository. A webhook can be re-triggered by clicking on a `Recent Delivery` and selecting `Redeliver`

### Accessing Jenkins
* Our Jenkins server is hosted [here](http://jenkins-testvirtuallab.centralus.cloudapp.azure.com/). 
* In order to access the parts of Jenkins that require authentication, such as job configurations, run the command `$ ssh -L 127.0.0.1:8080:localhost:8080 USERNAME@jenkins-testvirtuallab.centralus.cloudapp.azure.com` to establish an ssh connection with the Jenkins server. Replace `USERNAME` with your username on the Jenkins server, and you will be prompted to enter your password.
* Once the ssh connection is established, you will be able to access the Jenkins instance at `http://localhost:8080` in your web browser.

### Deployment
Production deployment and configurations are not yet created. Eventually, the API will be deployed on Azure using docker machine and docker compose for containerization.
