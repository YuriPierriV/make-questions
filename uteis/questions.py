from uteis.connection import db
from flask import session,flash
from uteis.forms import Forms

class Questions:
    def __init__(self):
        self.id = None
        self.form_id = None
        self.text = 'Pergunta sem título'
        self.type = 'texto'
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
        
