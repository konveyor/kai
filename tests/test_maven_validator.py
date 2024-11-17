import unittest

from kai.reactive_codeplanner.task_runner.compiler.maven_validator import (
    AccessControlError,
    BuildError,
    DependencyResolutionError,
    OtherError,
    PackageDoesNotExistError,
    SymbolNotFoundError,
    SyntaxError,
    TypeMismatchError,
    parse_maven_output,
)


class TestParseMavenOutput(unittest.TestCase):

    def test_no_errors(self) -> None:
        # Test case where Maven runs successfully without errors
        maven_output = """
[INFO] Scanning for projects...
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
"""
        rc = 0
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 0, "Expected no errors for successful build.")

    def test_symbol_not_found_error(self) -> None:
        # Test case for 'cannot find symbol' error
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/MyClass.java:[10,15] cannot find symbol
  symbol:   variable x
  location: class MyClass
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, SymbolNotFoundError)
        self.assertEqual(error.file, "/path/to/MyClass.java")
        self.assertEqual(error.line, 10)
        self.assertEqual(error.column, 15)
        self.assertEqual(error.missing_symbol, "variable x")
        self.assertEqual(error.symbol_location, "class MyClass")

    def test_package_does_not_exist_error(self) -> None:
        # Test case for 'package does not exist' error
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/AnotherClass.java:[5,8] package com.example.missing does not exist
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, PackageDoesNotExistError)
        self.assertEqual(error.file, "/path/to/AnotherClass.java")
        self.assertEqual(error.line, 5)
        self.assertEqual(error.column, 8)
        self.assertEqual(error.missing_package, "com.example.missing")

    def test_syntax_error(self) -> None:
        # Test case for syntax error
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/InvalidSyntax.java:[20,5] class, interface, or enum expected
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, SyntaxError)
        self.assertEqual(error.file, "/path/to/InvalidSyntax.java")
        self.assertEqual(error.line, 20)
        self.assertEqual(error.column, 5)

    def test_type_mismatch_error(self) -> None:
        # Test case for type mismatch error
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/TypeMismatch.java:[15,25] incompatible types: String cannot be converted to int
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, TypeMismatchError)
        self.assertEqual(error.file, "/path/to/TypeMismatch.java")
        self.assertEqual(error.line, 15)
        self.assertEqual(error.column, 25)
        self.assertEqual(
            error.message, "incompatible types: String cannot be converted to int"
        )

    def test_access_control_error(self) -> None:
        # Test case for access control error
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/AccessError.java:[30,10] cannot access com.example.PrivateClass
  class file for com.example.PrivateClass not found
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, AccessControlError)
        self.assertEqual(error.file, "/path/to/AccessError.java")
        self.assertEqual(error.line, 30)
        self.assertEqual(error.column, 10)
        self.assertEqual(error.inaccessible_class, "com.example.PrivateClass")

    def test_build_error(self) -> None:
        # Test case for a build error
        maven_output = """
[ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-parseable POM /path/to/pom.xml: expected start tag not found @ line 3, column 15
[ERROR] The build could not read 1 project -> [Help 1]
[ERROR]   The project  (/path/to/pom.xml) has 1 error
[ERROR]     Non-parseable POM /path/to/pom.xml: expected start tag not found @ line 3, column 15 -> [Help 2]
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one build error.")
        error = errors[0]
        self.assertIsInstance(error, BuildError)
        self.assertEqual(error.file, "/path/to/pom.xml")
        self.assertEqual(error.line, 3)
        self.assertEqual(error.column, 15)
        self.assertTrue("Non-parseable POM" in error.message)

    def test_multiple_identical_build_errors(self) -> None:
        # Test case where the same build error appears multiple times
        maven_output = """
[ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-parseable POM /path/to/pom.xml: invalid content @ line 5, column 20
[ERROR] The build could not read 1 project -> [Help 1]
[ERROR]   The project  (/path/to/pom.xml) has 1 error
[ERROR]     Non-parseable POM /path/to/pom.xml: invalid content @ line 5, column 20 -> [Help 2]
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        # Assuming deduplication is implemented in parse_maven_output
        self.assertEqual(
            len(errors), 1, "Expected one unique build error despite duplicates."
        )
        error = errors[0]
        self.assertIsInstance(error, BuildError)
        self.assertEqual(error.file, "/path/to/pom.xml")
        self.assertEqual(error.line, 5)
        self.assertEqual(error.column, 20)

    def test_failsafe_mechanism(self) -> None:
        # Test case where rc != 0 but no errors are parsed, triggering the failsafe
        maven_output = """
[INFO] Scanning for projects...
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.8.0:compile (default-compile) on project my-app: Compilation failure
[ERROR] 
[ERROR] -> [Help 1]
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(
            len(errors), 1, "Expected one error due to failsafe mechanism."
        )
        error = errors[0]
        self.assertIsInstance(error, OtherError)
        self.assertEqual(error.file, "unknown file")
        self.assertEqual(error.line, -1)
        self.assertEqual(error.column, -1)
        self.assertEqual(error.message, "Unknown error occurred during Maven build.")
        self.assertIn("BUILD FAILURE", error.details[0])

    def test_unhandled_error(self) -> None:
        # Test case for an error that doesn't match any known patterns
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/UnknownError.java:[50,20] unexpected error: unknown reason
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one error.")
        error = errors[0]
        self.assertIsInstance(error, OtherError)
        self.assertEqual(error.file, "/path/to/UnknownError.java")
        self.assertEqual(error.line, 50)
        self.assertEqual(error.column, 20)
        self.assertEqual(error.message, "unexpected error: unknown reason")

    def test_multiple_errors(self) -> None:
        # Test case with multiple different errors
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/ClassOne.java:[10,15] cannot find symbol
  symbol:   method doSomething()
  location: class ClassOne
[ERROR] /path/to/ClassTwo.java:[5,8] package com.example.missing does not exist
[INFO] 2 errors
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 2, "Expected two errors.")
        # First error
        error1 = errors[0]
        self.assertIsInstance(error1, SymbolNotFoundError)
        self.assertEqual(error1.file, "/path/to/ClassOne.java")
        self.assertEqual(error1.line, 10)
        self.assertEqual(error1.column, 15)
        self.assertEqual(error1.missing_symbol, "method doSomething()")
        self.assertEqual(error1.symbol_location, "class ClassOne")
        # Second error
        error2 = errors[1]
        self.assertIsInstance(error2, PackageDoesNotExistError)
        self.assertEqual(error2.file, "/path/to/ClassTwo.java")
        self.assertEqual(error2.line, 5)
        self.assertEqual(error2.column, 8)
        self.assertEqual(error2.missing_package, "com.example.missing")

    def test_duplicate_compilation_errors(self) -> None:
        # Test case with duplicate compilation errors
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/DuplicateError.java:[25,30] cannot find symbol
  symbol:   class MissingClass
  location: package com.example
[ERROR] /path/to/DuplicateError.java:[25,30] cannot find symbol
  symbol:   class MissingClass
  location: package com.example
[INFO] 2 errors
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        # Assuming deduplication is implemented
        self.assertEqual(
            len(errors), 1, "Expected one unique error despite duplicates."
        )
        error = errors[0]
        self.assertIsInstance(error, SymbolNotFoundError)
        self.assertEqual(error.file, "/path/to/DuplicateError.java")
        self.assertEqual(error.line, 25)
        self.assertEqual(error.column, 30)
        self.assertEqual(error.missing_symbol, "class MissingClass")
        self.assertEqual(error.symbol_location, "package com.example")

    def test_maven_not_installed(self) -> None:
        # Test case where Maven is not installed
        maven_output = ""
        rc = -1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(
            len(errors), 1, "Expected one error due to Maven not being installed."
        )
        error = errors[0]
        self.assertIsInstance(error, OtherError)
        self.assertEqual(error.file, "unknown file")
        self.assertEqual(error.message, "Unknown error occurred during Maven build.")

    def test_compile_error_with_details(self) -> None:
        # Test case with compilation error including detailed messages
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/ComplexError.java:[40,22] incompatible types: int cannot be converted to String
[ERROR] /path/to/ComplexError.java:[41,10] cannot find symbol
  symbol:   variable undefinedVar
  location: class ComplexError
[INFO] 2 errors
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 2, "Expected two errors.")
        # First error
        error1 = errors[0]
        self.assertIsInstance(error1, TypeMismatchError)
        self.assertEqual(error1.file, "/path/to/ComplexError.java")
        self.assertEqual(error1.line, 40)
        self.assertEqual(error1.column, 22)
        self.assertEqual(
            error1.message, "incompatible types: int cannot be converted to String"
        )
        # Second error
        error2 = errors[1]
        self.assertIsInstance(error2, SymbolNotFoundError)
        self.assertEqual(error2.file, "/path/to/ComplexError.java")
        self.assertEqual(error2.line, 41)
        self.assertEqual(error2.column, 10)
        self.assertEqual(error2.missing_symbol, "variable undefinedVar")
        self.assertEqual(error2.symbol_location, "class ComplexError")

    def test_error_with_no_line_column(self) -> None:
        # Test case where the error line does not contain line and column numbers
        maven_output = """
[ERROR] COMPILATION ERROR :
[ERROR] /path/to/UnknownLocation.java: cannot find symbol
  symbol:   class UnknownClass
[INFO] 1 error
[INFO] -------------------------------------------------------------
[ERROR] BUILD FAILURE
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        # Since the error_pattern requires line and column, this error may not be parsed.
        # Adjust the regex pattern if needed.
        self.assertEqual(
            len(errors), 1, "Expected one error despite missing line and column."
        )
        error = errors[0]
        self.assertIsInstance(error, SymbolNotFoundError)
        self.assertEqual(error.file, "/path/to/UnknownLocation.java")
        self.assertEqual(error.line, -1)
        self.assertEqual(error.column, -1)
        self.assertEqual(error.missing_symbol, "class UnknownClass")

    def test_build_error_with_multiple_projects(self) -> None:
        # Test case with build errors in a multi-module project
        maven_output = """
[ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-resolvable parent POM for com.example:module1:1.0-SNAPSHOT: Could not find artifact com.example:parent:pom:1.0-SNAPSHOT and 'parent.relativePath' points at wrong local POM @ line 5, column 13
[ERROR] The build could not read 1 project -> [Help 1]
[ERROR]   The project com.example:module1:1.0-SNAPSHOT (/path/to/module1/pom.xml) has 1 error
[ERROR]     Non-resolvable parent POM for com.example:module1:1.0-SNAPSHOT: Could not find artifact com.example:parent:pom:1.0-SNAPSHOT and 'parent.relativePath' points at wrong local POM @ line 5, column 13 -> [Help 2]
"""
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        # Assuming deduplication is implemented
        self.assertEqual(len(errors), 1, "Expected one unique build error.")
        error = errors[0]
        self.assertIsInstance(error, BuildError)
        self.assertEqual(error.file, "/path/to/module1/pom.xml")
        self.assertEqual(error.line, 5)
        self.assertEqual(error.column, 13)
        self.assertIn("Non-resolvable parent POM", error.message)

    def test_dependency_resolution_error(self) -> None:
        maven_output = """
    [INFO] Scanning for projects...
    [INFO]
    [INFO] -------------------< com.redhat.coolstore:monolith >--------------------
    [INFO] Building coolstore-monolith 1.0.0-SNAPSHOT
    [INFO]   from pom.xml
    [INFO] --------------------------------[ jar ]---------------------------------
    Downloading from github: https://maven.pkg.github.com/shawn-hurley/analyzer-lsp/jakarta/jakarta.jakartaee-web-api/8.0.0/jakarta.jakartaee-web-api-8.0.0.pom
    Downloading from github: https://maven.pkg.github.com/shawn-hurley/analyzer-lsp/jakarta/jakarta.jakartaee-api/8.0.0/jakarta.jakartaee-api-8.0.0.pom
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD FAILURE
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time:  2.296 s
    [INFO] Finished at: 2024-11-13T14:02:10-05:00
    [INFO] ------------------------------------------------------------------------
    [ERROR] Failed to execute goal on project monolith: Could not resolve dependencies for project com.redhat.coolstore:monolith:jar:1.0.0-SNAPSHOT: Failed to collect dependencies at jakarta:jakarta.jakartaee-web-api:jar:8.0.0: ...
    [ERROR]
    [ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
    [ERROR] Re-run Maven using the -X switch to enable full debug logging.
    [ERROR]
    [ERROR] For more information about the errors and possible solutions, please read the following articles:
    [ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/DependencyResolutionException
    """
        rc = 1
        errors = parse_maven_output(maven_output, rc)
        self.assertEqual(len(errors), 1, "Expected one dependency resolution error.")
        error = errors[0]
        self.assertIsInstance(error, DependencyResolutionError)
        self.assertEqual(error.file, "pom.xml")
        self.assertEqual(error.line, -1)
        self.assertEqual(error.column, -1)
        self.assertEqual(error.project, "monolith")
        self.assertEqual(error.goal, "")
        self.assertIn("Could not resolve dependencies", error.message)

    def test_bad_pom_error(self) -> None:
        mvn_output = """
[INFO] Scanning for projects...
[ERROR] [ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-parseable POM /kai/example/coolstore/pom.xml: processing instruction can not have PITarget with reserved xml name (position: START_DOCUMENT seen \n\n<?xml ... @3:7)  @ line 3, column 7
 @ 
[ERROR] The build could not read 1 project -> [Help 1]
[ERROR]   
[ERROR]   The project  (/kai/example/coolstore/pom.xml) has 1 error
[ERROR]     Non-parseable POM /kai/example/coolstore/pom.xml: processing instruction can not have PITarget with reserved xml name (position: START_DOCUMENT seen \n\n<?xml ... @3:7)  @ line 3, column 7 -> [Help 2]
[ERROR] 
"""
        errors = parse_maven_output(mvn_output, rc=1)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].file, "/kai/example/coolstore/pom.xml")


if __name__ == "__main__":
    unittest.main()
