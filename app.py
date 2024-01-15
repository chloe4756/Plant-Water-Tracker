from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    watering_interval = db.Column(db.Integer, nullable=False, default=7)
    dates = db.relationship('WateringDate', backref='plant', lazy=True)
    plant_type = db.Column(db.String(10), nullable=False, default='indoor')
    def next_watering_date(self):
        if self.dates:
            last_watering_date = max(date.date for date in self.dates)
            return last_watering_date + timedelta(days=self.watering_interval)
        return "Not available"

class WateringDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    plants = Plant.query.all()
    return render_template('index.html', plants=plants)



@app.route('/create_plant', methods=['GET', 'POST'])
def create_plant():
    if request.method == 'POST':
        plant_name = request.form['name']
        watering_interval = int(request.form['water'])
        plant_type = request.form['plant_type']  
        plant = Plant(name=plant_name, watering_interval=watering_interval, plant_type=plant_type)
        db.session.add(plant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_plant.html')

@app.route('/delete_plant/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    plant_to_delete = Plant.query.get_or_404(plant_id)

    WateringDate.query.filter_by(plant_id=plant_id).delete()

    db.session.delete(plant_to_delete)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_watering_date/<int:watering_date_id>', methods=['POST'])
def delete_watering_date(watering_date_id):
    watering_date_to_delete = WateringDate.query.get_or_404(watering_date_id)
    
    plant_id = watering_date_to_delete.plant_id
    db.session.delete(watering_date_to_delete)
    db.session.commit()
    return redirect(url_for('view_plant', plant_id=plant_id))


@app.route('/add_date/<int:plant_id>', methods=['GET', 'POST'])
def add_date(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    if request.method == 'POST':
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        existing_date = WateringDate.query.filter_by(plant_id=plant.id, date=date).first()
        if existing_date is None: 
            watering_date = WateringDate(date=date, plant=plant)
            db.session.add(watering_date)
            db.session.commit()
        return redirect(url_for('view_plant', plant_id=plant.id))
    return render_template('add_date.html', plant=plant)

@app.route('/view_plant/<int:plant_id>')
def view_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    next_recommended_date = plant.next_watering_date()
    return render_template('plant_details.html', plant=plant, next_recommended_date=next_recommended_date)



@app.route('/add_date_to_all', methods=['POST'])
def add_date_to_all():
    if request.method == 'POST':
        date = datetime.today().date()
        outdoor_plants = Plant.query.filter_by(plant_type='outdoor').all()

        added_count = 0

        for plant in outdoor_plants:
            existing_date = WateringDate.query.filter_by(plant_id=plant.id, date=date).first()

            if existing_date is None:
                watering_date = WateringDate(date=date, plant=plant)
                db.session.add(watering_date)
                added_count += 1
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

