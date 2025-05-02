# hello_activity.py
import logging

def main(name: str) -> str:
    logging.info(f'Saying hello to {name}')
    return f'Hello, {name}!'