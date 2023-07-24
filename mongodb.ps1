Start-Process mongod "--config mongodb.conf" -NoNewWindow

Get-Content ./.mongo/logs/mongo.log -Wait -Tail 30