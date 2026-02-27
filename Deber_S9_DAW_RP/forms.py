from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class FormularioNombre(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=20, message="El nombre debe tener entre 3 y 20 caracteres."),
            Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", message="Solo letras y espacios.")
        ]
    )
    submit = SubmitField("Enviar")