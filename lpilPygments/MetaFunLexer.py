
from pygments.lexer import \
  RegexLexer, bygroups, using, inherit, words
from pygments.lexers.markup import TexLexer
from pygments.token import \
  Error, Name, Number, Punctuation, \
  Keyword, Whitespace, Generic, _TokenType, \
  String

class MetaFunLexer(RegexLexer) :
  """
  Lexer for the MetaPost/MetaFun diagram typesetting langauge.
  """
  name = 'MetaFun'

  tokens = {
    'root' : [
      (r'(\-|\+)?[0-9\.]+', Number),
      (r'\(\)\[\]\^\%\&\*\$\!\|\{\}\~\#\@\?\>\<\,\./\\', Punctuation),
      (words(('draw', 'drawarrow'), suffix=r'\b'), Name.Builtin),
      (r"'", String, 'single-quote'),
      (r'"', String, 'double-quote'),
      (r'`', String, 'back-tick'),
      (r'\s+', Whitespace),
      (r'\S+', Generic)
    ],
    'single-quote' : [ (r"[^']+", String), (r"'", String, '#pop') ],
    'double-quote' : [ (r'[^"]+', String), (r'"', String, '#pop') ],
    'back-tick'    : [ (r'[^`]+', String), (r'`', String, '#pop') ]
  }

class TexMetaFunLexer(TexLexer) :
  """
  Lexer for TeX/LaTex which understands embedded \startMPxxxx \stopMPxxxx
  MetaPost/MetaFun enivronments.
  """
  name = "TexMetaFun"

  """
    \startMPcalculation \stopMPcalculation
    \startMPclip \stopMPclip
    \startMPcode  \stopMPcode
    \startMPdefinitions \stopMPdefinitions
    \startMPdrawing  \stopMPdrawing
    \startMPextensions \stopMPextensions
    \startMPinitializations \stopMPinitializations
    \startMPpage  \stopMPpage
    \startMPpositiongraphic \stopMPpositiongraphic
    \startMPrun \stopMPruns
    \startuseMPgraphic \stopuseMPgrapic

    metaPostEnvironments = [
      'calculation', 'clip', 'code',
      'definitions', 'drawing',
      'extensions',  'initializations',
      'page', 'positiongraphic', 'run'
    ]
  """

  tokens = {
    'root' : [
      (r'(\\startMP\S+)', Keyword, 'meta-post-content'),
      inherit,
    ],
    'meta-post-content': [
      (
        r'(?s:(.+?))(\\stopMP\S+)',
        bygroups(using(MetaFunLexer), Keyword)
      )
    ]
  }
