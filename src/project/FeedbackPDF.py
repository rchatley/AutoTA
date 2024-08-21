import os
from datetime import datetime

from fpdf import FPDF


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

    def add_commit_summary(self, revision_history):

        (summary, build_results) = revision_history

        self.add_page()
        self.set_font('Courier', 'B', 16)
        self.cell(0, 10, 'Summary of Git Commits', 0, 1, 'C')
        self.set_font('Courier', '', 12)

        self.cell(0, self.line_height * 2, summary, border=0, ln=1)

        for commit in build_results:
            display = commit['hash'] + " - " + commit['message']
            if commit['result'] == "Passed":
                with self.highlight(commit['log'], modification_time=None, color=(0, 1, 0)):
                    self.cell(0, self.line_height * 2, display, border=0, ln=1)
            elif commit['result'] == "Failed":
                with self.highlight(commit['log'], modification_time=None, color=(1, 0, 0)):
                    self.cell(0, self.line_height * 2, display, border=0, ln=1)
            else:
                self.cell(0, self.line_height * 2, commit, border=0, ln=1)

    def add_code_with_feedback(self, file):
        self.file_name = file.file_name
        self.add_page()

        if file.gpt_feedback is not None:
            self.print_gpt_feedback(file)

        self.set_xy(10, 20)
        self.set_font('Courier', '', 8)
        self.set_text_color(0, 0, 0)

        feedback_dict = {line_num: fb for line_num, fb in file.feedback}
        code_lines = file.contents.split('\n')

        for i, line in enumerate(code_lines):
            line_number = f'{i + 1:4}: '
            line_text = line_number + ''.join(map(str, line)).replace("\r", '')
            line_feedback = feedback_dict.get(i + 1)
            width = self.w / 2
            if line_feedback:
                with self.highlight(line_feedback, modification_time=None, color=(1, 1, 0)):
                    self.cell(width, self.line_height, line_text, border=0, ln=1)
            else:
                self.cell(width, self.line_height, line_text, border=0, ln=1)

    def print_gpt_feedback(self, file):
        self.set_font('DejaVu', '', 10)
        page_width = self.w
        cell_width = (page_width / 2) - 10
        x_position = page_width / 2
        y_position = 20
        self.set_xy(x_position, y_position)
        self.set_text_color(255, 0, 0)
        self.multi_cell(cell_width, self.line_height, file.gpt_feedback)


