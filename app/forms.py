from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, SelectField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, ValidationError, NumberRange


class SubmitFile(FlaskForm):
    file = FileField('Upload', validators=[FileAllowed(['xlsx','csv']), FileRequired()])
    analyze = SubmitField('Analyze')
    
class MonthlyEntriesForm(FlaskForm):
    months = SelectField('Month')
    check = SubmitField('Check')
    
class UnbalancedEntriesForm(FlaskForm):
    transaction = SelectField('Transaction Type')
    check = SubmitField('Check')
    
class WeekendEntriesForm(FlaskForm):
    weekend = SelectField('Weekend')
    check = SubmitField('Check')
    
class HighDollarEntriesForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    check = SubmitField('Check')
    
class SampleJournalEntriesForm(FlaskForm):
    number = IntegerField('Number',validators=[DataRequired(), NumberRange(min=0, max=10)])
    obtain = SubmitField('Obtain')