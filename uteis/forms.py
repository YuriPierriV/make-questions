from uteis.mydb import db
from flask import session,flash
from uteis.questions import Questions


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


    def getForms(self,id_forms):
        try:
            mydb = db()
            meu_cursor = mydb.cursor()

            meu_cursor.execute("SELECT id, usuarios_id,nome, titulo, descricao, created_at FROM forms WHERE id = %s", (id_forms,))
            form_tupla = meu_cursor.fetchone()

            
            if form_tupla:
                self.id = form_tupla[0]
                self.usuarios_id = form_tupla[1]
                self.nome = form_tupla[2]
                self.titulo = form_tupla[3]
                self.descricao = form_tupla[4]
                return True

        except Exception as e:
            print(e)
            return False

    def get_questions(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id,form_id, question_text, question_type, correct_id, pre_answer FROM questions WHERE form_id = %s", (self.id,))
            questions_tuplas = cursor.fetchall()
            questions = []
            for question_tupla in questions_tuplas:
                question = Questions(question_tupla[0],question_tupla[1],question_tupla[2],question_tupla[3],question_tupla[4],question_tupla[5])
                questions.append(question)

            mydb.commit()
            mydb.close()

            return questions
        except Exception as e:
            print(e)
        

    def get_questions_json(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id,form_id, question_text, question_type, correct_id, pre_answer FROM questions WHERE form_id = %s", (self.id,))
            questions_tuplas = cursor.fetchall()
            questions = []
            for question_tupla in questions_tuplas:
                question = dict(zip(['id','form_id' 'question_text', 'question_type', 'correct_id','pre_answer'], question_tupla))
                questions.append(question)

            mydb.commit()
            mydb.close()

            return questions
        except Exception as e:
            print(e)

    #Não faz sentido usar
    def att_forms(self,parametro,new):
        try:
            mydb = db()
            cursor = mydb.cursor()

            # Atualize o campo no banco de dados
            cursor.execute(f"UPDATE forms SET {parametro} = %s WHERE id = %s", (new, self.id))

            # Commit e feche a conexão
            mydb.commit()
            mydb.close()

            return f"Campo {nome_param} do formulário atualizado com sucesso."

        except mysql.connector.Error as err:
            print(f"Erro no MySQL: {err}")
            return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."