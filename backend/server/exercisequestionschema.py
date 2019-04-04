from app import marshmallow

class ExerciseQuestionSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','exercise_id','title','description', 'expectedOutput', 'points')