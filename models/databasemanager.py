import sqlalchemy as db

from models.questions import Question
from models.test import Test
from models.answers import Answer


class DatabaseManager:
    engine = db.create_engine('sqlite:///test.sqlite')
    connection = engine.connect()

    metadata = db.MetaData()
    tests = db.Table('tests', metadata, db.Column('id', db.Integer()), db.Column('name', db.String(255)),
                     db.Column('description', db.String(255)))
    questions = db.Table('questions', metadata, db.Column('id', db.Integer()), db.Column('test_id', db.Integer()),
                         db.Column('question', db.String(255)))
    answers = db.Table('answers', metadata, db.Column('id', db.Integer()), db.Column('question_id', db.Integer()),
                       db.Column('answer', db.String(255)), db.Column('true_answer', db.Boolean()))

    def create_tables(self):
        self.metadata.create_all(self.engine)

    def insert_data(self):
        query_for_tests = db.insert(self.tests)
        tests_data = [
            {'id': '1', 'name': '15 Minutes Test', 'description': 'Take just 15 minutes to estimate your Enlish level'},
            {'id': '2', 'name': 'Present Simple Test',
             'description': 'Grammar test about Present Simple negative,statements and questions'},
            {'id': '3', 'name': 'Past Simple Test',
             'description': 'Grammar test about Past Simple negative,statements and questions'}]
        self.engine.execute(query_for_tests, tests_data)
        query_for_questions = db.insert(self.questions)
        questions_data = [{'id': '1', 'test_id': 1,
                           'question': 'She arrived at 8 p.m., opened the door and shouted "Good ......!'},
                          {'id': '2', 'test_id': 1,
                           'question': 'They have been married for over fifty years, but she still remembers the day she first ......'},
                          {'id': '3', 'test_id': 2, 'question': 'I ..... to school.'},
                          {'id': '4', 'test_id': 3, 'question': 'Yesterday we ....... swimming.'}]
        self.engine.execute(query_for_questions, questions_data)
        query_for_answers = db.insert(self.answers)
        answer_data = [{'id': '1', 'question_id': 1, 'answer': 'morning', 'true_answer': False},
                       {'id': '2', 'question_id': 1, 'answer': 'evening', 'true_answer': True},
                       {'id': '3', 'question_id': 1, 'answer': 'bye', 'true_answer': False},
                       {'id': '4', 'question_id': 1, 'answer': 'afternoon', 'true_answer': False},
                       {'id': '5', 'question_id': 2, 'answer': 'keen on him', 'true_answer': False},
                       {'id': '6', 'question_id': 2, 'answer': 'stuck on him', 'true_answer': False},
                       {'id': '7', 'question_id': 2, 'answer': 'fell for him', 'true_answer': True},
                       {'id': '8', 'question_id': 2, 'answer': 'wed him', 'true_answer': False},
                       {'id': '9', 'question_id': 3, 'answer': 'go', 'true_answer': True},
                       {'id': '10', 'question_id': 3, 'answer': 'goes', 'true_answer': False},
                       {'id': '11', 'question_id': 3, 'answer': 'went', 'true_answer': False},
                       {'id': '12', 'question_id': 3, 'answer': 'have gone', 'true_answer': False}]
        self.engine.execute(query_for_answers, answer_data)

    def get_test(self, name_of_test):
        test_query = db.select(self.tests).where(self.tests.c.name == name_of_test)
        resultProxy_test = self.connection.execute(test_query)
        resultSet_test = resultProxy_test.fetchall()
        result_test = resultSet_test[0]
        result_description = result_test.description
        result_id = result_test.id
        questions_query = db.select(self.questions).where(self.questions.c.test_id == result_id)
        resultProxy_questions = self.connection.execute(questions_query)
        resultSet_questions = resultProxy_questions.fetchall()
        questions_data = []
        for question in resultSet_questions:
            answers_data = []
            answers_query = db.select(self.answers).where(self.answers.c.question_id == question.id)
            resultProxy_answers = self.connection.execute(answers_query)
            resultSet_answers = resultProxy_answers.fetchall()
            for answer in resultSet_answers:
                answers_data.append(Answer(answer.id, answer.answer, answer.true_answer))
            questions_data.append(Question(question.id, question.question, answers_data))

        return Test(result_id, name_of_test, result_description, questions_data)
