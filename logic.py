import csv
from PyQt6.QtWidgets import *
from gui import *


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        '''
        Initializes the Logic class, sets up the UI, and connects the submit button to the submit_vote method.
        '''
        super().__init__()
        self.setupUi(self)
        self.pushButton_Submit.clicked.connect(self.submit_vote)
        self.voters_file = 'voters_log.csv'

    def submit_vote(self) -> None:
        '''
        Handles the logic for submitting a vote. Validates the voter, checks if they've already voted.
        '''
        first_name = self.lineEdit_FirstName.text().strip()
        last_name = self.lineEdit_LastName.text().strip()
        voter_id = self.lineEdit_ID.text().strip()

        # Clear any previous text from the textEdit
        self.textEdit.clear()

        if not first_name or not last_name or not voter_id:
            self.textEdit.setHtml("<div style='text-align: center; color: red;'>Please fill in all fields.</div>")
            return

        if self.validate_voter(first_name, last_name, voter_id):
            if self.has_already_voted(first_name, last_name, voter_id):
                self.textEdit.setHtml(
                    "<div style='text-align: center; color: red;'>You have already voted.</div>")
                self.clear_inputs()  # Clear the inputs if the user has already voted
            else:
                selected_candidate = None
                if self.radioButton_John.isChecked():
                    selected_candidate = "John"
                elif self.radioButton_Alice.isChecked():
                    selected_candidate = "Alice"
                elif self.radioButton_Bob.isChecked():
                    selected_candidate = "Bob"

                if selected_candidate:
                    self.textEdit.setHtml(
                        f"<div style='text-align: center; color: green;'>Thank you for Voting.</div>")
                    self.log_voter(first_name, last_name, voter_id)
                    self.clear_inputs()
                else:
                    self.textEdit.setHtml(
                        "<div style='text-align: center; color: red;'>Please select a candidate.</div>")
        else:
            self.textEdit.setHtml("<div style='text-align: center; color: red;'>You are not eligible to vote.</div>")
            self.clear_inputs()

    def validate_voter(self, first_name: str, last_name: str, voter_id: str) -> bool:
        '''
        Validates if the voter is eligible to vote by checking against the eligible_voters.csv file.

        :param first_name: Voter's first name.
        :param last_name: Voter's last name.
        :param voter_id: Voter's ID.
        :return: True if the voter is eligible, False otherwise.
        '''
        with open('eligible_voters.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['First Name'] == first_name and row['Last Name'] == last_name and row['ID'] == voter_id:
                    return True
        return False

    def has_already_voted(self, first_name: str, last_name: str, voter_id: str) -> bool:
        '''
        Checks if the voter has already voted by searching the voters_log.csv file.

        :param first_name: Voter's first name.
        :param last_name: Voter's last name.
        :param voter_id: Voter's ID.
        :return: True if the voter has already voted, False otherwise.
        '''
        with open(self.voters_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['First Name'] == first_name and row['Last Name'] == last_name and row['ID'] == voter_id:
                    return True
        return False

    def log_voter(self, first_name: str, last_name: str, voter_id: str) -> None:
        '''
        Logs the voter's information in the voters_log.csv file after a successful vote submission.

        :param first_name: Voter's first name.
        :param last_name: Voter's last name.
        :param voter_id: Voter's ID.
        '''
        with open(self.voters_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, voter_id])

    def clear_inputs(self) -> None:
        '''
        Clears the input fields and resets the radio buttons in the form.
        '''
        self.lineEdit_FirstName.clear()
        self.lineEdit_LastName.clear()
        self.lineEdit_ID.clear()

        # Reset radio buttons
        self.radioButton_John.setAutoExclusive(False)
        self.radioButton_Alice.setAutoExclusive(False)
        self.radioButton_Bob.setAutoExclusive(False)

        self.radioButton_John.setChecked(False)
        self.radioButton_Alice.setChecked(False)
        self.radioButton_Bob.setChecked(False)

        self.radioButton_John.setAutoExclusive(True)
        self.radioButton_Alice.setAutoExclusive(True)
        self.radioButton_Bob.setAutoExclusive(True)