from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s
                    order by s.name"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getStatiAnno(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.* from sighting s, state st where s.state = st.id and year(s.`datetime`) = %s order by st.Name asc """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodi(anno, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * from sighting s where s.state = %s and year(s.`datetime`) = %s"""
            cursor.execute(query, (stato, anno,))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    def getSightingShape(map, anno, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as sig1, s2.id as sig2 from sighting s, sighting s2 where s.shape = s2.shape and s.id < s2.id and s.state = %s and year(s.`datetime`) = %s
                        and s.state = s2.state and year(s.`datetime`) = year(s2.`datetime`)"""
            cursor.execute(query, (stato, anno,))

            for row in cursor:
                sigh1 = map[row['sig1']]
                sigh2 = map[row['sig2']]
                result.append((sigh1, sigh2))
            cursor.close()
            cnx.close()
        return result

