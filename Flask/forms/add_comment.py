from wtforms import Form, StringField, PasswordField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange, Length


# определение формы добавления комментариев с валидацией
class AddCommentForm(Form):
    movie_id = IntegerField('Movie ID', validators=[
        DataRequired(), NumberRange(min=1, message='movie_id должен быть больше 0')
    ])
    text = StringField('Комментарий', [Length(min=1), DataRequired()])
