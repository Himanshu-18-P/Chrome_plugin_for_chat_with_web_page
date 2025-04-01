from flask import Flask , request , jsonify
from core import *
import os
import shutil

def create_app():

    app = Flask(__name__)

    @app.route('/get_url' , methods = ["POST"])
    def create_db():
        try:
            data = request.get_json()
            url = data.get('url')
            if not url:
                return {"message" : "url is missing please provide one"} , 400 
            
            db_path = start.load_data.craete_fassidb(url , True)

            return jsonify({"db_path" : db_path}) , 200

        except Exception as e:
            return {'message' : f"facing this error {e}"} , 500 


        # extract data create fassidb 

    @app.route('/chat_With_web' , methods = ["POST"])
    def chatbot():
        try:
            data = request.get_json()
            db_path = data.get('db_path')
            question = data.get('question')
            is_exit = data.get('is_exit')
            # Clear the database if is_exit is True
            if db_path:
                db_path = os.path.join("fassi_db", db_path.strip("/"))

            # Clear the database if is_exit is True
            if is_exit:
                if not db_path:
                    return {"message": "db_path is missing, cannot clear database"}, 400

                # Check if the path is a directory inside fassi_db, and remove accordingly
                if os.path.isdir(db_path):
                    shutil.rmtree(db_path)  # Remove the UUID folder inside fassi_db
                    return {"message": "DB cleared (UUID folder removed)"}, 200
                else:
                    return {"message": f"db_path '{db_path}' not found, unable to clear database"}, 404

            # Validate that db_path and question are provided
            if not db_path or not question:
                return {"message": "db_path and question are missing, please provide them"}, 400
            
            # Check if the FAISS database exists
            if not os.path.exists(db_path):
                return {"message": f"Database at '{db_path}' not found"}, 404

            # relevent text
            context = start.load_data.retrive_similer_docs_using_fassi(question , db_path) 
            print(context)
            # llm answer
            res = start.process.process_text(question , context)

            return jsonify({"response" : res}) , 200

        except Exception as e:
            return {'message' : f"facing this error {e}"} , 500 


    return app


if __name__ == '__main__':
    start = Start()
    app = create_app()
    app.run(debug=True)