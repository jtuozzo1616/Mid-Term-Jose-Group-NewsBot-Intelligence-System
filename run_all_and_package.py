#!/usr/bin/env python3
"""Run notebook, verify real empirical evidence, write report, and package the artifact.

Google Colab: upload and unzip the project ZIP, install its dependencies, then run
python run_all_and_package.py. Notebook setup uses IPython magic and may need internet.
"""
from pathlib import Path
import argparse, os, sys, zipfile
ROOT=Path(__file__).resolve().parent
def main():
    import nbformat
    from nbclient import NotebookClient
    from verify_release import verify
    from generate_final_report import create
    from reflection import main as refresh_reflection
    ap=argparse.ArgumentParser();ap.add_argument('--github',default='https://github.com/jtuozzo1616/Mid-Term-Jose-Group-NewsBot-Intelligence-System')
    ap.add_argument('--timeout',type=int,default=1800);args=ap.parse_args()
    target=ROOT/'Midterm_NewsBot_Intelligence_System.ipynb'
    nb=nbformat.read(target,as_version=4)
    os.chdir(ROOT)
    client=NotebookClient(nb,timeout=args.timeout,kernel_name='python3',allow_errors=False,resources={'metadata':{'path':str(ROOT)}})
    print('Executing all notebook cells on the actual BBC labeled corpus...')
    out=client.execute()
    executed=ROOT/'Midterm_NewsBot_Intelligence_System_EXECUTED.ipynb'
    nbformat.write(out,executed)
    manifest=verify(ROOT/'outputs')
    if not str(args.github).startswith('https://github.com/'):
        raise ValueError('Please supply the real public GitHub repository URL.')
    report=create(['--group','Solo','--repo',args.github])
    refresh_reflection()  # Regenerate the two-page evidence-grounded reflection draft.
    doc=ROOT/'docs'/'NewsBot_Reflection_Solo.pdf'
    files=[executed,report,doc,*list((ROOT/'outputs').glob('*'))]
    package=ROOT/'NewsBot_VERIFIED_EXECUTION_EVIDENCE.zip'
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        for f in files:
            if f.is_file():z.write(f,f.relative_to(ROOT))
    print('READY: verified execution ZIP:',package)
    print('Real BBC holdout macro-F1:',manifest['holdout_macro_f1'])
if __name__=='__main__':main()
