# Gdax Notify

**ITS NOT A TRADINGBOT!**
This small Tool creates a Windows-Notification on every filled GDax-Order.
It checks every second on all currencies. 


## Requierments
* Windows 10
* Python 3.6 32bit

## How to use
Create a file called 'creds.ini' in the root-directory, not the src-directory.
```
[ACCESS]
passphrase=yourpassphrase
key=yourkey
secret=yoursecret
```
Install and Start:
```
> cd gdax-notify
> c:\python36\Scripts\pip.exe requirements.txt
> c:\python36\python.exe src\main.py
```