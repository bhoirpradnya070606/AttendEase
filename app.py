from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "attendance.db")

def db():
    c=sqlite3.connect(DB_PATH)
    c.row_factory=sqlite3.Row
    return c

def init_db():
    c=db()
    c.execute("""CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL, subject TEXT NOT NULL,
        total_classes INTEGER NOT NULL, attended_classes INTEGER NOT NULL,
        percentage REAL NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.commit(); c.close()

@app.route("/")
def index():
    c=db()
    records=c.execute("SELECT * FROM attendance ORDER BY id DESC").fetchall()
    c.close()
    total=sum(int(r["total_classes"]) for r in records)
    attended=sum(int(r["attended_classes"]) for r in records)
    return render_template("index.html", records=records, total_classes=total,
        attended_classes=attended, absent_classes=total-attended,
        overall_percentage=round(attended/total*100,2) if total else 0)

@app.route("/add", methods=["POST"])
def add_attendance():
    name=request.form.get("student_name","").strip()
    subject=request.form.get("subject","").strip()
    tv=request.form.get("total_classes","").strip()
    av=request.form.get("attended_classes","").strip()
    if not name: return "Student name is required."
    if not subject: return "Please select a subject."
    try: total,attended=int(tv),int(av)
    except ValueError: return "Classes must be numbers."
    if total<=0: return "Total classes must be greater than 0."
    if attended<0: return "Attended classes cannot be negative."
    if attended>total: return "Attended classes cannot be greater than total classes."
    c=db()
    c.execute("INSERT INTO attendance(student_name,subject,total_classes,attended_classes,percentage) VALUES(?,?,?,?,?)",
              (name,subject,total,attended,attended/total*100))
    c.commit(); c.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_attendance(record_id):
    c=db(); c.execute("DELETE FROM attendance WHERE id=?",(record_id,)); c.commit(); c.close()
    return redirect(url_for("index"))

init_db()

if __name__=="__main__":
    app.run(debug=True)
