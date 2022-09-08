source env/scripts/activate
cd core/ || exit
uvicorn main:app --reload