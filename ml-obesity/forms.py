from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField, DecimalField


class FieldsRequiredForm(FlaskForm):
  """Require radio fields to have content. This works around the bug that WTForms radio fields don't honor the `DataRequired` or `InputRequired` validators."""
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)

genderOptions = [("female","Female"), ("male", "Male")]
yesno = [("yes","Yes"), ("no","No")]
asn = [("always","Always"), ("sometimes","Sometimes"), ("never", "Never")]
ncpOptions = [("one","Between one and two meals"), ("two","Three meals"), ("three","More than three meals")]
afsn = [("always","Always"), ("frequently","Frequently"), ("sometimes","Sometimes"), ("no", "No")]
ch2oOptions = [("one","Less than a liter"), ("two","Between one and two liters"), ("three","More than two liters")]
fafOptions = [("one","4 or 5 days"), ("two","2 or 4 days"), ("three","1 or 2 days"), ("four","I do not have")]

class Obesity(FieldsRequiredForm):
  gender = RadioField("Gender", choices=genderOptions)
  age = IntegerField("Age")
  height = DecimalField("Height")
  weight = DecimalField("Weight")
  family = RadioField("Family", choices=yesno)
  favc = RadioField("FAVC", choices=yesno)
  fcvc = RadioField("FCVC", choices=asn)
  ncp = RadioField("NCP", choices=ncpOptions)
  caec = RadioField("CAEC", choices=afsn)
  smoke = RadioField("SMOKE", choices=yesno)
  ch2o = RadioField("CH2O", choices=ch2oOptions)
  scc = RadioField("SCC", choices=yesno)
  faf = RadioField("FAF", choices=fafOptions)
  submit = SubmitField("Submit")