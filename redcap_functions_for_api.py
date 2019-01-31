import pycurl
import cStringIO
import pandas
import itertools
from redcap import Project, RedcapError


apiurl = 'https://redcap.stanford.edu/api/'
token = ''
rc_project = Project(apiurl, token)
long_proj = Project(apiurl, token)
ssl_proj = Project(apiurl, token, verify_ssl=True)
survey_proj = Project(apiurl, '')


def metadata_to_df(rc_project):
    df = rc_project.export_metadata(format='df')
    return df


def export_always_include_def_field(rc_project):
    """ Ensure def_field always comes in the output even if not explicity
    given in a requested form """
    # If we just ask for a form, must also get def_field in there
    records = rc_project.export_records(forms=['imaging'])


def is_longitudinal(rc_project):
    "Test the is_longitudinal method"
    rc_project.assertFalse(rc_project.reg_proj.is_longitudinal())
    rc_project.assertTrue(rc_project.long_proj.is_longitudinal())


def regular_attrs(rc_project):
    """proj.events/arm_names/arm_nums should be empty tuples"""
    for attr in 'events', 'arm_names', 'arm_nums':
        attr_obj = getattr(rc_project.reg_proj, attr)
        rc_project.assertIsNotNone(attr_obj)
        rc_project.assertEqual(len(attr_obj), 0)


def json_export(rc_project):
    """ Make sure we get a list of dicts"""
    data = rc_project.export_records()


def long_export(rc_project):
    """After determining a unique event name, make sure we get a
    list of dicts"""
    unique_event = rc_project.long_proj.events[0]['unique_event_name']
    data = rc_project.long_proj.export_records(events=[unique_event])
    rc_project.assertIsInstance(data, list)
    for record in data:
        rc_project.assertIsInstance(record, dict)


def import_records(rc_project):
    "Test record import"
    data = rc_project.export_records()
    response = rc_project.import_records(data)


def import_exception(rc_project):
    "Test record import throws RedcapError for bad import"
    data = rc_project.export_records()


def is_good_csv(rc_project, csv_string):
    "Helper to test csv strings"
    return isinstance(csv_string, basestring)


def csv_export(rc_project):
    """Test valid csv export """
    csv = rc_project.export_records(format='csv')
