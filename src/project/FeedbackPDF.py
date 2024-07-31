import os
from datetime import datetime

from fpdf import FPDF


class FeedbackPDF(FPDF):
    def __init__(self, task='Student Exercise', summary=None, orientation='L',
                 unit='mm', size='A4'):
        super().__init__(orientation, unit, size)
        self.file_name = ""
        self.add_cover_page(task, 'AutoTA', summary)
        self.set_font('Courier', '', 8)
        self.line_height = self.font_size * 1.25
        self.set_auto_page_break(auto=True, margin=15)
        self.cell(0, self.line_height, summary, border=0, ln=1)

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

    def add_commit_summary(self, commit_log):
        self.add_page()
        self.set_font('Courier', 'B', 16)
        self.cell(0, 10, 'Summary of Git Commits', 0, 1, 'C')
        self.set_font('Courier', '', 12)
        self.multi_cell(0, 10, commit_log)

    def add_code_with_feedback(self, file):
        self.file_name = file.file_name
        self.add_page()
        self.set_font('Courier', '', 8)
        feedback_dict = {line_num: fb for line_num, fb in file.feedback}
        code_lines = file.contents.split('\n')

        for i, line in enumerate(code_lines):
            line_number = f'{i + 1:4}: '
            line_text = line_number + ''.join(map(str, line)).replace("\r", '')
            line_feedback = feedback_dict.get(i + 1)
            if line_feedback:
                with self.highlight(line_feedback, modification_time=None, color=(1, 1, 0)):
                    self.cell(0, self.line_height, line_text, border=0, ln=1)
            else:
                self.cell(0, self.line_height, line_text, border=0, ln=1)
