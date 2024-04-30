print("StyleTTS 2 CLI Inference")
import click
import time
import os
import argparse
import tqdm
import msinference
from pydub import AudioSegment
from txtsplit import txtsplit
import numpy as np
import scipy
from nltk.tokenize import word_tokenize

#@click.command()
#@click.argument('text')
#@click.argument('output')
#@click.option('--audio-sample', '-a', type=click.Path(exists=True), required=True)
#@click.option('--pth-path', '-p', type=click.Path(exists=True), required=True)
#@click.option('--file', '-f', default=False, show_default=True, help='Read from input text from file')

parser = argparse.ArgumentParser(prog='ProgramName', description='What the program does', epilog='Text at the bottom of help')
parser.add_argument('-f', '--file', action='store_true')
parser.add_argument('-b', '--batch', action='store_true')
parser.add_argument('-p', '--pthpath', required=True, action='store')
parser.add_argument('-t', '--text', required=True, action='store')
parser.add_argument('-a', '--audio', required=True, action='store')
parser.add_argument('-v', '--alpha', default=0.5, action='store')
parser.add_argument('-e', '--beta', default=1.0, action='store')
parser.add_argument('-s', '--scale', default=1.0, action='store')
parser.add_argument('-x', '--denoiseonly', default=False, action='store_false')
parser.add_argument('-y', '--lambd', default=1.0, action='store')
parser.add_argument('-z', '--nfe', default=128, action='store')
args = parser.parse_args()
print(args)

msinference.init(args.pthpath)
print("Computing Style")
s_ref = msinference.compute_style(args.audio)
print("Done Computing Style")

def enhancement(input_dir, output_dir, denoise=args.denoiseonly, strength=args.lambd, nfe=args.nfe):
    if denoise:
        os.system(f"resemble-enhance --denoise_only --lambd {strength} --parallel_mode {input_dir} {output_dir}")
    else:
        os.system(f"resemble-enhance --lambd {strength} --nfe {nfe} --parallel_mode {input_dir} {output_dir}")

def main(text_=args.text, audio_sample=args.audio, pth_path=args.pthpath, file=args.file):
    normal_outdir = f"./Results/{os.path.basename(pth_path).split('.pth')[0]}/"
    enhanced_dir = f"./ResultsEnhanced/{os.path.basename(pth_path).split('.pth')[0]}/"
    if not os.path.exists(normal_outdir):
        os.makedirs(normal_outdir)
    if not os.path.exists(enhanced_dir):
        os.makedirs(enhanced_dir)
    output = str(normal_outdir + os.path.basename(pth_path).split(".pth")[0] + "_" + str(round(time.time() * 1000)) + ".wav")
    if file and not args.batch:
        with open(text_, 'r') as file:
            text_ = file.read()
    #click.echo("Importing modules...")
    
    ps = msinference.global_phonemizer.phonemize([text_])
    ps = word_tokenize(ps[0])
    ps = ' '.join(ps)
    ps = ps.replace('``', '"')
    ps = ps.replace("''", '"')

    sentences = txtsplit(ps)
    wavs = []
    s_prev = None
    for text in sentences:
        if text_.strip() == "": continue
        # wav, s_prev = msinference.LFinference(text, s_prev, s_ref, alpha = 0.5, beta = 0.9, t = 0.7, diffusion_steps=10, embedding_scale=2.5)
        wav, s_prev = msinference.LFinference(text, s_prev, s_ref, alpha=float(args.alpha), beta=float(args.beta), t=0.7, diffusion_steps=25, embedding_scale=float(args.scale))
        wavs.append(wav)
    #click.echo('Synthesized.')
    scipy.io.wavfile.write(output, 24000, np.concatenate(wavs))
    if not args.batch:
        enhancement(input_dir=normal_outdir, output_dir=enhanced_dir)
    else:
        return normal_outdir, enhanced_dir

def sub(text_file=args.text):
    with open(text_file, 'r') as file:
        script = file.readlines()
    input_dir, output_dir = "", ""
    for line in tqdm.tqdm(script):
        input_dir, output_dir = main(text_=line, audio_sample=args.audio, pth_path=args.pthpath, file=args.file)
    enhancement(input_dir=input_dir, output_dir=output_dir)

#@click.option('--batch', '-b', default=False, show_default=True, help='Create an output for each line in a file.')
if __name__ == '__main__':
    if args.batch and args.file:
        sub()
    else:
        main()
