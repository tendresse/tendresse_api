# tendresse_api
rest api of tendresse app   
yeoman used : https://github.com/ColeKettler/generator-flask-api 

PRODUCTION == :  

export APP_CONFIG=production  
export APP_PRODUCTION_DATABASE_URI="postgres://user:password@localhost/tendresse"
export SECRET_KEY="your_secret_key"  

python manage.py dropdb && python manage.py createdb && python manage.py populatedb
