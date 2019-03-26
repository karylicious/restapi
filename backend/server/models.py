from app import db


class Tutorial (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name, level):
        self.name = name
        self.level = level


class Exercise (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    uploadedfile = db.Column(db.String(100), unique=True, nullable=False)
    exercisetype = db.Column(db.String(20), nullable=False)
    exercisequestions = db.relationship('ExerciseQuestion')

    def __init__(self, name, uploadedfile, exercisetype):
        self.name = name
        self.uploadedfile = uploadedfile
        self.exercisetype = exercisetype


class ExerciseQuestion (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        'exercise.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    #exercise = db.relationship('Exercise', back_populates = 'exercise')

    def __init__(self, exercise_id, title, description):
        self.exercise_id = exercise_id
        self.title = title
        self.description = description

    # def alreadyExists(self, name, level):
