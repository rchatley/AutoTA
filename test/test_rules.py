import unittest

from src.filters.JavaFilter import JavaFilter
from src.project.JavaFile import JavaFile
from src.rules.EncapsulationRule import EncapsulationRule
from src.rules.IdentifierRule import IdentifierRule


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
        file = JavaFile('./', 'example.java', contents=code)
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
        file = JavaFile('./', 'example.java', contents=code)
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
        file = JavaFile('./', 'example.java', contents=code)
        results = IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                        node_name=r"^test")).apply(file)

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
        file = JavaFile('./', 'example.java', contents=code)
        results = IdentifierRule(node_filter=JavaFilter(node_class='method',
                                                        node_name=r"^test")).apply(file)

        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
