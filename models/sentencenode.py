class SuspectedSentenceNode:
    def __init__(self, file_path, line_no, script, private_word_list, purpose):
        self.file_path = file_path
        self.line_no = line_no
        self.script = script
        self.private_word_list = private_word_list
        self.purpose = purpose

    def __str__(self):
        return self.file_path + ' ' + str(self.line_no) + '\n' + str(self.private_word_list) + ' ' + self.purpose

    def __eq__(self, other):
        return self.file_path == other.file_path and self.line_no == other.line_no
