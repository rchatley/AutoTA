import os
import subprocess

from Rules.Syntactic.SyntacticRule import SyntacticRule


class StyleRule(SyntacticRule):
    def __init__(self, scope='project', rule_modifiers=None):
        super().__init__(scope)

        self.traversal = self.build_traversal()

        self.rule = self.build_rule()

    def __str__(self):
        return f'STOIYLE'

    def build_traversal(self):
        checkstyle_jar = "checkstyle/checkstyle.jar"
        config_file = "checkstyle/google_checks.xml"

        def traversal(review_file):
            cmd = ["java", '-jar', checkstyle_jar, "-c", config_file,
                   os.path.join(review_file.root, review_file.file_name)]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                return ["ERROR IN CHECKSTYLE"]

            return list(stdout.decode("utf-8"))

        return traversal
