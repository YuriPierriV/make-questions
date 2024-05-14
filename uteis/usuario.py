from uteis.mydb import db
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
        self.quantidade_forms = None
        self.image = None
        self.participando = None
        self.editor = None
        
        

    def check_permission(self,form_id):
        for participando in self.participando:
            if participando == form_id:
                return True
        for editor in self.editor:
            if editor == form_id:
                return True
        return False

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
        finally:
            mydb.close()

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

    def getUsuario(self, id_session):
        try:
            mydb = db()
            cursor = mydb.cursor()

            cursor.execute("SELECT id, nome, sobrenome, email, celular, senha_hash FROM usuarios WHERE id = %s", (id_session,))
            usuario_tupla = cursor.fetchone()

            if usuario_tupla:
                self.id, self.nome, self.sobrenome, self.email, self.celular, self.senha_hash = usuario_tupla

                cursor.execute("SELECT COUNT(*) FROM forms WHERE usuarios_id = %s", (self.id,))
                self.quantidade_forms = cursor.fetchone()[0]

                cursor.execute("""SELECT images.image_data FROM images JOIN users_images ON images.id = users_images.image_id WHERE users_images.usuario_id = %s""", (self.id,))
                image_data = cursor.fetchone()
                self.image = image_data[0] if image_data else None

                cursor.execute("SELECT forms_id FROM permission WHERE usuarios_id = %s AND permission = 1;", (self.id,))
                self.participando = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT forms_id FROM permission WHERE usuarios_id = %s AND permission = 2;", (self.id,))
                self.editor = [row[0] for row in cursor.fetchall()]
                return True

            else:
                flash("Usuário não encontrado.")
                return False

        except Exception as e:
            print(str(e))

        finally:
            mydb.close()

    def formularios(self):
        from uteis.forms import Forms
        mydb = db()
        cursor = mydb.cursor()

        cursor.execute("SELECT id, usuarios_id, nome, titulo, descricao, created_at FROM forms WHERE usuarios_id = %s", (self.id,))
        forms_tuplas = cursor.fetchall()
        
        

        formularios = []
        for form_tupla in forms_tuplas:
            form = Forms()
            formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))
            form.getForms(formulario['id'])
            form.getLink()
            formularios.append(form)

        return formularios

    def associate_image(self,image_id):
        mydb = db()
        cursor = mydb.cursor()

        try:
            cursor.execute("""
                INSERT INTO users_images (usuario_id, image_id)
                VALUES (%s, %s)
            """, (self.id, image_id))
            image_id = cursor.lastrowid
            self.image = image_id
            mydb.commit()
            return True
        except Exception as err:
            return print(err),False
        finally:
            cursor.close()
            conn.close()