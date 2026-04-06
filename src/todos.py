from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TodoItem:
    title: str
    detail: str
    status: str = 'todo'


_DEFAULT_TODOS: tuple[TodoItem, ...] = (
    TodoItem('Build leaderboard page', 'Create the leaderboard page shell and data bindings.'),
    TodoItem('Add PnL calendar', 'Add a PnL calendar with payout summary image support and total payouts per firm.'),
    TodoItem('Fix accounts page', 'Auto-add from orders, add firm selector, and add status picker.'),
    TodoItem('Fix orders page', 'Add a firm dropdown selector.'),
    TodoItem('Fix AI paste parser', 'Detect price values (including $-prefixed prices) and prop firm names correctly.'),
)


def default_todos() -> tuple[TodoItem, ...]:
    return _DEFAULT_TODOS


def render_todos() -> str:
    lines = ['Updated Todos', '']
    lines.extend(f'- [{item.status}] {item.title} — {item.detail}' for item in default_todos())
    return '\n'.join(lines)
