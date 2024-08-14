import psycopg2 as db
from psycopg2 import sql

class Aluno():
    def __init__(self):
        # Atributos da classe
        self.nome = ''
        self.nota1 = 0
        self.nota2 = 0
        self.media = 0
        self.aprovado = False

    # Método para iniciar a conexão com o banco de dados
    def iniciar(self):
        self.con = db.connect('dbname=alunos user=postgres password=123')

    # Método para cadastrar um aluno
    def cadastrar(self, nome, nota1, nota2):
        try:
            # Iniciar a conexão com o banco de dados
            self.iniciar()
            self.cur = self.con.cursor()

            # Cálculo da média e aprovação
            self.nome = nome
            self.nota1 = nota1
            self.nota2 = nota2
            self.media = (self.nota1 + self.nota2) / 2
            if self.media >= 6:
                self.aprovado = True
            else:
                self.aprovado = False

            # INICIO - Código para ajustar a sequência de IDs (Achei que seria legal =D)
            self.cur.execute("SELECT MAX(id) FROM alunos")
            max_id = self.cur.fetchone()[0]
            missing_id = None

            # Se não há IDs na tabela, configurar a sequência para 1
            if max_id is None:
                self.cur.execute("SELECT SETVAL('alunos_id_seq', 1, false)")
                print("Sequência 'alunos_id_seq' ajustada para 1, pois a tabela está vazia.")

            else:

            # Etapa 2: Encontrar o menor ID faltante
                self.cur.execute("""       
                                SELECT MIN(s.i)
                                FROM GENERATE_SERIES(1, %s) s(i)
                                WHERE NOT EXISTS (SELECT id FROM alunos WHERE id = s.i)
                                """, (max_id,))
                missing_id = self.cur.fetchone()[0]

            # Verifica se há um ID faltante
            if missing_id == 1:
                self.cur.execute("SELECT SETVAL('alunos_id_seq', 1, false)")

            elif missing_id is not None:
                # Ajustar a sequência para o menor ID faltante menos 1
                self.cur.execute("SELECT SETVAL('alunos_id_seq', %s - 1)", (missing_id,))
                print(f"Sequência 'alunos_id_seq' ajustada para {missing_id}.")

            else:
                # Caso contrário, ajustar a sequência para o próximo ID após o maior existente
                self.cur.execute("SELECT SETVAL('alunos_id_seq', %s)", (max_id,))
                print(f"Sequência 'alunos_id_seq' ajustada para {max_id + 1}.")
            # FIM - Código para ajustar a sequência de IDs

            # Inserir os dados na tabela
            self.cur.execute(sql.SQL('''INSERT INTO alunos (nome, nota1, nota2, media, aprovado)
                                VALUES (%s, %s, %s, %s, %s)'''), (self.nome, self.nota1, self.nota2, self.media, self.aprovado))
  
        # Tratamento de exceções
        except db.Error as e:
            print(f"Erro ao inserir dados: {e}")
     
        # Finalização da conexão com o banco de dados
        finally:
            self.cur.close()
            self.con.commit()
            self.con.close()

    # Método para consultar os alunos cadastrados
    def consultar(self):
        try:
            self.iniciar()
            self.cur = self.con.cursor()

            # Consultar os dados da tabela ordenados por ID
            self.cur.execute(sql.SQL('SELECT * FROM alunos ORDER BY id'))
            consulta = self.cur.fetchall()
            return consulta
        
        except db.Error as e:
            print(f"Erro ao consultar dados: {e}")
        
        finally:
            self.cur.close()
            self.con.close()

    # Método para excluir um aluno
    def excluir(self, id):
        try:
            self.iniciar()
            self.cur = self.con.cursor()

            # Excluir o aluno com o ID informado
            self.cur.execute(sql.SQL('DELETE FROM alunos WHERE id = %s'), (id,))

        except db.Error as e:
            print(f"Erro ao excluir dados: {e}")

        finally:
            self.cur.close()
            self.con.commit()
            self.con.close()

    # Método para alterar os dados de um aluno
    def alterar(self, id, nome, nota1, nota2):
        try:
            self.iniciar()
            self.cur = self.con.cursor()

            # Cálculo da média e aprovação
            media = (nota1 + nota2) / 2
            aprovado = True if media >= 6 else False

            # Alterar os dados do aluno com o ID informado
            self.cur.execute(sql.SQL('UPDATE alunos SET nome = %s, nota1 = %s, nota2 = %s, media = %s, aprovado = %s WHERE id = %s'), (nome, nota1, nota2, media, aprovado, id))
      
        except db.Error as e:
            print(f"Erro ao alterar dados: {e}")

        finally:
            self.cur.close()
            self.con.commit()
            self.con.close()


