from app import marshmallow

class TutorialSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','title')