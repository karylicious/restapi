from app import marshmallow

class LessonSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','tutorial_id','title','description', 'link')