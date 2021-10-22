import sqlalchemy as db

from models.test import Test


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

    def create_tables(self, metadata, engine):
        metadata.create_all(engine)

    def insert_data(self, tests, questions, answers, engine):
        query_for_tests = db.insert(tests)
        tests_data = [
            {'Id': '1', 'name': '15 Minutes Test', 'description': 'Take just 15 minutes to estimate your Enlish level'},
            {'Id': '2', 'name': 'Present Simple Test',
             'description': 'Grammar test about Present Simple negative,statements and questions'},
            {'Id': '3', 'name': 'Past Simple Test',
             'description': 'Grammar test about Past Simple negative,statements and questions'}]
        engine.execute(query_for_tests, tests_data)
        query_for_questions = db.insert(questions)
        questions_data = [{'Id': '1', 'test_id': 1,
                           'question': 'She arrived at 8 p.m., opened the door and shouted "Good ......!'},
                          {'Id': '2', 'test_id': 1,
                           'question': 'They have been married for over fifty years, but she still remembers the day she first ......'},
                          {'Id': '3', 'test_id': 2, 'question': 'I ..... to school.'},
                          {'Id': '4', 'test_id': 3, 'question': 'Yesterday we ....... swimming.'}]
        engine.execute(query_for_questions, questions_data)
        query_for_answers = db.insert(answers)
        answer_data = [{'Id': '1', 'question_id': 1, 'answer': 'morning', 'true_answer': False},
                       {'Id': '2', 'question_id': 1, 'answer': 'evening', 'true_answer': True},
                       {'Id': '3', 'question_id': 1, 'answer': 'bye', 'true_answer': False},
                       {'Id': '4', 'question_id': 1, 'answer': 'afternoon', 'true_answer': False},
                       {'Id': '5', 'question_id': 2, 'answer': 'keen on him', 'true_answer': False},
                       {'Id': '6', 'question_id': 2, 'answer': 'stuck on him', 'true_answer': False},
                       {'Id': '7', 'question_id': 2, 'answer': 'fell for him', 'true_answer': True},
                       {'Id': '8', 'question_id': 2, 'answer': 'wed him', 'true_answer': False},
                       {'Id': '9', 'question_id': 3, 'answer': 'go', 'true_answer': True},
                       {'Id': '10', 'question_id': 3, 'answer': 'goes', 'true_answer': False},
                       {'Id': '11', 'question_id': 3, 'answer': 'went', 'true_answer': False},
                       {'Id': '12', 'question_id': 3, 'answer': 'have gone', 'true_answer': False}]
        engine.execute(query_for_answers, answer_data)

    def get_test(self, name_of_test):
        query = db.select(self.tests).where(self.tests.c.name == name_of_test)
        return Test(name_of_test)
