import sqlalchemy as db

from models.questions import Question
from models.test import Test
from models.answers import Answer


class DatabaseManager:
    engine = db.create_engine('sqlite:///test.sqlite?check_same_thread=False')
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
             'description': 'Grammar test about Past Simple negative,statements and questions'},
            {'id': '4', 'name': 'Commonly Misspelled Words', 'description': 'Do you know the correct words?'},
            {'id': '5', 'name': 'Grammar', 'description': 'Testing your grammar.'}
        ]
        self.engine.execute(query_for_tests, tests_data)
        query_for_questions = db.insert(self.questions)
        questions_data = [{'id': '1', 'test_id': 1,
                           'question': 'She arrived at 8 p.m., opened the door and shouted "Good ......!'},
                          {'id': '2', 'test_id': 1,
                           'question': 'They have been married for over fifty years, but she still remembers the day she first ......'},
                          {'id': '3', 'test_id': 2, 'question': 'I ..... to school.'},
                          {'id': '4', 'test_id': 3, 'question': 'Yesterday we ....... swimming.'},
                          {'id': '5', 'test_id': 4,
                           'question': 'The drawbridge went up while I was driving _______ the party. I hoped it wouldn\'t make me _______ late for the party.'},
                          {'id': '6', 'test_id': 4,
                           'question': 'Unfortunately, Jim\'s buckle must have been _______ _______ , as his pants dropped to the floor during the performance.'},
                          {'id': '7', 'test_id': 4,
                           'question': 'When I spotted my parents at the airport, I exclaimed to my sister \"Look, _______ over _______!\"'},
                          {'id': '8', 'test_id': 4,
                           'question': 'I can tell you why _______ here. You left _______ keys on the kitchen counter.'},
                          {'id': '9', 'test_id': 4,
                           'question': 'I think I saw a ghost! He was standing right in front of me, then he just _______.'},
                          {'id': '10', 'test_id': 4,
                           'question': 'I gave my cat, Mr. Ribbons, some tuna for dinner. He was in total _______.'},
                          {'id': '11', 'test_id': 5, 'question': 'I am thin. He is ______.'},
                          {'id': '12', 'test_id': 5, 'question': 'Daniel always goes skateboarding ______ Sundays.'},
                          {'id': '13', 'test_id': 5, 'question': 'The woman was bitten ______ a snake.'},
                          {'id': '14', 'test_id': 5, 'question': 'Which of the following sentences is INCORRECT?'},
                          {'id': '15', 'test_id': 5, 'question': 'Your children don’t go out alone, ______?'},
                          {'id': '16', 'test_id': 5,
                           'question': 'I listened to the weather forecast. It ______ nice today.'}
                          ]
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
                       {'id': '12', 'question_id': 3, 'answer': 'have gone', 'true_answer': False},
                       {'id': '13', 'question_id': 5, 'answer': 'To / Too', 'true_answer': True},
                       {'id': '14', 'question_id': 5, 'answer': 'Too / Too', 'true_answer': False},
                       {'id': '15', 'question_id': 5, 'answer': 'To / Two', 'true_answer': False},
                       {'id': '16', 'question_id': 6, 'answer': 'To Lose', 'true_answer': False},
                       {'id': '17', 'question_id': 6, 'answer': 'Too Lose', 'true_answer': False},
                       {'id': '18', 'question_id': 6, 'answer': 'Too Loose', 'true_answer': True},
                       {'id': '19', 'question_id': 6, 'answer': 'Too Loss', 'true_answer': False},
                       {'id': '20', 'question_id': 7, 'answer': 'Their / There', 'true_answer': False},
                       {'id': '21', 'question_id': 7, 'answer': 'There / Their', 'true_answer': False},
                       {'id': '22', 'question_id': 7, 'answer': 'They\'re / There', 'true_answer': True},
                       {'id': '23', 'question_id': 8, 'answer': 'Your / Your', 'true_answer': False},
                       {'id': '24', 'question_id': 8, 'answer': 'You\'re / Your', 'true_answer': True},
                       {'id': '25', 'question_id': 8, 'answer': 'Your / You\'re', 'true_answer': False},
                       {'id': '26', 'question_id': 9, 'answer': 'Dissappeared', 'true_answer': False},
                       {'id': '27', 'question_id': 9, 'answer': 'Disappeared', 'true_answer': True},
                       {'id': '28', 'question_id': 9, 'answer': 'Dissapeared', 'true_answer': False},
                       {'id': '29', 'question_id': 10, 'answer': 'Ecstasy', 'true_answer': True},
                       {'id': '30', 'question_id': 10, 'answer': 'Ecstacy', 'true_answer': False},
                       {'id': '31', 'question_id': 10, 'answer': 'Extacy', 'true_answer': False},
                       {'id': '32', 'question_id': 10, 'answer': 'Exstacy', 'true_answer': False},
                       {'id': '33', 'question_id': 11, 'answer': 'thinner', 'true_answer': True},
                       {'id': '34', 'question_id': 11, 'answer': 'thiner', 'true_answer': False},
                       {'id': '35', 'question_id': 11, 'answer': 'thinnest', 'true_answer': False},
                       {'id': '36', 'question_id': 12, 'answer': 'each', 'true_answer': False},
                       {'id': '37', 'question_id': 12, 'answer': 'every', 'true_answer': False},
                       {'id': '38', 'question_id': 12, 'answer': 'on', 'true_answer': True},
                       {'id': '39', 'question_id': 13, 'answer': 'by', 'true_answer': True},
                       {'id': '40', 'question_id': 13, 'answer': 'from', 'true_answer': False},
                       {'id': '41', 'question_id': 13, 'answer': 'for', 'true_answer': False},
                       {'id': '42', 'question_id': 14, 'answer': 'I’ll finish the work in the morning.',
                        'true_answer': False},
                       {'id': '43', 'question_id': 14, 'answer': 'We went to Turkey in June.', 'true_answer': False},
                       {'id': '44', 'question_id': 14, 'answer': 'Let’s go to the cinema in the weekend.',
                        'true_answer': True},
                       {'id': '45', 'question_id': 15, 'answer': 'can’t they', 'true_answer': False},
                       {'id': '46', 'question_id': 15, 'answer': 'can they', 'true_answer': False},
                       {'id': '47', 'question_id': 15, 'answer': 'do they', 'true_answer': True},
                       {'id': '48', 'question_id': 16, 'answer': 'will be', 'true_answer': False},
                       {'id': '49', 'question_id': 16, 'answer': 'is going to be', 'true_answer': True},
                       {'id': '50', 'question_id': 16, 'answer': 'is being', 'true_answer': False}
                       ]
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

    def get_test_name(self, test_id):
        test_query = db.select(self.tests).where(self.tests.c.id == test_id)
        resultProxy_test = self.connection.execute(test_query)
        resultSet_test = resultProxy_test.first()
        return resultSet_test.name
