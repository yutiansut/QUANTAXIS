# run mongo

service mongod restart

# nohup mongod &


cd ../QUANTAXIS_WEBKIT/backend 
forever start bin/www

cd ../web
forever start build/dev-server.js