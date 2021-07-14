from flask import Flask, render_template, jsonify
import psycopg2
import urllib.request
import json
from data import Articles

app = Flask(__name__)

Articles_return = Articles()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/ping')
def ping():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route('/select')
def select():
    connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                  host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    cursor = connection.cursor()
    select_query = """ SELECT * FROM characters"""
    cursor.execute(select_query)
    records = cursor.fetchall()
    if records is not None:
        return "OK"
    connection.close()
    cursor.close()


@app.route('/create')
def create_table():
    try:
        connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
                                      host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    except psycopg2.Error as e:
        resp = jsonify(success=False, error=e)
        resp.status_code = 500
        return resp
    cursor = connection.cursor()

    create_table_query = (
        "CREATE TABLE characters ( id SERIAL, name character varying, gender character varying,homeworld character varying);")
    try:
        cursor.execute(create_table_query)
        connection.commit()
        connection.close()
        cursor.close()
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    except psycopg2.Error as e:
        resp = jsonify(success=False, reason=e.pgerror)
        resp.status_code = 500
        return resp


@app.route('/test')
def articles():
    return render_template('articles.html', articles=Articles_return)


@app.route('/insert')
def insert_func():
    #    try:
    #        connection = psycopg2.connect(dbname='postgres', user='varkhipov@varkhipovazurepgsqlsrv', password='H@Sh1CoR3!',
    #                                      host='varkhipovazurepgsqlsrv.postgres.database.azure.com')
    #    except psycopg2.Error as e:
    #        resp = jsonify(success=False, error=e)
    #        resp.status_code = 500
    #        return resp
    #    cursor = connection.cursor()
    api_url_response = urllib.request.urlopen('https://swapi.dev/api/people/')
    api_url_response_page = api_url_response.read().decode('utf-8')
    parsed_page = json.loads(api_url_response_page)
    #    for i in range(0, len(parsed_page['results'])):
    #        homeworld_url = (parsed_page['results'][i]['homeworld'])
    #        api_url_response = urllib.request.urlopen(homeworld_url)
    #        api_url_response_page = api_url_response.read().decode('utf-8')
    #        parsed_page_homeworld = json.loads(api_url_response_page)
    #        insert_query = """ INSERT INTO characters (name, gender,homeworld) VALUES (%s,%s,%s)"""
    #        values_to_insert = (
    #            parsed_page['results'][i]['name'], parsed_page['results'][i]['gender'], parsed_page_homeworld['name'])
    #        cursor.execute(insert_query, values_to_insert)
    #        connection.commit()
    #        connection.close()
    #        cursor.close()
    #        resp = jsonify(success=True)
    #        resp.status_code = 200
    return parsed_page


if __name__ == '__main__':
    app.run()
