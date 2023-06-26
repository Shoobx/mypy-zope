import os
import re

import pytest
from mypy import build
from mypy import options
from mypy.errors import CompileError
from mypy.modulefinder import BuildSource


HERE = os.path.abspath(os.path.dirname(__file__))
SAMPLES_DIR = os.path.join(HERE, "samples")
OUTPUT_RE = re.compile(r"<output>(.*)</output>", re.MULTILINE | re.DOTALL)


@pytest.fixture(scope="session")
def mypy_cache_dir(tmp_path_factory):
    tdir = tmp_path_factory.mktemp('.mypy_cahe')
    print("Setup cache", str(tdir))
    return str(tdir)


def test_samples(samplefile, mypy_cache_dir):
    opts = options.Options()
    opts.cache_dir = mypy_cache_dir
    opts.show_traceback = True
    opts.namespace_packages = True
    opts.hide_error_codes = True
    opts.plugins = ['mypy_zope:plugin']
    opts.python_version = (3, 11)
    # Config file is needed to load plugins, it doesn't not exist and is not
    # supposed to.
    opts.config_file = '    not_existing_config.ini'

    try:
        base_dir = os.path.dirname(samplefile)
        source = BuildSource(samplefile,
                             module=None,
                             text=None,
                             base_dir=base_dir)
        res = build.build(
            sources=[source],
            options=opts)
    except CompileError as e:
        assert False, e

    normalized = normalize_errors(res.errors, samplefile)
    actual = '\n'.join(normalized)
    expected = find_expected_output(samplefile)
    assert actual == expected


def find_expected_output(filename):
    with open(filename, "r") as f:
        source = f.read()
        m = OUTPUT_RE.search(source)
        if not m:
            return ""
        return m.group(1).strip()


def normalize_errors(errors, filename):
    cwd = os.getcwd() + os.path.sep
    assert filename.startswith(cwd)
    relfname = filename[len(cwd):]
    basename = os.path.basename(filename)
    return [msg.replace(relfname, basename) for msg in errors]


def pytest_generate_tests(metafunc):
    samples = []
    ids = []
    for fname in os.listdir(SAMPLES_DIR):
        samples.append(os.path.join(SAMPLES_DIR, fname))
        name, ext = os.path.splitext(fname)
        ids.append(name)

    metafunc.parametrize("samplefile", samples, ids=ids)
