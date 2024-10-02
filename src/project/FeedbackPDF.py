import os
from datetime import datetime
from typing import List

from fpdf import FPDF

from src.project.BuildResult import BuildResult
from src.project.BuildResults import BuildResults
from src.project.JavaFile import JavaFile


def feedback_for_line(line_number, file: JavaFile):
    return next((feedback.feedback for feedback in file.feedback if feedback.line_number == line_number), None)


class FeedbackPDF(FPDF):
    def __init__(self, task='Student Exercise', summary=None, orientation='L',
                 unit='mm', size='A4'):
        super().__init__(orientation, unit, size)
        self.file_name = ""
        self.add_cover_page(task, 'abc23', summary)
        self.set_font('Courier', '', 8)
        self.line_height = self.font_size * 1.25
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)

    def header(self):
        self.set_font('Courier', 'B', 12)
        self.cell(0, 10, f'{self.file_name}', 0, 1, 'C')

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font('Courier', 'B', 8)
            self.cell(0, 10, str(self.page_no() - 1), 0, 0, 'C')

    def add_cover_page(self, title, author, summary):
        self.add_page()
        self.set_font('Arial', 'B', 24)
        self.cell(0, 80, title, 0, 1, 'C')
        self.set_font('Arial', 'I', 16)
        self.cell(0, 10, f'Author: {author}', 0, 1, 'C')
        self.cell(0, 10, f'Date: {datetime.now().date()}', 0, 1, 'C')
        if summary is not None:
            self.set_font('Arial', '', 10)
            self.ln(20)
            self.multi_cell(0, 10, summary, 0, 'C')

    def add_commit_summary(self, build_results: BuildResults):

        self.add_page()
        self.set_font('Courier', 'B', 16)
        self.cell(0, 10, 'Summary of Git Commits', 0, 1, 'C')
        self.set_font('Courier', '', 12)

        self.cell(0, self.line_height * 2, build_results.summary, border=0, ln=1)

        result_colors = {
            BuildResult.Status.PASSED: (0, 1, 0),
            BuildResult.Status.COVERAGE: (1, 0.5, 0),
            BuildResult.Status.STYLE: (1, 1, 0),
            BuildResult.Status.FAILED: (1, 0, 0)
        }

        for build in build_results.builds:
            display = build.commit + " - " + build.message
            line_color = result_colors.get(build.status, (1, 1, 1))
            with self.highlight(build.log, modification_time=None, color=line_color):
                self.cell(0, self.line_height * 2, display, border=0, ln=1)

    def add_code_with_feedback(self, file):
        self.file_name = file.file_name
        self.add_page()

        if file.gpt_feedback is not None:
            self.print_gpt_feedback(file)

        self.set_xy(10, 20)
        self.set_font('Courier', '', 8)
        self.set_text_color(0, 0, 0)

        code_lines = file.contents.split('\n')

        for i, line in enumerate(code_lines):
            line_number = f'{i + 1:4}: '
            line_text = line_number + ''.join(map(str, line)).replace("\r", '')
            line_feedback = feedback_for_line(i + 1, file)
            width = self.w / 2
            if line_feedback:
                with self.highlight(line_feedback, modification_time=None, color=(1, 1, 0)):
                    self.cell(width, self.line_height, line_text, border=0, ln=1)
            else:
                self.cell(width, self.line_height, line_text, border=0, ln=1)

    def print_gpt_feedback(self, file):
        if file.gpt_feedback is None or len(file.gpt_feedback) == 0:
            return

        self.set_font('DejaVu', '', 10)
        page_width = self.w
        cell_width = (page_width / 2) - 10
        x_position = page_width / 2
        y_position = 20
        self.set_xy(x_position, y_position)
        self.set_text_color(255, 0, 0)
        self.multi_cell(cell_width, self.line_height, "\n\n".join(file.gpt_feedback))
        self.set_text_color(0, 0, 0)

    def comment_on(self, build_results: BuildResults, other_comments: List[str] = None):

        comments: list(str) = []

        if build_results.not_many_commits():
            comments.append("You have not made many commits. Try to commit more frequently, breaking down your work.")
            if build_results.all_passed():
                comments.append("Good that the commits you have made are passing though.")
        elif build_results.all_passed():
            comments.append("Incremental work and all builds passed. Good job!")
        elif build_results.final_build().passed():
            comments.append("Your final build passed. Good job!")

        if build_results.mostly_failed():
            comments.append("Most of your builds have failed. Try to only commit when the build is passing.")
        elif build_results.any_failed():
            comments.append("Some builds have failed. Try to only commit when the build is passing.")

        if build_results.show_style_errors():
            comments.append("Some builds have style errors. Try to fix these before committing.")
            comments.append("You can format your code automatically in your IDE.")

        if build_results.show_low_coverage():
            comments.append("Some builds have low test coverage. ")
            comments.append("If you follow TDD then every build should naturally have good coverage.")

        page_width = self.w
        cell_width = page_width - 20
        self.multi_cell(cell_width, self.line_height * 1.5, "\n" + "\n".join(comments + other_comments))
