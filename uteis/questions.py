from uteis.connection import db
from flask import session,flash


class Questions:
    def __init__(self,id=None,form_id=None,text='Pergunta sem título',type='texto',correct = None):
        self.id = id
        self.form_id = form_id
        self.text = text
        self.type = type
        self.correct = None

    def cria_question(self,forms):
        try:
            
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("INSERT INTO questions (form_id, question_text, question_type, correct_id) VALUES (%s,%s, %s, %s)",
                           (forms.id,self.text, self.type, None))
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
                question = Questions(question_tupla[0],question_tupla[1],question_tupla[2],question_tupla[3])
                questions.append(question)


            mydb.commit()
            mydb.close()

            return questions
        except Exception as e:
            print(e)

