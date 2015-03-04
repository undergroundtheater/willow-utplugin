from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from willow.forms import get_chapter_query, \
        get_chapter_name, \
        get_venue_query, \
        ProfileForm

class UTProfileForm(ProfileForm):
    name = StringField('Real Name', validators=[DataRequired()])
    primary_chapter = QuerySelectField("Primary Chapter",
            query_factory=get_chapter_query,
            get_label=get_chapter_name,
            allow_blank=True,
            blank_text=u'Unassociated')

