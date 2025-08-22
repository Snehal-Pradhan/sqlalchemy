# SQLAlchemy Learning Project

This repository is used for learning SQLAlchemy. Learning is done through a question-driven method.

## Method Used

1.  A question about SQLAlchemy is written down in a markdown file.
2.  The question is investigated through documentation and experimentation.
3.  A solution is written in a Python file to answer the question with code.
4.  The answer is summarized in the markdown file.
5.  The status is marked as completed.

## File Structure

The following structure is used to organize questions and answers.

```
├── core/
│   ├── 01_question_about_engine.md
│   └── 01_solution.py
├── querying/
├── relationships/
├── templates/
│   ├── question.md
│   └── solution.py
└── README.md
```

## How to Use

1.  A topic folder is selected (e.g., `core`, `querying`).
2.  The `templates/question.md` file is copied into the topic folder. The file is renamed to the next number in the sequence.
3.  The question is written in the new file. The status is set to `#pending`.
4.  The `templates/solution.py` file is copied into the same topic folder. It is given the same number as the question file.
5.  Code is written in the solution file to answer the question.
6.  After the solution is found, the question file is updated. The answer is written down and the status is changed to `#completed`.

## Templates

Two templates are provided:
-   `question.md`: Used to define and track a question.
-   `solution.py`: Used to write code that answers the question.

These templates are found in the `templates/` directory.

---