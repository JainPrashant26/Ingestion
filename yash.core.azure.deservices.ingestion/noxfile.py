import nox

locations = "src", "ingestion", "noxfile.py"


@nox.session()
def lint(session):
    """Run the Linting using Flake8."""
    args = session.posargs or locations
    session.install("flake8")
    session.install("flake8-junit-report", "--use-pep517")
    session.run("flake8", "--tee", "src/", "--output-file", "tests-reports/flake8.txt", "--exit-zero")
    session.run("flake8_junit", "tests-reports/flake8.txt", "tests-reports/lint-results.xml")


@nox.session()
def test_functional(session):
    """Run the Functional Test Suite."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    if session.posargs:
        patterns = ['ingestion/patterns/'+session.posargs[0]+'/tests']
    else:
        patterns = ['ingestion/patterns/excel_adls/tests',
                    'ingestion/patterns/excel_adls_master/tests',
                    'ingestion/patterns/file_cdc/tests',
                    'ingestion/patterns/az_sql_cdc/tests',
                    'ingestion/patterns/az_sql_cdc_master/tests',
                    'ingestion/patterns/az_sql_bulk/tests',
                    'ingestion/patterns/az_sql_bulk_master/tests',
                    'ingestion/patterns/sql_cdc/tests',
                    'ingestion/patterns/sql_cdc_master/tests',
                    'ingestion/patterns/sql_bulk/tests',
                    'ingestion/patterns/sql_bulk_master/tests']

    session.run("poetry", "run", "pytest", "-s", *patterns, "--junitxml=tests-reports/functional-tests-results.xml")


@nox.session()
def code_coverage(session):
    """Run the Code Coverage."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", "--cov=yash.core.azure.deservices.ingestion",
              "--cov-report=xml:test-reports/coverage-results.xml")
   
            
