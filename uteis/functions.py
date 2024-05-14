from uteis.mydb import db
from flask import Flask, render_template, redirect, request, flash, url_for, session, abort
import mysql.connector


def obter_formularios_do_usuario(id_user):
    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, usuarios_id, nome, titulo, descricao, created_at FROM forms WHERE usuarios_id = %s", (id_user,))
    forms_tuplas = meu_cursor.fetchall()

    formularios = []
    for form_tupla in forms_tuplas:
        formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))
        formularios.append(formulario)

    return formularios


def obter_dados_do_formulario(id_forms):
    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, usuarios_id,nome, titulo, descricao, created_at FROM forms WHERE id = %s", (id_forms,))
    form_tupla = meu_cursor.fetchone()

    formulario = None
    if form_tupla:
        formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))

    return formulario

def obter_dados_do_usuario(id_usuario):
    if id_usuario is None:
        return None  # ou uma resposta padrão se o ID do usuário não estiver definido

    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, nome, sobrenome, email, celular FROM usuarios WHERE id = %s", (id_usuario,))
    usuario_tupla = meu_cursor.fetchone()

    usuario = None
    if usuario_tupla:
        usuario = dict(zip(['id', 'nome', 'sobrenome', 'email', 'celular'], usuario_tupla))

    return usuario

def obter_questoes_do_formulario(id_formulario):
    if id_formulario is None:
        return None  # ou uma resposta padrão se o ID do usuário não estiver definido

    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, question_text, question_type, correct_id FROM questions WHERE form_id = %s", (id_formulario,))
    questions_tuplas = meu_cursor.fetchall()

    questions = []
    for question_tupla in questions_tuplas:
        question = dict(zip(['id', 'question_text', 'question_type', 'correct_id'], question_tupla))
        questions.append(question)

    return questions

def save_image_to_db(image_data):
    mydb = db()
    cursor = mydb.cursor()
    try:
        cursor.execute("""
            INSERT INTO images (image_data, description)
            VALUES (%s, %s)
            """, (image_data, 'description'))
        image_id = cursor.lastrowid
        mydb.commit()
        return image_id
    finally:
        cursor.close()
        mydb.close()

def associate_image_question(id_question, image_id):
    mydb = db()
    cursor = mydb.cursor()
    try:
        cursor.execute("""
            INSERT INTO question_images (question_id, image_id)
            VALUES (%s, %s)
        """, (id_question, image_id))
        mydb.commit()
        return True
    except Exception as err:
        print(err)
        return False
    finally:
        cursor.close()
        mydb.close()

def associate_image_user(id_user,image_id):
        mydb = db()
        cursor = mydb.cursor()

        try:
            cursor.execute("""
                INSERT INTO users_images (usuario_id, image_id)
                VALUES (%s, %s)
            """, (id_user, image_id))
            mydb.commit()
            return True
        except Exception as err:
            print(err)
            return False
        finally:
            cursor.close()
            mydb.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}