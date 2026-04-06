from __future__ import annotations

import subprocess
import sys
import unittest

from src.paste_parser import parse_paste_order, parse_price
from src.todos import default_todos


class PasteParserAndTodoTests(unittest.TestCase):
    def test_parse_price_supports_dollar_prefixed_values(self) -> None:
        self.assertEqual(parse_price('BUY NQ @ $19,245.75 FTMO'), 19245.75)

    def test_parse_order_detects_price_and_firm(self) -> None:
        parsed = parse_paste_order('Filled at $3,450.25 on Apex challenge account')
        self.assertEqual(parsed.price, 3450.25)
        self.assertEqual(parsed.prop_firm, 'Apex Trader Funding')

    def test_default_todos_include_requested_items(self) -> None:
        titles = {item.title for item in default_todos()}
        self.assertIn('Build leaderboard page', titles)
        self.assertIn('Fix AI paste parser', titles)

    def test_cli_todos_and_parse_paste_commands(self) -> None:
        todos_result = subprocess.run(
            [sys.executable, '-m', 'src.main', 'todos'],
            check=True,
            capture_output=True,
            text=True,
        )
        parse_result = subprocess.run(
            [sys.executable, '-m', 'src.main', 'parse-paste', 'Entry $4,210.50 on FTMO account'],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn('Updated Todos', todos_result.stdout)
        self.assertIn('Build leaderboard page', todos_result.stdout)
        self.assertIn('price=4210.5', parse_result.stdout)
        self.assertIn('prop_firm=FTMO', parse_result.stdout)


if __name__ == '__main__':
    unittest.main()
