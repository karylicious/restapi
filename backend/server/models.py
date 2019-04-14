from app import db

class Tutorial (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    lessons = db.relationship('Lesson')

    def __init__(self, title):
        self.title = title

class Lesson (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutorial_id = db.Column(db.Integer, db.ForeignKey(
        'tutorial.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)

    def __init__(self, tutorial_id, title, description, link):
        self.tutorial_id = tutorial_id
        self.title = title
        self.description = description
        self.link = link


class Exercise (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploadedfile = db.Column(db.String(100), unique=True, nullable=False)
    exerciseType = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expectedClientEntryPoint = db.Column(db.String(200), nullable=False)
    serverDirectoryNameOnDeployment = db.Column(db.String(200))
    exercisequestions = db.relationship('ExerciseQuestion')

    def __init__(self, uploadedfile, exerciseType, description, expectedClientEntryPoint, serverDirectoryNameOnDeployment):
        self.uploadedfile = uploadedfile
        self.exerciseType = exerciseType
        self.description = description
        self.expectedClientEntryPoint = expectedClientEntryPoint
        self.serverDirectoryNameOnDeployment = serverDirectoryNameOnDeployment


class ExerciseQuestion (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        'exercise.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    expectedOutput = db.Column(db.String(100), nullable=False)
    expectedInvokedMethod = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Float, nullable=False)

    def __init__(self, exercise_id, title, description, expectedInvokedMethod, expectedOutput, points):
        self.exercise_id = exercise_id
        self.title = title
        self.description = description
        self.expectedInvokedMethod = expectedInvokedMethod
        self.expectedOutput = expectedOutput
        self.points = points

class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Session (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    loggedin = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, loggedin):
        self.username = username
        self.loggedin = loggedin
