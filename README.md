## PorkCert

Simple script to fetch SSL certs from [Porkbun](https://porkbun.com/) domain registrar

### Description

[Porkbun](https://porkbun.com/) domain registrar automatically provides SSL certificates for domains. Unless you are web hosting through them, these will need to be downloaded every 3 months and updated on your serverThis
- Docker & crontab for setting up auto-downloading job

This repo includes:
* A python script to manually download the SSL cert bundle and store at desired location on server
* A shell script which builds above script as a Docker image and runs regularly as cron job to ensure that SSL certs are up to date

Certs are saved in traditional certbot names rather than default Porkbun names

### Prerequisites
- Ensure you have gotten your API_KEY and API_SECRET_KEY from https://porkbun.com/account/api

### Running the python script to manually download and store certs once
```
$ git clone https://github.com/cjcon90/porkcert.git && cd porkcert
$ python -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt
$ python main.py -d {domain_name} -l {directory_to_save_certs}
```

### Setting cert renewal cron job
```
$ ./install.sh
Enter domain to retrieve SSL certs for: cjcon90.dev
Enter directory to store SSL certs: /var/www/cjcon90/certs
Building porkcert docker image...
Finished building porkcert
Enter value for API_KEY:
Enter value for SECRET_API_KEY:
Do you want to store these keys to $HOME/.config/porkcert/keys.json? [Y/n]:
Installed certs to /var/www/cjcon90/certs
New crontab job created to keep certs updated
```

