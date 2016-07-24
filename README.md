# tendresse_api
rest api of tendresse app   
yeoman used : https://github.com/ColeKettler/generator-flask-api 

PRODUCTION == :  

export APP_CONFIG=production  
export APP_PRODUCTION_DATABASE_URI="postgres://user:password@localhost/tendresse"
export SECRET_KEY="your_secret_key"  
export APNS_CERTIFICATE="your_apple_developer_id"
export GCM_API_KEY="your_google_app_id"


python manage.py dropdb && python manage.py createdb && python manage.py populatedb
