export API_CONFIG="config.json"
export FLASK_DEBUG=true
PORT=8001
export FLASK_APP="wine_predictor_api:create_app"

lsof -t -i:$PORT | xargs kill -9
python -m flask run -h 0.0.0.0 -p $PORT
