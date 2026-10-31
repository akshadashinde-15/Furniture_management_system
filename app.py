from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)


def get_connect():
    con = psycopg2.connect(
        dbname="furnituredb",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    return con


def create_table():

    con = get_connect()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Furniture (
            Order_ID SERIAL PRIMARY KEY,
            Customer_Name VARCHAR(100),
            Product_Name VARCHAR(100),
            Quantity INTEGER,
            Address VARCHAR(200)
        )
    """)

    con.commit()
    cur.close()
    con.close()


@app.route("/")
def home():
    return redirect("/add")



@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        customer_name = request.form.get("Customer_Name")
        product_name = request.form.get("Product_Name")
        quantity = request.form.get("Quantity")
        address = request.form.get("Address")

        con = get_connect()
        cur = con.cursor()

        cur.execute("""
            INSERT INTO Furniture
            (Customer_Name, Product_Name, Quantity, Address)
            VALUES (%s, %s, %s, %s)
        """, (
            customer_name,
            product_name,
            quantity,
            address
        ))

        con.commit()

        cur.close()
        con.close()

        return redirect("/display")

    return render_template("add.html")



@app.route("/display")
def display():

    con = get_connect()
    cur = con.cursor()

    cur.execute("""
        SELECT * FROM Furniture
        ORDER BY Order_ID
    """)

    furniture = cur.fetchall()

    cur.close()
    con.close()

    return render_template(
        "display.html",
        furniture=furniture
    )



@app.route("/update", methods=["GET", "POST"])
def update():

    if request.method == "POST":

        order_id = request.form.get("Order_ID")
        customer_name = request.form.get("Customer_Name")
        product_name = request.form.get("Product_Name")
        quantity = request.form.get("Quantity")
        address = request.form.get("Address")

        con = get_connect()
        cur = con.cursor()

        cur.execute("""
            UPDATE Furniture
            SET Customer_Name = %s,
                Product_Name = %s,
                Quantity = %s,
                Address = %s
            WHERE Order_ID = %s
        """, (
            customer_name,
            product_name,
            quantity,
            address,
            order_id
        ))

        con.commit()

        cur.close()
        con.close()

        return redirect("/display")

    return render_template("update.html")


# DELETE
@app.route("/delete", methods=["GET", "POST"])
def delete():

    if request.method == "POST":

        order_id = request.form.get("Order_ID")

        con = get_connect()
        cur = con.cursor()

        cur.execute("""
            DELETE FROM Furniture
            WHERE Order_ID = %s
        """, (order_id,))

        con.commit()

        deleted = cur.rowcount

        cur.close()
        con.close()

        if deleted > 0:
            return render_template(
                "delete.html",
                message="Order Deleted Successfully!"
            )
        else:
            return render_template(
                "delete.html",
                message="Order ID Not Found!"
            )

    return render_template("delete.html")


if __name__ == "__main__":

    create_table()

    app.run(debug=True)