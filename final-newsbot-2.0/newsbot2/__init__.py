"""NewsBot Intelligence System 2.0 — responsible, evidence-first NLP."""
__version__ = '2.0.0'
from .engine import NewsBotEngine
from .schemas import Article
__all__ = ['NewsBotEngine', 'Article']
