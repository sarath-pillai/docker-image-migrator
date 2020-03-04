# Migrate Docker images from one registry to another (WIP)

Note: This is only tested against a source insecure registry running on port 80 and an authenticated target registry.

## Assumptions
1. Source registry and destination registry authentication is configured on the system from where you fire this.
2. Source registry is HTTP(insecure)

## How to execute

The very first step is to install python packages from requirements.txt as shown below. 
```
pip install -r requirements.txt
```

The second step is to run the migrator as shown below. 

```
python migrate.py --source-reg myregistry.example.net --destination-reg mytargetregistry.example.net
```
