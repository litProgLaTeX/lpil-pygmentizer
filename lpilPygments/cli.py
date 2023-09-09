
import os
import re
import sys
import yaml

from pygments import highlight
from pygments.lexers import get_lexer_by_name, \
  load_lexer_from_file
from pygments.formatters import get_formatter_by_name

#from pygments.formatters import LatexFormatter
#from pygments.lexer import RegexLexer, bygroups, using, inherit, words
#from pygments.lexers import PythonLexer
#from pygments.lexers.markup import TexLexer
#from pygments.token import \
#  Error, Name, Number, Punctuation, \
#  Keyword, Whitespace, Generic, _TokenType, \
#  String

metaFunLexerStr = os.path.join(
  os.path.dirname(__file__),
  'MetaFunLexer.py'
) + ':TexMetaFunLexer'

knownLpilLexers = {
  'metafun'         : metaFunLexerStr,
  'metafunlexer'    : metaFunLexerStr,
  'texmetafun'      : metaFunLexerStr,
  'texmetafunlexer' : metaFunLexerStr,
}

def usage() :
  print("""
  usage: lpilPygmentizer [-h,--help] <lexerName> <inputFile> <outputFile> [<options>]

  where:

    lexerName   is the name of a builtin Pygments Lexer 
                OR one of:

                  MetaFunLexer
              
    inputFile   is the path to a file to be pygmentized
    
    outputFile  is the path to a file to which to write the pygmentized result.
  
    options     (optional) collection of pygments LaTeX formatter options

  options:
    -h, --help   This help text

  """)
  exit(1)

def cli() :
  if len(sys.argv) < 4 : usage()
  if -1 < sys.argv[1].find('-h') : usage()

  lexerName  = sys.argv[1]
  inputPath  = sys.argv[2]
  outputPath = sys.argv[3]

  opts = None
  if 4 < len(sys.argv) :
    opts = sys.argv[4]

  print( "lpilPygmentizer")
  print(f"    from: {inputPath}")
  print(f"       to: {outputPath}")
  print(f"    using: {lexerName}")
  if opts : print(f"  options: {opts}")

  if lexerName.lower() in knownLpilLexers :
    lexerName = knownLpilLexers[lexerName.lower()]
  elif lexerName.lower().endswith('lexer') :
    lexerName = lexerName.lower().removesuffix('lexer')

  theLexer = None
  if -1 < lexerName.find(':') :
    # we have a relative path and a className
    lexerPath, lexerName = lexerName.split(':')
    try : 
      theLexer = load_lexer_from_file(lexerPath, lexername=lexerName)
    except Exception as err :
      print(repr(err))
  else :
    # we might have a lexer alias
    try :
      theLexer = get_lexer_by_name(lexerName)
    except err1 :
      print(repr(err1))
      try :
        theLexer = load_lexer_from_file(lexerName)
      except err2 :
        print(repr(err2))
  
  if not theLexer :
    print("We could not load any lexers!")
    sys.exit(1)

  formatterOptions = {
    'style' : 'sas'
  }
  if opts :
    for anOptPair in opts.split(',') :
      aKey, aValue = anOptPair.split('=')
      formatterOptions[aKey] = aValue

  theFormatter = get_formatter_by_name(
    'latex', **formatterOptions
  )

  with open(inputPath) as inFile :
    inputStr = inFile.read()

  highLightedStr = highlight(
    inputStr,
    theLexer,
    theFormatter,

  )

  with open(outputPath, 'w') as outFile :
    outFile.write(highLightedStr)
  