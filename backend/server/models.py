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
    expectedClientEntryPoint = db.Column(db.String(200), unique=True, nullable=False)
    serverDirectoryNameOnDeployment = db.Column(db.String(200), nullable=False)
    exercisequestions = db.relationship('ExerciseQuestion')

    def __init__(self, name, uploadedfile, exercisetype, expectedClientEntryPoint, serverDirectoryNameOnDeployment):
        self.name = name
        self.uploadedfile = uploadedfile
        self.exercisetype = exercisetype
        self.expectedClientEntryPoint = expectedClientEntryPoint
        self.serverDirectoryNameOnDeployment = serverDirectoryNameOnDeployment


class ExerciseQuestion (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        'exercise.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expectedOutput = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Float, nullable=False)

    def __init__(self, exercise_id, title, description, expectedOutput, points):
        self.exercise_id = exercise_id
        self.title = title
        self.description = description
        self.expectedOutput = expectedOutput
        self.points = points

