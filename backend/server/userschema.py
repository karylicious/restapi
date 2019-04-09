from app import marshmallow

class UserSchema(marshmallow.Schema):
    class Meta:
        fields = ('id','username','password')