import psycopg2

try:
    conn = psycopg2.connect(
        dbname='db_smartschool_j3jo',
        user='user_smartschool',
        password='RJhIzuVGFhBqgKmZCiVNVoE6utlNxApn',
        host='dpg-d1rd3t3e5dus73dipuj0-a.oregon-postgres.render.com',
        port='5432'
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:")
    print(e)
