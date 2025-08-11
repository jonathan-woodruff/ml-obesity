from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class FieldsRequiredForm(FlaskForm):
  """Require radio fields to have content. This works around the bug that WTForms radio fields don't honor the `DataRequired` or `InputRequired` validators."""
  class Meta:
    def render_field(self, field, render_kw):
      if field.type == "_Option":
        render_kw.setdefault("required", True)
      return super().render_field(field, render_kw)

genderOptions = [("female","Female"), ("male", "Male")]

## Create Form Here
class Gender(FieldsRequiredForm):
  category = RadioField("Gender", choices=genderOptions)
  submit = SubmitField("Submit")