#! /usr/bin/env python

# Adapted from sig_sys_table.py

from __future__ import print_function

import argparse
import glob
import os
import re
import subprocess

def fullPath(path):
    return os.path.realpath(os.path.abspath(os.path.expanduser(path)))

def ensureDir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def printHeader(model, out_file):
    print("\\documentclass{article}", file=out_file)
    print("\\usepackage{rotating}", file=out_file)
    print("\\usepackage{amsmath}", file=out_file)
    print("\\usepackage{multirow}\n", file=out_file)
    
    print("\\newcommand{\\cPqb}{\\ifmmode{\\text{b}}\\else{b}}", file=out_file)
    print("\\newcommand{\\met}{E_{\\text{T}}^{\\text{miss}}}", file=out_file)
    print("\\newcommand{\\njets}{N_{\\text{jets}}}", file=out_file)
    print("\\newcommand{\\nb}{N_{\\text{b}}}\n", file=out_file)

    print("\\begin{document}\n", file=out_file)

    print("\\begin{sidewaystable}[p!]", file=out_file)
    print("  \\centering", file=out_file)
    print("  \\caption{Summary of the signal systematic uncertainties. Systematics are considered", file=out_file)
    print("           fully correlated between bins and opposite signs indicate anti-correlation.", file=out_file)
    print("           Different sources of uncertainties are considered uncorrelated.}", file=out_file)
    print("  \\label{tab:unc:sig}", file=out_file)
    print("  \\resizebox{\\textwidth}{!}{", file=out_file)
    print("  \\renewcommand{\\arraystretch}{1.2}", file=out_file)
    if "TChiHH" in model:
        print("  \\begin{tabular}{l|cc|cc|cc|cc}", file=out_file)
        print("  \\hline\\hline", file=out_file)
        print("  ${\\cal L}=35.9$ fb$^{-1}$  & \\multicolumn{8}{c}{Uncertainty [\\%]}\\\\", file=out_file)
        print("  \\hline", file=out_file)
        print("  \\multirow{2}{*}{Source} & \\multicolumn{2}{c|}{$150<\\met\\leq 200$}& \\multicolumn{2}{c|}{$200<\\met\\leq 300$}& \\multicolumn{2}{c|}{$300<\\met\\leq 450$}& \\multicolumn{2}{c}{$\\met>450$}\\\\", file=out_file)
        print("  \\cline{2-9}", file=out_file)
        print("  &      3b &      4b &      3b &      4b &      3b &      4b &      3b &      4b \\\\", file=out_file)
        print("  \\hline", file=out_file)
    else: 
        print("  \\begin{tabular}[tbp!]{l||ccc|ccc||ccc|ccc||ccc|ccc}\\hline\\hline", file=out_file)
        print("  \\multirow{3}{*}{Uncertainty [\\%]} & \\multicolumn{6}{c||}{$200<\\met\\leq350$} & \\multicolumn{6}{c||}{$350<\\met\\leq500$} & \\multicolumn{6}{c}{$\\met>500$}\\\\", file=out_file)
        print("  \\cline{2-19} & \\multicolumn{3}{c|}{$6\\leq\\njets\\leq8$} & \\multicolumn{3}{c||}{$\\njets\\geq9$} & \\multicolumn{3}{c|}{$6\\leq\\njets\\leq8$} & \\multicolumn{3}{c||}{$\\njets\\geq9$} & \\multicolumn{3}{c|}{$6\\leq\\njets\\leq8$} & \\multicolumn{3}{c}{$\\njets\\geq9$}\\\\", file=out_file)
        print("  \\cline{2-19} & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$ & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$ & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$ & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$ & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$ & $\\nb=1$ & $\\nb=2$ & $\\nb\geq3$\\\\", file=out_file)



def prettySysName(sys_name):
    sys_name = sys_name.strip()
    if   sys_name == "lepeff":                                      return "Lepton efficiency"
    elif sys_name == "fs_lepeff":                                   return "FastSim lepton efficiency"
    elif sys_name == "trig":                                        return "Trigger efficiency"
    elif sys_name == "fs_bctag"   or sys_name == "fs_bchig_deep" :  return "FastSim \\cPqb{}-tag efficiency"
    elif sys_name == "bctag"      or sys_name == "bchig_deep":      return "\\cPqb{}-tag efficiency"
    elif sys_name == "fs_udsgtag" or sys_name == "fs_udsghig_deep": return "FastSim mistag efficiency"
    elif sys_name == "udsgtag"    or sys_name == "udsghig_deep":    return "Mistag efficiency"
    elif sys_name == "fs_genmet":                                   return "FastSim MET"
    elif sys_name == "jec":                                         return "Jet energy corrections"
    elif sys_name == "jer":                                         return "Jet energy resolution"
    elif sys_name == "jetid":                                       return "Jet ID"
    elif sys_name == "murf":                                        return "QCD Scales"
    elif sys_name == "isr":                                         return "ISR"
    elif sys_name == "pu":                                          return "Pile up"
    elif sys_name == "lumi":                                        return "Luminosity"
    else:                                                           return sys_name
    
def printSystematic(model_name, out_file, sys_name, values):
    if ("TChiHH" not in model_name):
        print("  {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {}\\\\"
              .format(
                  prettySysName(sys_name),
                  values[0][0][0], values[0][0][1], values[0][0][2],
                  values[0][1][0], values[0][1][1], values[0][1][2],
                  values[1][0][0], values[1][0][1], values[1][0][2],
                  values[1][1][0], values[1][1][1], values[1][1][2],
                  values[2][0][0], values[2][0][1], values[2][0][2],
                  values[2][1][0], values[2][1][1], values[2][1][2]),
              file=out_file)

        return [[[ None for i in range(3) ] for j in range(2) ] for k in range(3) ]
    else:
        print("  {} & {} & {} & {} & {} & {} & {} & {} & {}\\\\"
              .format(
                  prettySysName(sys_name),
                  values[0][0], values[0][1], values[1][0], values[1][1],
                  values[2][0], values[2][1], values[3][0], values[3][1]),
              file=out_file)

        return [[ None for i in range(2) ] for j in range(4) ]

def recordValue(line, values):
    try:
        name, value = line.split()
    except ValueError as e:
        return

    region, bin_name = name.split("_",1)

    if region != "r4":
        return

    met, njets, nb = bin_name.split("_")

    imet = None
    if   met == "lowmet":  imet = 0
    elif met == "medmet":  imet = 1
    elif met == "highmet": imet = 2
    else: raise Exception("Bad MET: {}".format(met))

    injets = None
    if   njets == "lownj":  injets = 0
    elif njets == "highnj": injets = 1
    else: raise Exception("Bad Njets: {}".format(njets))

    inb = None
    if   nb == "1b": inb = 0
    elif nb == "2b": inb = 1
    elif nb == "3b": inb = 2
    else: raise Exception("Bad Nb: {}".format(nb))

    value = int(round(100.*float(value)))

    if value == 0:
        values[imet][injets][inb] = "$<1$"
    else:
        values[imet][injets][inb] = "${}$".format(str(value))

def recordValueHiggsino(line, values):
    try: 
        name, value = line.split()
    except ValueError as e: 
        return

    region, nb, met = name.split("_")

    if region == "sbd" or nb == "2b": 
        return

    imet = None
    try: 
        imet = int(met.replace("met",""))
    except ValueError as e: 
        return
    if (imet>3): 
        raise Exception("Bad MET: {}".format(met))

    inb = None
    try: 
        inb = int(nb.replace("b",""))-3
    except ValueError as e: 
        return
    if (inb<0 or inb>1): 
        raise Exception("Bad Nb: {}".format(nb))

    value = int(round(100.*float(value)))

    if value == 0:
        values[imet][inb] = "$<1$"
    else:
        values[imet][inb] = "${}$".format(str(value))

def modelName(path):
    name = os.path.basename(path)
    regex = re.compile("sys.*?_SMS-(.*?)_mGluino-(.*?)_mLSP-(.*?)_")
    result = regex.match(name)
    if result:
        return "{}({},{})".format(result.group(1), result.group(2), result.group(3))
    else:
        return name

def printModel(model_name, out_file, input_file):
    print("  \\hline", file=out_file)
    if ("TChiHH" not in model_name): 
        print("  & \\multicolumn{{18}}{{c}}{{Signal model: {} }}\\\\".format(model_name), file=out_file)
    else:
        print("  & \\multicolumn{{8}}{{c}}{{Signal model: {} }}\\\\".format(model_name), file=out_file)
    print("  \\hline", file=out_file)
    sys_name = None
    is_signal = False
    syst_written = True
    if ("TChiHH" not in model_name): 
        values = [[[ None for i in range(3) ] for j in range(2) ] for k in range(3) ]
    else:
        values = [[ None for i in range(2) ] for j in range(4) ]
    for line in input_file:
        if "SYSTEMATIC" in line:
            if sys_name is not None and is_signal and not syst_written:
                values = printSystematic(model_name, out_file, sys_name, values)
                syst_written = True
            sys_name = line.rstrip().split("SYSTEMATIC",1)[1]
        elif "PROCESSES" in line:
            if sys_name is not None and is_signal and not syst_written:
                values = printSystematic(model_name, out_file, sys_name, values)
                syst_written = True
            is_signal = ("signal" in line)
        elif sys_name is None or not is_signal:
            continue
        else:
            syst_written = False
            if ("TChiHH" in model_name): 
                recordValueHiggsino(line, values)
            else: 
                recordValue(line, values)
            
    if sys_name is not None and is_signal and not syst_written:
        values = printSystematic(model_name, out_file, sys_name, values)
        syst_written = True

def printFooter(out_file):
    print("  \\hline\\hline", file=out_file)
    print("  \\end{tabular}", file=out_file)
    print("  }", file=out_file)
    print("\\end{sidewaystable}", file=out_file)
    print("\\end{document}", file=out_file)

def compileLaTeX(output_path):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(output_path))
    subprocess.call(["pdflatex",output_path])
    os.chdir(cwd)
    print("\nCompiled {}\n".format(output_path))

def sigSysTable(output_path, input_paths, do_compile):
    output_path = fullPath(output_path)
    input_paths = [ fullPath(f) for sublist in input_paths for f in glob.glob(sublist) if os.path.isfile(f) ]
    model_name = modelName(input_paths[0])
    print("Working on "+model_name)
    with open(output_path, "w") as out_file:
        printHeader(model_name, out_file)
        for input_path in input_paths:
            with open(input_path, "r") as input_file:
                model_name = modelName(input_path)
                printModel(model_name, out_file, input_file)
        printFooter(out_file)

    print("\nWrote signal systematics table to {}\n".format(output_path))

    if do_compile:
        compileLaTeX(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes input systematics files and produces a LaTeX table of systematics",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("output_file", help="Output LaTeX file containing table")
    parser.add_argument("input_files", nargs="*", help="Input text file(s) containing systematics")
    parser.add_argument("--no_compile", action="store_true", help="Do not run pdflatex on resulting .tex file")
    args = parser.parse_args()

    sigSysTable(args.output_file, args.input_files, not args.no_compile)