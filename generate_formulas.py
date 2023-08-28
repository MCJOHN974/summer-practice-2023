import os
from dotenv import load_dotenv
import openai
import time
from multiprocessing import Pool
import time
import random
from process_generated_formulas import concat_and_process_files

# environmental variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_TOKEN')

TOTAL_REQUESTS = 200
THREADS = 16
PROMPT_TOKEN_PRICE = 0.00015  # cents
REPLY_TOKEN_PRICE = 0.0002  # cents


def get_open_ai_answer(prompt):
    # start_time = time.time()
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'system', 'content': prompt}],
        temperature = 1,
        stream=False
    )
    answer = response['choices'][0]['message']['content']
    # end_time = time.time()
    # print(answer)
    # print(f"Time spent: {end_time - start_time:.3f} Price: {response['usage']['prompt_tokens'] * PROMPT_TOKEN_PRICE + response['usage']['completion_tokens'] * REPLY_TOKEN_PRICE:.3f}c")

    return answer, response['usage']['prompt_tokens'] * PROMPT_TOKEN_PRICE + response['usage']['completion_tokens'] * REPLY_TOKEN_PRICE


def latex_generator(outp_path):
    start_time = time.time()
    time.sleep(random.random() * 30)
    print(outp_path, 'starting')

    for i in range(TOTAL_REQUESTS):
        try:
            ans, price = get_open_ai_answer(get_rand_prompt_like_article())
            print(outp_path, f"{i + 1}/{TOTAL_REQUESTS} elapsed: {time.time() - start_time:.2f} price: {price}")
        except Exception:
            continue
        with open(outp_path, 'a') as f:
            f.write(ans + '\n')


def get_const_prompt():
    res = """Generate 25 latex formulas. Only write formulas in list without any extra text.
Write only unique formulas. Be VERY creative, imagine unusual formulas.
Try to make complex formulas that could have been seen in an scientific paper.

Use these as an example but DONT USE THEM DIRECTLY:
\\lambda ^ { i } = \\left( \\begin{array} { c } { \\lambda _ { L } ^ { i } } \\\\ { \\epsilon ^ { i j } \\bar { \\lambda } _ { L \\, j } } \\\\ \\end{array} \\right)
B = \\frac { ( n - 1 ) ^ { 2 } } { 4 \\pi ^ { 2 } a ^ { 4 } } ( - \\frac { x _ { 0 } } { 8 } + \\frac { 6 5 } { 2 0 4 8 } \\pi ) , ~ ~ ~ ~ x _ { 0 } \\rightarrow \\infty .
m _ { a b } ^ { q } ( 2 r + 1 + \\epsilon _ { a b } ) = q ^ { 2 r + 1 + \\epsilon _ { a b } } ( \\lambda _ { b } , \\sigma ^ { - r } \\phi _ { a } ) , \\ \\ \\ r \\in { \\bf Z } .
\\mathrm { T r } \\operatorname { l n } \\left( - { \\frac { d ^ { 2 } } { d t ^ { 2 } } } + m ^ { 2 } \\right) = - \\int _ { 0 } ^ { \\infty } { \\frac { d \\tau } { \\tau } } \\int _ { 0 } ^ { \\beta } d t \\; K ( 0 ; \\tau ) \\; ,
\\zeta \\left( b \\right) \\equiv \\left\\{ z \\in { \\cal Z } \\left( b \\right) \\mid z \\subset { \\cal B } \\left( X \\right) \\right\\} = { \\cal Z } \\left( b \\right) \\cap { \\cal B } \\left( X \\right) \\quad ,
\\tilde { \\omega } ( S _ { k } ) = ( - 1 ) ^ { k } \\, \\Lambda _ { k } , \\ \\ k \\geq 0 \\ ,"""
    return res


def get_rand_prompt_gpt():
    possible = [
        "Provide 25 calculus-based LaTeX mathematical formulas that haven't been generated before and are different from any previously generated formulas.\n"
        "Generate 25 LaTeX formulas focused on linear algebra concepts, ensuring they are different from any previously generated formulas.\n"
        "Provide 25 mathematical expressions in LaTeX related to differential equations, ensuring uniqueness from prior outputs.\n"
        "Generate 25 unique LaTeX formulas based on geometry and trigonometry that are distinct from previously generated ones.\n"
        "Provide 25 LaTeX mathematical formulas associated with probability and statistics, different from any that have been generated before.\n"
        "Generate 25 unique number theory formulas in LaTeX format, ensuring they are distinct from prior outputs.\n"
        "Create 25 complex analysis mathematical expressions using LaTeX that haven't been produced before.\n"
        "Provide 25 LaTeX formulas related to discrete mathematics and combinatorics, ensuring they differ from previously generated formulas.\n"
        "Generate 25 mathematical expressions in LaTeX dealing with topology, distinct from any that have been generated before.\n"
        "Provide 25 LaTeX formulas centered on mathematical physics concepts, ensuring they haven't been generated before.\n"
        "Generate 25 abstract algebra LaTeX mathematical expressions, making sure they differ from previous generations.\n"
        "Construct 25 mathematical formulas in LaTeX focusing on group theory, different from any that have been generated before.\n"
        "Provide 25 LaTeX mathematical formulas based on numerical methods, ensuring they are unique from previous outputs.\n"
        "Generate 25 mathematical expressions in LaTeX related to mathematical logic, distinct from previously generated formulas.\n"
        "Illustrate 25 LaTeX formulas connected to optimization and operations research, different from any that have been generated before.\n"
        "Generate 25 mathematical expressions in LaTeX that deal with functional analysis, ensuring they differ from prior outputs.\n"
        "Provide 25 mathematical formulas in LaTeX format that are related to real analysis concepts and are different from any previously generated formulas.\n"
        "Construct 25 LaTeX formulas associated with graph theory concepts, ensuring they haven't been produced before.\n"
        "Generate 25 LaTeX mathematical expressions related to set theory, making sure they are distinct from previous generations.\n"
        "Produce 25 mathematical formulas in LaTeX that deal with cryptography principles, ensuring they are different from any previously generated formulas.\n"
    ]

    examples = [
        "\\alpha _ { 1 } ^ { r } \\gamma _ { 1 } + \\dots + \\alpha _ { N } ^ { r } \\gamma _ { N } = 0 \\quad ( r = 1 , . . . , R ) \\; ,",
        "\\eta = - \\frac { 1 } { 2 } \\operatorname { l n } \\left( \\frac { \\operatorname { c o s h } \\left( \\sqrt { 2 } b _ { \\infty } \\sqrt { 1 + \\alpha ^ { 2 } } \\; y - \\mathrm { a r c s i n h } \\; \\alpha \\right) } { \\sqrt { 1 + \\alpha ^ { 2 } } } \\right)",
        " _ { ( 2 ) } ^ { - } = \\int \\beta d \\beta d ^ { 9 } p d ^ { 8 } \\lambda \\Phi ( - p , - \\lambda ) \\left( - \\frac { p ^ { I } p ^ { I } } { 2 \\beta } \\right) \\Phi ( p , \\lambda ) \\, .",
        "\\Gamma ( z + 1 ) = \\int _ { 0 } ^ { \\infty } \\, \\, d x \\, \\, e ^ { - x } x ^ { z } .",
        "\\frac { d } { d s } { \\bf C } _ { i } = \\frac { 1 } { 2 } \\epsilon _ { i j k } { \\bf C } _ { j } \\times { \\bf C } _ { k } \\, .",
        " = \\sum _ { s p i n s } \\prod _ { c u b e s } W ( a | e , f , g | b , c , d | h ) ,",
        "\\left\\{ Q ^ { i } , Q ^ { j } \\right\\} = c ^ { i j } \\Gamma ^ { M } C P _ { M } + C c ^ { i j } Z ,",
        "\\breve { c } _ { n , \\nu } = \\sum _ { m = n } ^ { 2 n } { \\frac { \\Gamma \\left( \\nu + m - { \\frac { D - 1 } { 2 } } \\right) } { \\Gamma \\left( \\nu + n - { \\frac { D - 1 } { 2 } } \\right) } } ~ \\breve { a } _ { 2 ( m - n ) , m } ~ ~ ~ .",
        " ( g ) = - f \\left[ 3 \\left[ ( \\operatorname { l n } f ) ^ { \\prime } \\right] ^ { 2 } + \\frac { \\Lambda ( x ^ { 5 } ) } { M ^ { 3 } } \\right] \\; ,",
        "{ \\frac { d } { d s } } { \\frac { 1 } { \\Gamma ( - s ) } } \\bigg | _ { s = 0 } = - 1 ,",
        "\\dot { z } _ { 1 } = - N ^ { z } ( z _ { 1 } ) = - g ( z _ { 1 } ) = - \\frac { z _ { 1 } } { P _ { z } ( z _ { 2 } - z _ { 1 } ) } ; ~ ~ ~ \\dot { z } _ { 2 } = - \\frac { z _ { 2 } } { P _ { z } ( z _ { 2 } - z _ { 1 } ) }",
        " _ { \\alpha } = \\sum _ { \\beta \\in \\Lambda _ { R } } \\epsilon ( \\alpha , \\beta ) | \\beta + \\bar { p } > < \\beta + \\bar { p } |",
        "{ \\cal L } = - { \\frac { 1 } { 4 } } F _ { \\mu \\nu } F ^ { \\mu \\nu } + { \\bar { \\psi } } ( i \\gamma ^ { \\mu } D _ { \\mu } - m ) \\psi \\, ,",
        " ^ { i { \\bf k \\cdot r } } = e ^ { i k r \\operatorname { c o s } ( \\theta - \\Theta ) } = \\sum _ { l = - \\infty } ^ { \\infty } i ^ { l } \\, J _ { l } ( k r ) \\, e ^ { i l ( \\theta - \\Theta ) } \\, ,",
        " \\sqrt { 2 } \\partial _ { - } \\chi - g [ \\phi , \\psi ] = 0 , \\quad \\partial _ { - } ^ { 2 } \\bar { A } _ { + } - g ^ { 2 } J ^ { + } = 0 .",
        "\\Omega _ { k } ^ { ( l ) } = \\sum _ { s = 0 } \\int d ^ { 3 } y \\left( ( - 1 ) ^ { s + 1 } \\frac { d ^ { s } } { d t ^ { s } } \\phi _ { k } ^ { i ( s ) } ( x , y ) L _ { i } ^ { ( 0 ) } ( y ) \\right) .",
        " _ { g } ^ { ' } \\Bigl ( v ( h ) \\Bigr ) = v ( L _ { g } h ) = v ( g h ) \\, , \\, \\, \\, \\forall g , h \\in G ,",
        "\\xi ^ { 2 } = \\left( \\frac { \\varepsilon _ { 1 } - \\varepsilon _ { 2 } } { \\varepsilon _ { 1 } + \\varepsilon _ { 2 } } \\right) ^ { 2 } = \\left( \\frac { \\mu _ { 1 } - \\mu _ { 2 } } { \\mu _ { 1 } + \\mu _ { 2 } } \\right) ^ { 2 } ,",
        " ( e _ { 1 } ) = \\epsilon ^ { - J _ { 6 7 } + J _ { 8 9 } } , \\quad R ( e _ { 2 } ) = \\epsilon ^ { J _ { 4 5 } - J _ { 8 9 } } .",
        "{ \\tilde { \\cal { E } } } _ { m < 0 } = { \\cal { E } } _ { m < 0 } ( B ) - { \\cal { E } } ( 0 ) = \\frac { B ^ { 2 } } { 2 } + \\frac { ( e B ) ^ { \\frac { 3 } { 2 } } } { 2 \\pi } g \\left( \\frac { e B } { m ^ { 2 } } \\right) \\, ,",
    ]

    return random.choice(possible) + "example:\n" + '\n'.join(random.sample(examples, 5))


def get_rand_prompt_like_article():
    subsections = ['Astrophysics of Galaxies', 'Cosmology and Nongalactic Astrophysics', 'Earth and Planetary Astrophysics', 'High Energy Astrophysical Phenomena', 'Instrumentation and Methods for Astrophysics', 'Solar and Stellar Astrophysics', 'Disordered Systems and Neural Networks', 'Materials Science', 'Mesoscale and Nanoscale Physics', 'Other Condensed Matter', 'Quantum Gases', 'Soft Condensed Matter', 'Statistical Mechanics', 'Strongly Correlated Electrons', 'Superconductivity', 'Adaptation and Self-Organizing Systems', 'Cellular Automata and Lattice Gases', 'Chaotic Dynamics', 'Exactly Solvable and Integrable Systems', 'Pattern Formation and Solitons', 'Accelerator Physics', 'Applied Physics', 'Atmospheric and Oceanic Physics', 'Atomic and Molecular Clusters', 'Atomic Physics', 'Biological Physics', 'Chemical Physics', 'Classical Physics', 'Computational Physics', 'Data Analysis, Statistics and Probability', 'Fluid Dynamics', 'General Physics', 'Geophysics', 'History and Philosophy of Physics', 'Instrumentation and Detectors', 'Medical Physics', 'Optics', 'Physics and Society', 'Physics Education', 'Plasma Physics', 'Popular Physics', 'Space Physics', 'Quantum Physics', 'Algebraic Geometry', 'Algebraic Topology', 'Analysis of PDEs', 'Category Theory', 'Classical Analysis and ODEs', 'Combinatorics', 'Commutative Algebra', 'Complex Variables', 'Differential Geometry', 'Dynamical Systems', 'Functional Analysis', 'General Mathematics', 'General Topology', 'Geometric Topology', 'Group Theory', 'History and Overview', 'Information Theory', 'K-Theory and Homology', 'Logic', 'Mathematical Physics', 'Metric Geometry', 'Number Theory', 'Numerical Analysis', 'Operator Algebras', 'Optimization and Control', 'Probability', 'Quantum Algebra', 'Representation Theory', 'Rings and Algebras', 'Spectral Theory', 'Statistics Theory', 'Symplectic Geometry', 'Artificial Intelligence', 'Computation and Language', 'Computational Complexity', 'Computational Engineering, Finance, and Science', 'Computational Geometry', 'Computer Science and Game Theory', 'Computer Vision and Pattern Recognition', 'Computers and Society', 'Cryptography and Security', 'Data Structures and Algorithms', 'Databases', 'Digital Libraries', 'Discrete Mathematics', 'Distributed, Parallel, and Cluster Computing', 'Emerging Technologies', 'Formal Languages and Automata Theory', 'General Literature', 'Graphics', 'Hardware Architecture', 'Human-Computer Interaction', 'Information Retrieval', 'Information Theory', 'Logic in Computer Science', 'Machine Learning', 'Mathematical Software', 'Multiagent Systems', 'Multimedia', 'Networking and Internet Architecture', 'Neural and Evolutionary Computing', 'Numerical Analysis', 'Operating Systems', 'Other Computer Science', 'Performance', 'Programming Languages', 'Robotics', 'Social and Information Networks', 'Software Engineering', 'Sound', 'Symbolic Computation', 'Systems and Control', 'Biomolecules', 'Cell Behavior', 'Genomics', 'Molecular Networks', 'Neurons and Cognition', 'Other Quantitative Biology', 'Populations and Evolution', 'Quantitative Methods', 'Subcellular Processes', 'Tissues and Organs', 'Computational Finance', 'Economics', 'General Finance', 'Mathematical Finance', 'Portfolio Management', 'Pricing of Securities', 'Risk Management', 'Statistical Finance', 'Trading and Market Microstructure', 'Applications', 'Computation', 'Machine Learning', 'Methodology', 'Other Statistics', 'Statistics Theory', 'Audio and Speech Processing', 'Image and Video Processing', 'Signal Processing', 'Systems and Control', 'Econometrics', 'General Economics', 'Theoretical Economics']
    examples = [
        "\\alpha _ { 1 } ^ { r } \\gamma _ { 1 } + \\dots + \\alpha _ { N } ^ { r } \\gamma _ { N } = 0 \\quad ( r = 1 , . . . , R ) \\; ,",
        "\\eta = - \\frac { 1 } { 2 } \\operatorname { l n } \\left( \\frac { \\operatorname { c o s h } \\left( \\sqrt { 2 } b _ { \\infty } \\sqrt { 1 + \\alpha ^ { 2 } } \\; y - \\mathrm { a r c s i n h } \\; \\alpha \\right) } { \\sqrt { 1 + \\alpha ^ { 2 } } } \\right)",
        " _ { ( 2 ) } ^ { - } = \\int \\beta d \\beta d ^ { 9 } p d ^ { 8 } \\lambda \\Phi ( - p , - \\lambda ) \\left( - \\frac { p ^ { I } p ^ { I } } { 2 \\beta } \\right) \\Phi ( p , \\lambda ) \\, .",
        "\\Gamma ( z + 1 ) = \\int _ { 0 } ^ { \\infty } \\, \\, d x \\, \\, e ^ { - x } x ^ { z } .",
        "\\frac { d } { d s } { \\bf C } _ { i } = \\frac { 1 } { 2 } \\epsilon _ { i j k } { \\bf C } _ { j } \\times { \\bf C } _ { k } \\, .",
        " = \\sum _ { s p i n s } \\prod _ { c u b e s } W ( a | e , f , g | b , c , d | h ) ,",
        "\\left\\{ Q ^ { i } , Q ^ { j } \\right\\} = c ^ { i j } \\Gamma ^ { M } C P _ { M } + C c ^ { i j } Z ,",
        "\\breve { c } _ { n , \\nu } = \\sum _ { m = n } ^ { 2 n } { \\frac { \\Gamma \\left( \\nu + m - { \\frac { D - 1 } { 2 } } \\right) } { \\Gamma \\left( \\nu + n - { \\frac { D - 1 } { 2 } } \\right) } } ~ \\breve { a } _ { 2 ( m - n ) , m } ~ ~ ~ .",
        " ( g ) = - f \\left[ 3 \\left[ ( \\operatorname { l n } f ) ^ { \\prime } \\right] ^ { 2 } + \\frac { \\Lambda ( x ^ { 5 } ) } { M ^ { 3 } } \\right] \\; ,",
        "{ \\frac { d } { d s } } { \\frac { 1 } { \\Gamma ( - s ) } } \\bigg | _ { s = 0 } = - 1 ,",
        "\\dot { z } _ { 1 } = - N ^ { z } ( z _ { 1 } ) = - g ( z _ { 1 } ) = - \\frac { z _ { 1 } } { P _ { z } ( z _ { 2 } - z _ { 1 } ) } ; ~ ~ ~ \\dot { z } _ { 2 } = - \\frac { z _ { 2 } } { P _ { z } ( z _ { 2 } - z _ { 1 } ) }",
        " _ { \\alpha } = \\sum _ { \\beta \\in \\Lambda _ { R } } \\epsilon ( \\alpha , \\beta ) | \\beta + \\bar { p } > < \\beta + \\bar { p } |",
        "{ \\cal L } = - { \\frac { 1 } { 4 } } F _ { \\mu \\nu } F ^ { \\mu \\nu } + { \\bar { \\psi } } ( i \\gamma ^ { \\mu } D _ { \\mu } - m ) \\psi \\, ,",
        " ^ { i { \\bf k \\cdot r } } = e ^ { i k r \\operatorname { c o s } ( \\theta - \\Theta ) } = \\sum _ { l = - \\infty } ^ { \\infty } i ^ { l } \\, J _ { l } ( k r ) \\, e ^ { i l ( \\theta - \\Theta ) } \\, ,",
        " \\sqrt { 2 } \\partial _ { - } \\chi - g [ \\phi , \\psi ] = 0 , \\quad \\partial _ { - } ^ { 2 } \\bar { A } _ { + } - g ^ { 2 } J ^ { + } = 0 .",
        "\\Omega _ { k } ^ { ( l ) } = \\sum _ { s = 0 } \\int d ^ { 3 } y \\left( ( - 1 ) ^ { s + 1 } \\frac { d ^ { s } } { d t ^ { s } } \\phi _ { k } ^ { i ( s ) } ( x , y ) L _ { i } ^ { ( 0 ) } ( y ) \\right) .",
        " _ { g } ^ { ' } \\Bigl ( v ( h ) \\Bigr ) = v ( L _ { g } h ) = v ( g h ) \\, , \\, \\, \\, \\forall g , h \\in G ,",
        "\\xi ^ { 2 } = \\left( \\frac { \\varepsilon _ { 1 } - \\varepsilon _ { 2 } } { \\varepsilon _ { 1 } + \\varepsilon _ { 2 } } \\right) ^ { 2 } = \\left( \\frac { \\mu _ { 1 } - \\mu _ { 2 } } { \\mu _ { 1 } + \\mu _ { 2 } } \\right) ^ { 2 } ,",
        " ( e _ { 1 } ) = \\epsilon ^ { - J _ { 6 7 } + J _ { 8 9 } } , \\quad R ( e _ { 2 } ) = \\epsilon ^ { J _ { 4 5 } - J _ { 8 9 } } .",
        "{ \\tilde { \\cal { E } } } _ { m < 0 } = { \\cal { E } } _ { m < 0 } ( B ) - { \\cal { E } } ( 0 ) = \\frac { B ^ { 2 } } { 2 } + \\frac { ( e B ) ^ { \\frac { 3 } { 2 } } } { 2 \\pi } g \\left( \\frac { e B } { m ^ { 2 } } \\right) \\, ,",
    ]
    chosen_examples = "\n".join(random.sample(examples, 5))
    prompt = f"""Generate 35 latex formulas. Only write formulas in list without any extra text.
Write only unique formulas that are different from any previously generated. Be VERY creative, imagine unusual formulas.
Make complex formulas that could have been be found on https://arxiv.org/ in subsection {random.choice(subsections)}

Here is an example:
{chosen_examples}"""
    return prompt


if __name__ == "__main__":
    pool = Pool(THREADS)
    dir_path = 'data/article_prompts_big'
    os.makedirs(dir_path, exist_ok=True)
    outp_paths = [dir_path + f'/result_{i+1}.txt' for i in range(16)]

    print('starting to generate')
    for result in pool.imap_unordered(latex_generator, outp_paths):
        pass

    print('counting_results')
    concat_and_process_files(outp_paths, dir_path)
