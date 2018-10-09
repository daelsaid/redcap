import pycurl
import cStringIO
import pandas
import itertools
from redcap import Project, RedcapError


apiurl = 'https://redcap.stanford.edu/api/'
token = ''
best_project = Project(apiurl, token)
long_proj = Project(apiurl, token)
ssl_proj = Project(apiurl, token, verify_ssl=True)
survey_proj = Project(apiurl, '')


def metadata_to_df(best_project):
    """Test metadata export --> DataFrame"""
    df = best_project.export_metadata(format='df')
    return df


def export_always_include_def_field(best_project):
    """ Ensure def_field always comes in the output even if not explicity
    given in a requested form """
    # If we just ask for a form, must also get def_field in there
    records = best_project.export_records(forms=['imaging'])


def is_longitudinal(best_project):
    "Test the is_longitudinal method"
    best_project.assertFalse(best_project.reg_proj.is_longitudinal())
    best_project.assertTrue(best_project.long_proj.is_longitudinal())


def regular_attrs(best_project):
    """proj.events/arm_names/arm_nums should be empty tuples"""
    for attr in 'events', 'arm_names', 'arm_nums':
        attr_obj = getattr(best_project.reg_proj, attr)
        best_project.assertIsNotNone(attr_obj)
        best_project.assertEqual(len(attr_obj), 0)


def json_export(best_project):
    """ Make sure we get a list of dicts"""
    data = best_project.export_records()


def long_export(best_project):
    """After determining a unique event name, make sure we get a
    list of dicts"""
    unique_event = best_project.long_proj.events[0]['unique_event_name']
    data = best_project.long_proj.export_records(events=[unique_event])
    best_project.assertIsInstance(data, list)
    for record in data:
        best_project.assertIsInstance(record, dict)


def import_records(best_project):
    "Test record import"
    data = best_project.export_records()
    response = best_project.import_records(data)


def import_exception(best_project):
    "Test record import throws RedcapError for bad import"
    data = best_project.export_records()


def is_good_csv(best_project, csv_string):
    "Helper to test csv strings"
    return isinstance(csv_string, basestring)


def csv_export(best_project):
    """Test valid csv export """
    csv = best_project.export_records(format='csv')
