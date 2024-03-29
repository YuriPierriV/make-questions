from uteis.connection import db
from flask import session,flash

class Forms:
    
    def __init__(self):
        self.id = None
        self.user_id = session.get('user_id')
        self.nome = 'Formulário sem Nome'
        self.titulo = 'Formulário sem Titulo'
        self.descricao = 'Descrição'
        
        
    def cria_form(self):
        try:
            mydb = db()
            cursor = mydb.cursor()
            # Insira o novo formulário na tabela forms
            cursor.execute("INSERT INTO forms (usuarios_id, nome, titulo, descricao) VALUES (%s,%s, %s, %s)",
                            (self.user_id,self.nome, self.titulo, self.descricao))
            self.id = cursor.lastrowid
            mydb.commit()
            mydb.close()

            return True
        except Exception as e:
            flash(str(e))
            return False


    #testar
    def questoes(self):
        mydb = db()
        cursor = mydb.cursor()

        cursor.execute("SELECT form_id, question_text, question_type, correct_id FROM questions WHERE form_id = %s", (self.id,))
        questions_tuplas = cursor.fetchall()

        questions = []
        for form_tupla in forms_tuplas:
            question = dict(zip(['form_id', 'question_text','question_type', 'correct_id'], form_tupla))
            questions.append(question)

        return formularios
        