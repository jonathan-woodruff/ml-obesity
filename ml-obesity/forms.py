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
caecOptions = [(3, "Always"), (2, "Frequently"), (1, "Sometimes"), (0, "No")]
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
  height = DecimalField("Height", validators=[DataRequired(), NumberRange(min=.01, message='You must enter a positive number')])
  heightUnit = SelectField(choices=[('cm', 'cm'), ('in', 'in')])
  submit = SubmitField("Submit")

class WeightForm(FlaskForm):
  weight = DecimalField("Weight", validators=[DataRequired(), NumberRange(min=.01, message='You must enter a positive number')])
  weightUnit = SelectField(choices=[('kg', 'kg'), ('lbs', 'lbs')])
  submit = SubmitField("Submit")

class FamilyForm(FieldsRequiredForm):
  family = RadioField("Family", choices=yesno)
  submit = SubmitField("Submit")

class FAVCForm(FieldsRequiredForm):
  favc = RadioField("FAVC", choices=yesno)
  submit = SubmitField("Submit")

class FCVCForm(FieldsRequiredForm):
  fcvc = RadioField("FCVC", choices=fcvcOptions)
  submit = SubmitField("Submit")

class NCPForm(FieldsRequiredForm):
  ncp = RadioField("NCP", choices=ncpOptions)
  submit = SubmitField("Submit")

class CAECForm(FieldsRequiredForm):
  caec = RadioField("CAEC", choices=caecOptions)
  submit = SubmitField("Submit")

class SmokeForm(FieldsRequiredForm):
  smoke = RadioField("SMOKE", choices=yesno)
  submit = SubmitField("Submit")

class CH2OForm(FieldsRequiredForm):
  ch2o = RadioField("CH2O", choices=ch2oOptions)
  submit = SubmitField("Submit")

class SCCForm(FieldsRequiredForm):
  scc = RadioField("SCC", choices=yesno)
  submit = SubmitField("Submit")

class FAFForm(FieldsRequiredForm):
  faf = RadioField("FAF", choices=fafOptions)
  submit = SubmitField("Submit")

class TUEForm(FieldsRequiredForm):
  tue = RadioField("TUE", choices=tueOptions)
  submit = SubmitField("Submit")

class CALCForm(FieldsRequiredForm):
  calc = RadioField("CALC", choices=calcOptions)
  submit = SubmitField("Submit")

class MTRANSForm(FieldsRequiredForm):
  mtrans = RadioField("MTRANS", choices=mtransOptions)
  submit = SubmitField("Submit")