from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.order import Order


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/create_order")
def create():
    if not Order.validate_order(request.form):
        return redirect("/")
    Order.create_order(request.form)
    return redirect("/all_orders")


@app.route("/view_order/<int:id>")
def get_order(id):
    order = Order.get_order({"id": id})
    return render_template("edit_order.html", order=order)


@app.post("/update_order")
def update_order():
    id = request.form["id"]
    if not Order.validate_order(request.form):
        return redirect(f"/view_order/{id}")
    Order.update(request.form)
    return redirect("/all_orders")


@app.route("/all_orders")
def all_orders():
    orders = Order.get_all()
    return render_template("all_orders.html", orders=orders)
