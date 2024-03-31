from uteis.connection import db
from flask import session,flash
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:

    def __init__(self,nome = None,sobrenome = None,email = None,celular = None,senha_hash = None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.celular = celular
        self.senha_hash = senha_hash
        self.id = None
        
        

        

    def cadastra(self):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (self.email,))
            resultado = cursor.fetchone()

            if resultado:
                flash("Este email já está cadastrado. Por favor, escolha outro ou faça login.","cadastro")
                return False  

            cursor.execute("INSERT INTO usuarios (nome, sobrenome, email, celular, senha_hash) VALUES (%s, %s, %s, %s, %s)",
                               (self.nome, self.sobrenome, self.email, self.celular, self.senha_hash))  

            mydb.commit()

            
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (self.email,))
            user_id = cursor.fetchone()[0]

            self.id = user_id  # Atribui o ID ao objeto Usuario
            session["user_id"] = user_id

            flash("Cadastro realizado com sucesso!","cadastro")
            return True  

        except Exception as e:
            flash(str(e))
            return False  # Retorna False se houver algum erro durante o cadastro

    def login(self,email,senha):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            id = cursor.fetchone()
            usuario = Usuario()
            usuario.getUsuario(id[0])
            print(usuario.senha_hash)
            if check_password_hash(usuario.senha_hash, senha):
                
                session["user_id"] = usuario.id
                return True
            else:
                flash("Email ou senha incorreto","login")
                return False

        except Exception as e:
            flash(str(e))
            return False

    def getUsuario(self,id_sesson):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id, nome, sobrenome, email, celular, senha_hash FROM usuarios WHERE id = %s", (id_sesson,))
            usuario_tupla = cursor.fetchone()
            

            if usuario_tupla:
                self.nome = usuario_tupla[1]
                self.sobrenome = usuario_tupla[2]
                self.email = usuario_tupla[3]
                self.celular = usuario_tupla[4]
                self.senha_hash = usuario_tupla[5]
                self.id = usuario_tupla[0]
                return True
            else:
                flash("Usuário não encontrado.")
                return False

        except Exception as e:
            print(str(e))

        finally:
            mydb.close()

    def formularios(self):
        mydb = db()
        cursor = mydb.cursor()

        cursor.execute("SELECT id, usuarios_id, nome, titulo, descricao, created_at FROM forms WHERE usuarios_id = %s", (self.id,))
        forms_tuplas = cursor.fetchall()

        formularios = []
        for form_tupla in forms_tuplas:
            formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))
            formularios.append(formulario)

        return formularios