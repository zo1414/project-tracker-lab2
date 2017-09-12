"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print "Student: {first} {last}\nGitHub account: {acct}".format(
        first=row[0], last=row[1], acct=row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO students (first_name, last_name, github)
            VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})

    db.session.commit()

    print "Successfully added student: {first} {last}".format(
        first=first_name, last=last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
        SELECT *
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print "Title: {title}\nDescription: {des}\nMax Grade: {grade}".format(
        title=row[1], des=row[2], grade=row[3])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """
            SELECT grade
            FROM grades
            WHERE student_github = :github AND project_title = :title
            """

    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})

    row = db_cursor.fetchone()

    print "Grade: {grade}".format(grade=row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
        VALUES (:github, :title, :grade)
        """

    db.session.execute(QUERY, {'github': github,
                               'title': title,
                               'grade': grade})

    db.session.commit()

    print "Successfully input grade for {git}".format(git=github)


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "give_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
