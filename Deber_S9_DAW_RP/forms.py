from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email

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

class FormularioRegistro(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres."),
            Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", message="Solo letras y espacios.")
        ]
    )
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo válido."),
            Length(max=120, message="El correo no puede superar los 120 caracteres.")
        ]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=4, max=50, message="La contraseña debe tener entre 4 y 50 caracteres.")
        ]
    )
    submit = SubmitField("Registrarse")

class FormularioLogin(FlaskForm):
    email = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Ingrese un correo válido."),
            Length(max=120, message="El correo no puede superar los 120 caracteres.")
        ]
    )
    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=4, max=50, message="La contraseña debe tener entre 4 y 50 caracteres.")
        ]
    )
    submit = SubmitField("Iniciar sesión")