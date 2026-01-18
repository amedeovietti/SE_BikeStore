from MySQLdb._mysql import result
from model.categorie import Categoria
from database.DB_connect import DBConnect

class DAO:

    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)
        for row in cursor:
            results.append(row["order_date"])
        first = results[0]
        last = results[-1]
        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def leggiDateFiltrate(category_id):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.id AS product_id, o.order_date
                    FROM product p
                    JOIN order_item i ON i.product_id = p.id
                    JOIN `order` o ON o.id = i.order_id
                    WHERE p.category_id = %s """
        cursor.execute(query, (category_id,))
        for row in cursor:
            result.append(row)
        last = max(d["order_date"] for d in result)
        first = min(d["order_date"] for d in result)
        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def leggiCategorie():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, category_name
                    FROM category """
        cursor.execute(query)
        for row in cursor:
            r = Categoria(row["id"], row["category_name"])
            result.append(r)
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def cercaProdotti(category_id):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id
                    FROM product p
                    WHERE p.category_id = %s """
        cursor.execute(query, (category_id,))
        for row in cursor:
            result.append(row["id"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def cercaOrdini(p):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT o.order_id
                    FROM order_item o
                    WHERE o.product_id = %s """
        cursor.execute(query, (p,))
        for row in cursor:
            result.append(row["order_id"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def cercaVendita(o, data_inizio, data_fine):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT COUNT(*)
                    FROM `order` o
                    WHERE o.id = %s 
                      AND o.order_date BETWEEN %s AND %s """
        cursor.execute(query, (o, data_inizio, data_fine))
        for row in cursor:
            result.append(row["COUNT(*)"])
        cursor.close()
        conn.close()
        return result[0]