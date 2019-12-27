import re

from pylint.interfaces import IRawChecker
from pylint.checkers import BaseChecker

todo_comment_regex = re.compile('^(?!.*tracker.yandex.ru/VPAGROUPDEV-[0-9]+).*TODO.*$')


class ToDoChecker(BaseChecker):
    __implements__ = IRawChecker

    name = 'todo_ticket'
    msgs = {
        'C0777': (
            'Include tracker ticket to your TODOs',
            'todo-no-ticket',
            'Some of your TODOs doesn\'t have tracker ticket'
        ),
    }
    options = ()

    def process_module(self, node):
        with node.stream() as stream:
            for (lineno, line) in enumerate(stream):
                if todo_comment_regex.match(str(line)):
                    self.add_message('todo-no-ticket', line=lineno)


def register(linter):
    linter.register_checker(ToDoChecker(linter))

