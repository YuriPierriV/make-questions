from uteis.mydb import db
from flask import session,flash


class Questions:
    def __init__(self,id=None,form_id=None,text='Pergunta sem título',type='texto',correct = None,pre_answer='Resposta'):
        self.id = id
        self.form_id = form_id
        self.text = text
        self.type = type
        self.correct = None
        self.pre_answer = pre_answer

    def cria_question(self,forms):
        try:
            
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("INSERT INTO questions (form_id, question_text, question_type, correct_id,pre_answer) VALUES (%s,%s, %s, %s,%s)",
                           (forms.id,self.text, self.type, None,self.pre_answer))
            # Commit e feche a conexão
            mydb.commit()
            mydb.close()
            return True
        except Exception as e:
            flash(str(e))
            return False
        
    def get_questions(self,form_id):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id, question_text, question_type, correct_id FROM questions WHERE form_id = %s", (id_formulario,))
            questions_tuplas = cursor.fetchall()

            questions = []
            for question_tupla in questions_tuplas:
                question = dict(zip(['id', 'question_text', 'question_type', 'correct_id'], question_tupla))
                questions.append(question)


            mydb.commit()
            mydb.close()

            return questions
        except Exception as e:
            print(e)