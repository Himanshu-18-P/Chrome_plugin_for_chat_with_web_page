import os
from groq import Groq 
import asyncio
from dotenv import load_dotenv
from core.prompt.prompt import *
import logging
from flask import jsonify

load_dotenv('.env.secrets')


class GroqAIProcessor:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

    def run_completion(self,user_input ,context):
        resp = self.client.chat.completions.create(
            messages=[
                {
                 "role": "system",
                 "content": f'guidlines: {prompt_for_response} , context_of_answer : {context}'
                },

            {
                "role": "user",
                "content": user_input,
            }
            ],
                model= "llama-3.3-70b-versatile"  ,
                temperature = 0.0,
                top_p = 1,
                max_tokens = 1024
            )

        return resp.choices[0].message.content
    
    def process_text(self , user_text  ,  context):
        try:
            if user_text == '':
                return "please repeat your question"
            
            res = self.run_completion(user_text, context)
            return res 
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    process = GroqAIProcessor()
    print(asyncio.run(process.process_text('hello how are you')))