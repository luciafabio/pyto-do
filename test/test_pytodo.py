import sys
import os

from click.testing import CliRunner

# add module directory to path
module_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, module_path + '/../')

from pycli_todo import entry_point

RUNNER = CliRunner()
PENDING_SYMBOL = "\u2715"
DONE_SYMBOL = "\u2713"
WORKING_SYMBOL = "\u26A0"


def test_entry_point(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, [])
    assert result.exit_code == 1
    assert result.output == ".todo file not found!\n"


def test_init(tmpdir):
    os.chdir(tmpdir)

    # create todo file
    result = RUNNER.invoke(entry_point, ['init'])
    assert result.output == f'A \".todo\" file is now added to {tmpdir}\n'

    # todo file already created
    result = RUNNER.invoke(entry_point, ['init'])
    assert result.output == f'A \".todo\" file already exists in {tmpdir}\n'


def test_add(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    assert result.exit_code == 0

    result = RUNNER.invoke(entry_point, [])
    assert result.output == f"1   | {PENDING_SYMBOL} test task 1\n"

    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} test task 2\n")


def test_working(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, ['working', '2'])
    assert result.exit_code == 0

    result = RUNNER.invoke(entry_point, ["--all"])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {WORKING_SYMBOL} test task 2\n")


def test_toggle(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    # toggle pending to done
    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, ['toggle', '2'])
    assert result.exit_code == 0

    result = RUNNER.invoke(entry_point, ["--all"])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {DONE_SYMBOL} test task 2\n")

    # toggle working to done
    result = RUNNER.invoke(entry_point, ['working', '2'])
    result = RUNNER.invoke(entry_point, ['toggle', '2'])
    assert result.exit_code == 0

    result = RUNNER.invoke(entry_point, ["--all"])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {DONE_SYMBOL} test task 2\n")

    # toggle done to pending
    result = RUNNER.invoke(entry_point, ['toggle', '2'])
    assert result.exit_code == 0

    result = RUNNER.invoke(entry_point, ["--all"])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} test task 2\n")



def test_clean(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])

    result = RUNNER.invoke(entry_point, ['toggle', '2'])
    result = RUNNER.invoke(entry_point, ['clean'])
    result = RUNNER.invoke(entry_point, [])
    assert result.output == f"1   | {PENDING_SYMBOL} test task 1\n"

    result = RUNNER.invoke(entry_point, ['toggle', '1'])
    result = RUNNER.invoke(entry_point, ['clean'])
    result = RUNNER.invoke(entry_point, [])
    assert result.output == ""


def test_modify(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])

    result = RUNNER.invoke(
        entry_point, ['modify', '2', 'new task 2 description'])

    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} new task 2 description\n")


def test_reorder(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 3'])
    result = RUNNER.invoke(entry_point, ['reorder', '1', '2'])

    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 2\n"
        f"2   | {PENDING_SYMBOL} test task 1\n"
        f"3   | {PENDING_SYMBOL} test task 3\n")

    result = RUNNER.invoke(entry_point, ['toggle', '2'])
    result = RUNNER.invoke(entry_point, ['clean'])

    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 2\n"
        f"3   | {PENDING_SYMBOL} test task 3\n")

    result = RUNNER.invoke(entry_point, ['reorder'])

    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 2\n"
        f"2   | {PENDING_SYMBOL} test task 3\n")


def test_search(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, ['add', 'new task 3'])

    result = RUNNER.invoke(entry_point, ['search', 'new'])
    assert result.output == f"3   | {PENDING_SYMBOL} new task 3\n"


def test_flags(tmpdir):
    os.chdir(tmpdir)

    result = RUNNER.invoke(entry_point, ['init'])

    result = RUNNER.invoke(entry_point, ['add', 'test task 1'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 2'])
    result = RUNNER.invoke(entry_point, ['add', 'test task 3'])
    result = RUNNER.invoke(entry_point, ['toggle', '3'])

    result = RUNNER.invoke(entry_point, ['--done'])
    assert result.output == f"3   | {DONE_SYMBOL} test task 3\n"

    result = RUNNER.invoke(entry_point, ['-d'])
    assert result.output == f"3   | {DONE_SYMBOL} test task 3\n"

    result = RUNNER.invoke(entry_point, ['--all'])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} test task 2\n"
        f"3   | {DONE_SYMBOL} test task 3\n")

    result = RUNNER.invoke(entry_point, ['-a'])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} test task 2\n"
        f"3   | {DONE_SYMBOL} test task 3\n")

    result = RUNNER.invoke(entry_point, [])
    assert result.output == (
        f"1   | {PENDING_SYMBOL} test task 1\n"
        f"2   | {PENDING_SYMBOL} test task 2\n")
