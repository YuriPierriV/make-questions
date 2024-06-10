from uteis.mydb import db
from flask import session,flash
from uteis.forms import Forms
from datetime import datetime, timedelta
from uteis.forms import Forms

class Answer:

    def __init__(self,id=None,question_id=None,user_id=None,text=None,selected_id=None,form_id=None,enviado=0,type_answer = None,time = None):
        self.id = id
        self.question_id = question_id
        self.user_id = user_id
        self.text = text
        self.selected_id = selected_id
        self.form_id = form_id
        self.enviado = enviado
        self.type = type_answer
        self.time = time
        
    def blank(self,form_id,user_id,permission):

        mydb = db()
        cursor = mydb.cursor()

        cursor.execute("INSERT INTO permission (usuarios_id,forms_id,permission) VALUES (%s,%s,%s)", (user_id,form_id,permission))
        resultado = cursor.fetchone()

        mydb.commit()
        mydb.close()
            
        return True  

    def answer_list(self):
        return True
    
    def getAnswer(self,form_id):

            mydb = db()
            cursor = mydb.cursor()

            query = """
            SELECT a.*, q.question_type
            FROM answers a
            JOIN questions q ON a.question_id = q.id
            JOIN forms f ON q.form_id = f.id
            WHERE f.id = %s
            """
            cursor.execute(query, (form_id,))

            resultados = cursor.fetchall()

            mydb.commit()
            mydb.close()
            
            # Criar uma lista de dicionários com os resultados
            respostas = []
            for resultado in resultados:
                resposta = dict(zip([desc[0] for desc in cursor.description], resultado))
                respostas.append(resposta)

            return respostas
            

    def answer_list(self):
        return True