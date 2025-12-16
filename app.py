from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "farm_secret_key"

# ---------------- GLOBAL DATA ----------------

machines = [
    # -------- TRACTORS --------
    {
        "id": 1,
        "name": "Mahindra 575",
        "category": "Tractor",
        "owner": "Ramesh",
        "price": 1200,
        "location": "5 km away",
        "status": "Available"
    },
    {
        "id": 2,
        "name": "John Deere 5310",
        "category": "Tractor",
        "owner": "Suresh",
        "price": 1500,
        "location": "7 km away",
        "status": "Available"
    },

    # -------- HARVESTERS --------
    {
        "id": 3,
        "name": "Claas Crop Tiger",
        "category": "Harvester",
        "owner": "Mahesh",
        "price": 2500,
        "location": "10 km away",
        "status": "Available"
    },
    {
        "id": 4,
        "name": "Kubota DC-68G",
        "category": "Harvester",
        "owner": "Ravi",
        "price": 2800,
        "location": "12 km away",
        "status": "Available"
    },

    # -------- SPRAYERS --------
    {
        "id": 5,
        "name": "Battery Sprayer",
        "category": "Sprayer",
        "owner": "Anil",
        "price": 600,
        "location": "3 km away",
        "status": "Available"
    },
    {
        "id": 6,
        "name": "Tractor Mounted Sprayer",
        "category": "Sprayer",
        "owner": "Kiran",
        "price": 900,
        "location": "4 km away",
        "status": "Available"
    }
]

bookings = []   # ✅ REQUIRED for owner dashboard

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["role"] = request.form["role"]
        session["mobile"] = request.form["mobile"]

        if session["role"] == "farmer":
            return redirect(url_for("farmer"))
        else:
            return redirect(url_for("owner"))

    return render_template("login.html")

# ---------------- FARMER ----------------
@app.route("/farmer")
def farmer():
    if session.get("role") != "farmer":
        return redirect(url_for("login"))

    return render_template(
        "farmer.html",
        machines=machines,
        name=session["name"]
    )

# ---------------- BOOK MACHINE ----------------
@app.route("/book/<int:machine_id>", methods=["GET", "POST"])
def book(machine_id):
    if session.get("role") != "farmer":
        return redirect(url_for("login"))

    machine = next((m for m in machines if m["id"] == machine_id), None)

    if not machine:
        return "Machine not found"

    if request.method == "POST":
        date = request.form["date"]
        hours = int(request.form["hours"])
        total = hours * machine["price"]

        bookings.append({
            "farmer": session["name"],
            "machine": machine["name"],
            "category": machine["category"],
            "owner": machine["owner"],
            "date": date,
            "hours": hours,
            "total": total,
            "status": "Pending"
        })

        return render_template(
            "confirm.html",
            machine=machine,
            date=date,
            hours=hours,
            total=total,
            name=session["name"]
        )

    return render_template("book.html", machine=machine)

# ---------------- OWNER ----------------
@app.route("/owner")
def owner():
    if session.get("role") != "owner":
        return redirect(url_for("login"))

    owner_bookings = [
        b for b in bookings if b["owner"] == session["name"]
    ]

    return render_template(
        "owner.html",
        name=session["name"],
        bookings=owner_bookings
    )

# ---------------- ADD MACHINE ----------------
@app.route("/add-machine", methods=["POST"])
def add_machine():
    if session.get("role") != "owner":
        return redirect(url_for("login"))

    new_id = len(machines) + 1

    machines.append({
        "id": new_id,
        "name": request.form["name"],
        "category": request.form["category"],
        "owner": session["name"],
        "price": int(request.form["price"]),
        "location": request.form["location"],
        "status": "Available"
    })

    return redirect(url_for("owner"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
