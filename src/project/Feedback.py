from pydantic import BaseModel


class LineFeedback(BaseModel):
    line_number: int
    feedback: str

    # def __init__(self, line_number, feedback):
    #     super().__init__()
    #     self.line_number = line_number
    #     self.feedback = feedback


class FileFeedback(BaseModel):
    line_feedback: list[LineFeedback]
    overall_comment: str


