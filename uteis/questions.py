from uteis.mydb import db
from flask import session,flash


class Questions:
    def __init__(self,id=None,form_id=None,text='Pergunta sem título',type='text',correct = None,pre_answer='Resposta',required=0):
        self.id = id
        self.form_id = form_id
        self.text = text
        self.type = type
        self.correct = None
        self.pre_answer = pre_answer
        self.options = []
        self.required = required
        self.image = None

    def cria_question(self,forms):
        try:
            
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("INSERT INTO questions (form_id, question_text, question_type, correct_id,pre_answer,required) VALUES (%s,%s, %s, %s,%s,%s)",
                           (forms.id,self.text, self.type, None,self.pre_answer,self.required))
            
            
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

            cursor.execute("SELECT id, question_text, question_type, correct_id ,pre_answer,required FROM questions WHERE form_id = %s", (form_id,))
            questions_tuplas = cursor.fetchall()

            questions = []
            for question_tupla in questions_tuplas:
                question = dict(zip(['id', 'question_text', 'question_type', 'correct_id','pre_answer','required'], question_tupla))
                questions.append(question)

            
            mydb.commit()
            mydb.close()

            return questions
        except Exception as e:
            print(e)

    def get_question_obj(self,id_formulario):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id, question_text, question_type, correct_id ,pre_answer,required FROM questions WHERE form_id = %s", (id_formulario,))
            questions_tuplas = cursor.fetchall()

            if questions_tuplas:
                self.id = questions_tuplas[0]
                self.text = questions_tuplas[1]
                self.type = questions_tuplas[2]
                self.correct = questions_tuplas[3]
                self.pre_answer = questions_tuplas[4]
                self.required = questions_tuplas[5]
                self.form_id = id_formulario

            
            mydb.commit()
            mydb.close()

            return True
        except Exception as e:
            print(e)
            return False

    def get_options(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id, option_text, question_id FROM options WHERE question_id = %s", (self.id,))
            options_tuplas = cursor.fetchall()

            for options_tupla in options_tuplas:
                option = dict(zip(['id', 'option_text', 'question_id'], options_tupla))
                self.options.append(option)

            mydb.commit()
            mydb.close()
            return True
        except Exception:
            return False    

    def cria_options_padrao(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            sql = "INSERT INTO options (`option_text`, `question_id`) VALUES (%s, %s)"
            values = [('Opção 1', self.id), ('Opção 2', self.id)]

            cursor.executemany(sql, values)

            mydb.commit()
            mydb.close()
            return True
        except Exception as e:
            print(e)
            return False

    def remove_options(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            
            sql = "DELETE FROM options WHERE question_id = %s"
            
            values = (self.id,)

            
            cursor.execute(sql, values)

            
            mydb.commit()
            mydb.close()
            return True
        except Exception as e:
            print(e)
            return False


    def cria_options_text(self,novoValor):
        try:
            mydb = db()
            cursor = mydb.cursor()

            sql = "INSERT INTO options (`option_text`, `question_id`) VALUES (%s, %s)"
            values = (novoValor,self.id)

            
            cursor.execute(sql, values)

            mydb.commit()
            mydb.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_image(self):

        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("""SELECT images.id FROM images JOIN question_images ON images.id = question_images.image_id WHERE question_images.question_id = %s""", (self.id,))
            lista = cursor.fetchall()
            self.image = lista[-1]

            

            mydb.commit()
            mydb.close()
            return True
        except Exception as e:
            print(e)
            return False

        


    