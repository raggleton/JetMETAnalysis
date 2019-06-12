#!/usr/bin/env python

import sys
import os
import argparse
import ROOT


ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2()
ROOT.gStyle.SetOptStat(0)

def count_events_in_file(input_file, dir_name, use_weight):
    nevents = 0
    f = ROOT.TFile(input_file)
    tree = f.Get("%s/t" % (dir_name))
    if use_weight:
        for evt in tree:
            nevents += evt.weight
    else:
        nevents += tree.GetEntriesFast()
    f.Close()
    return nevents


def get_cache(cache_filename="cache_nevents.csv"):
    results = {}
    if os.path.isfile(cache_filename):
        with open(cache_filename) as cache_file:
            for line in cache_file:
                filename, nevents = line.split(",")
                results[filename] = float(nevents)
    return results


def save_cache(results, cache_filename="cache_nevents.csv"):
    with open(cache_filename, "w") as cache_file:
        for k, v in results.items():
            cache_file.write("%s,%.3f\n" % (k, v))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs="+")
    parser.add_argument('--dirName', type=str, help="Name of directory")
    parser.add_argument('--useWeight', default=False, action='store_true', help="If True, applies event weight")
    parser.add_argument('--cache', default="cache_nevents.csv", help="Cache file")
    args = parser.parse_args()

    results = get_cache(args.cache)

    nevents = 0
    for ind, ifile in enumerate(args.input, 1):
        print "Doing %d/%d" % (ind, len(args.input)), ifile
        this_nevents = count_events_in_file(ifile, args.dirName, args.useWeight)
        results[os.path.abspath(ifile)] = this_nevents
        nevents += this_nevents

    print nevents
    save_cache(results, args.cache)
