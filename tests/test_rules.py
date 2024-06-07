import unittest

from review.filters.JavaFilter import JavaFilter
from review.filters.PythonFilter import PythonFilter
from review.project.ReviewFile import ReviewFile
from review.rules.EncapsulationRule import EncapsulationRule
from review.rules.IdentifierRule import IdentifierRule


class TestRules(unittest.TestCase):
    def test_positive_java_encapsulation_rule(self):
        code = """
        public class Example {
            private final String encapsulated = "test";
            public String getEncapsulated() {
                return encapsulated;
            }
        }
        """
        file = ReviewFile('./', 'example.java', contents=code)
        results = EncapsulationRule().apply(file)

        self.assertEqual(results, [])

    def test_negative_java_encapsulation_rule(self):
        code = """
        public class Example {
            public String encapsulated;
            public String getEncapsulated() {
                return encapsulated;
            }
        }
        """
        file = ReviewFile('./', 'example.java', contents=code)
        results = EncapsulationRule().apply(file)

        self.assertEqual(len(results), 1)

    def test_positive_java_identifier_rule(self):
        code = """
        public class ExampleTest {
            @Test
            public void doesThing() {
                assertThat(1, is(1));
            }
        }
        """
        file = ReviewFile('./', 'example.java', contents=code)
        results = IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                        node_name=r"^test")).apply(
            file)

        self.assertEqual(results, [])

    def test_negative_java_identifier_rule(self):
        code = """
        public class ExampleTest {
            @Test
            public void testThatDoesThing() {
                assertThat(1, is(1));
            }
        }
        """
        file = ReviewFile('./', 'example.java', contents=code)
        results = IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                        node_name=r"^test")).apply(
            file)

        self.assertEqual(len(results), 1)

    def test_positive_python_encapsulation_rule(self):
        code = """class Example:
            self._encapsulated = "test"
            def get_encapsulated(self):
                return self.encapsulated
        """
        file = ReviewFile('./', 'example.py', contents=code)
        results = EncapsulationRule().apply(file)

        self.assertEqual(results, [])

    def test_negative_python_encapsulation_rule(self):
        code = """class Example:
            self.encapsulated = "test"
            def get_encapsulated(self):
                return self.encapsulated
        """
        file = ReviewFile('./', 'example.py', contents=code)
        results = EncapsulationRule().apply(file)

        self.assertEqual(1, len(results))

    def test_positive_python_identifier_rule(self):
        code = """class Example:
            self.field = "something"
            def get_encapsulated(self):
                return self.encapsulated
        """
        file = ReviewFile('./', 'example.py', contents=code)
        results = IdentifierRule(
            node_filter=PythonFilter(node_class='method',
                                     node_name=r'.*[A-Z].*')).apply(file)

        self.assertEqual(results, [])

    def test_negative_python_identifier_rule(self):
        code = """class Example:
            self.field = "something"
            def getEncapsulated(self):
                return self.encapsulated
        """
        file = ReviewFile('./', 'example.py', contents=code)
        results = IdentifierRule(
            node_filter=PythonFilter(node_class='method',
                                     node_name=r'.*[A-Z].*')).apply(file)

        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
