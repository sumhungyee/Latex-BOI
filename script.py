import telebot
import subprocess
import pdf2image
import glob
import os
import uuid
from dotenv import load_dotenv
from threading import Thread, Lock



TEMPLATE = """
\\documentclass[border=2pt, varwidth={varwidth}cm]{{standalone}}
\\usepackage{{amsfonts, amssymb, amsmath, amsthm}}
\\usepackage{{tikz}}
\\usepackage{{listings}}
\\usetikzlibrary{{shapes, arrows, calc, positioning}}
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.18}}

\\newtheorem{{lemma}}{{Lemma}}
\\newtheorem{{theorem}}{{Theorem}}
\\newtheorem{{statement}}{{Statement}}
\\newtheorem{{remark}}{{Remark}}
\\newenvironment{{solution}}
  {{\\renewcommand\\qedsymbol{{$\\blacksquare$}}\\begin{{proof}}[Solution]}}
  {{\end{{proof}}}}


\\newcommand{{\\LaTeXbOi}}{{%
  L\\kern-.36em{{\\raise.3ex\\hbox{{\\scriptsize A}}}}% 
  \\kern-.15em\\TeX%
  \\kern-.15em\\raise-.2ex\\hbox{{B}}%
  \\kern-.2em{{\\raise-.5ex\\hbox{{\\scriptsize O}}}}%
  \\kern-.15em I%
}}

\\begin{{document}}
{latex}
\\end{{document}}
"""
class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        print(exception)
        return True
load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEBOT_TOKEN"),  exception_handler=ExceptionHandler(), threaded=True)
jobs = 0
lock = Lock()


def split_string(s, max_len=3950):
    return [s[i:i+max_len] for i in range(0, len(s), max_len)]

def send_pic(latex_content, msg, varwidth=7.5, dpi = 1000):
    global jobs

    with lock:
        jobid = str(uuid.uuid4())
        jobs += 1

        with open(f'{jobid}.tex', 'w') as file:
            try:
                file.write(TEMPLATE.format(latex=latex_content, varwidth=varwidth))
            except Exception as e:
                bot.reply_to(msg, f"Error compiling LaTeX. Error: {e}\n")
                clear_files_and_decrement(jobid)
                return
    

    result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", f"-jobname={jobid}", f"{jobid}.tex"],
            capture_output=True,
            text=True
    )

    if result.returncode != 0:
        output = "Error compiling LaTeX. Check your code.\n"
        bot.reply_to(msg, output, parse_mode='Markdown')
        error_printing = []
        if result.stdout:
            stdout = result.stdout.splitlines()
            for i, line in enumerate(stdout):
                if line.startswith("!"):
                    error_printing.append(line)
            error_string = "\n".join(error_printing)
            error_string_split = split_string(error_string)
            for substr in error_string_split:
                bot.reply_to(msg, f"```\n{substr}\n```", parse_mode='Markdown')
        
        clear_files_and_decrement(jobid)
        return

    iter_dpi = dpi

    for i in range(5):
        print(f"Try: {i+1}" )
        images = pdf2image.convert_from_path(f'{jobid}.pdf', dpi=iter_dpi, single_file=True)
        code = None
        try:
            code = bot.send_photo(chat_id=msg.chat.id, photo=images[0])
        except:
            iter_dpi = int(0.75 * iter_dpi)
        if code is not None:
            # clear files
            clear_files_and_decrement(jobid)
            return
    bot.reply_to(msg, "Error sending photo: Probably too large!")
    # clear files
    clear_files_and_decrement(jobid)


def clear_files_and_decrement(jobid):
    global jobs
    with lock:
        for f in glob.glob(f"{jobid}.*"):
            os.remove(f)
        jobs -= 1


@bot.message_handler(commands = ["latex"])
def equations(msg):
    content = msg.text.replace("/latex", "").strip()
    if "$" in content or r"\(" in content:
        latex_content = content
    else:
        latex_content = r"\(\displaystyle{" + f"{content}" + r"}\)"
    send_pic(latex_content, msg)
    
@bot.message_handler(commands = ["text"])
def equations(msg):
    content = msg.text.replace("/text", "").strip()
    if len(content) <= 75:
        send_pic(content, msg, varwidth=5, dpi=1000)
    elif len(content) <= 300:
        send_pic(content, msg)
    elif len(content) <= 1000:
        send_pic(content, msg, 10, dpi=800)
    elif len(content) <= 2000:
        send_pic(content, msg, 16, dpi=700)
    else:
        send_pic(content, msg, 21, dpi=500)
    
@bot.message_handler(commands = ["hi"])
def greet(msg):
    content = r"""Hello there! I am \LaTeXbOi! Use me to print \LaTeX!""" 
    send_pic(content, msg, varwidth=5)
    bot.reply_to(msg, content)

@bot.message_handler(commands = ["help"])
def help(msg):
    content = r"""
    \section{Help}
    Hello there, I am \LaTeXbOi and I am here to \colorbox{green}{help} you! I am currently (supposed to be) hosted on a cloud instance, 
    so I will be slaving for you 24/7 :(
    \subsection{Commands}
    \begin{enumerate}
    \item \texttt{/help}. Obvious
    \item \texttt{/hi}. Say hi!
    \item \texttt{/text <content>}. Assumes you are typing text! This probably works best for most cases!
    \item \texttt{/latex <equation>}. Assumes you are typing a short equation (and you are lazy)!
    \end{enumerate}
    \subsection{This is All Compiled!}
    By the way, this is compiled too!
    \subsection{Currently Installed}
    \begin{enumerate}
    \item amsfonts, amssymb, amsmath, amsthm
    \item tikz
        \begin{enumerate}
            \item shapes 
            \item arrows 
            \item calc 
            \item positioning
        \end{enumerate}
    \item listings
    \item pgfplots (1.18)
    \end{enumerate}
    """ 
    send_pic(content, msg, varwidth=12, dpi = 600)


bot.infinity_polling(timeout = 2, long_polling_timeout=5)
