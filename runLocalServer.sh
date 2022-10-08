source env/scripts/activate
cd core/ || exit
uvicorn main:app --port 8008 --reload
echo "Starting server on port 8008"
