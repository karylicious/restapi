from app import marshmallow

class ExerciseSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','name', 'uploadedfile')