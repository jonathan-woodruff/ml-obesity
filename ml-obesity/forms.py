from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField, DecimalField, SelectField
from wtforms.validators import InputRequired, DataRequired, NumberRange

class FieldsRequiredForm(FlaskForm):
  """Require radio fields to have content. This works around the bug that WTForms radio fields don't honor the `DataRequired` or `InputRequired` validators."""
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)

genderOptions = [(0, "Female"), (1, "Male")]
yesno = [(1, "Yes"), (0, "No")]
fcvcOptions = [(3, "Always"), (2, "Sometimes"), (1, "Never")]
ncpOptions = [(1, "Between one and two meals"), (3, "Three meals"), (4, "More than three meals")]
caecOptions = [(4, "Always"), (3, "Frequently"), (1, "Sometimes"), (0, "No")]
ch2oOptions = [(1, "Less than a liter"), (2, "Between one and two liters"), (3, "More than two liters")]
fafOptions = [(3, "4 or 5 days"), (2, "2 or 4 days"), (1, "1 or 2 days"), (0, "I do not have")]
tueOptions = [(0, "0 - 1 hours"), (1, "2 - 5 hours"), (2, "more than 5 hours")]
calcOptions = [(3, "Always"), (2, "Frequently"), (1, "Sometimes"), (0, "I do not drink")]
mtransOptions = [(0, "Automobile"), (2, "Motorbike"), (1, "Bike"), (3, "Public Transportation"), (4, "Walking")]

class GenderForm(FieldsRequiredForm):
  gender = RadioField("Gender", choices=genderOptions)
  submit = SubmitField("Submit")

class AgeForm(FlaskForm):
  age = IntegerField("age", validators=[DataRequired(), NumberRange(min=14, message='You must be at least 14 years old')])
  submit = SubmitField("Submit")

class HeightForm(FlaskForm):
  height = DecimalField("Height", validators=[DataRequired(), NumberRange(min=1, message='You must enter a positive number')])
  heightUnit = SelectField(choices=[('cm', 'cm'), ('in', 'in')])
  submit = SubmitField("Submit")

class WeightForm(FlaskForm):
  weight = DecimalField("Weight", validators=[DataRequired(), NumberRange(min=1, message='You must enter a positive number')])
  weightUnit = SelectField(choices=[('kg', 'kg'), ('lbs', 'lbs')])
  submit = SubmitField("Submit")
  
  """
  family = RadioField("Family", choices=yesno)
  favc = RadioField("FAVC", choices=yesno)
  fcvc = RadioField("FCVC", choices=fcvcOptions)
  ncp = RadioField("NCP", choices=ncpOptions)
  caec = RadioField("CAEC", choices=caecOptions)
  smoke = RadioField("SMOKE", choices=yesno)
  ch2o = RadioField("CH2O", choices=ch2oOptions)
  scc = RadioField("SCC", choices=yesno)
  faf = RadioField("FAF", choices=fafOptions)
  tue = RadioField("TUE", choices=tueOptions)
  calc = RadioField("CALC", choices=calcOptions)
  mtrans = RadioField("MTRANS", choices=mtransOptions)
  submit = SubmitField("Submit")
  """