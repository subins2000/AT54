# AT54 Notifier Bot

* Change config in `bot.py`
* Run server & bot :

```
nohup python bot.py && nohup python server.py
```

## How To Add Prediction

```
curl --data "model=A&serial_number=AAA&failure_when=2019-06-01%2000:00:00&probability=54" http://127.0.0.1:5000/add
add
```

### Flow

* A daemon running in background on server that checks SMART data with the model
* If found to fail, send request to the web server using `cURL` or something else
* The report gets notified via Telegram and email to the sysadmin