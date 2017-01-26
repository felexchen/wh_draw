#include <iostream>
#include <string>
#include <vector>
#include <memory>

#include "TError.h"
#include "TColor.h"
#include "TVector2.h"

#include "core/baby.hpp"
#include "core/process.hpp"
#include "core/named_func.hpp"
#include "core/plot_maker.hpp"
#include "core/plot_opt.hpp"
#include "core/palette.hpp"
#include "core/hist1d.hpp"
#include "core/utilities.hpp"
#include "core/functions.hpp"

using namespace std;
using namespace PlotOptTypes;

namespace {
  double lumi = 36.8;
}

int main(){
  gErrorIgnoreLevel = 6000;
  string bfolder("");
  string hostname = execute("echo $HOSTNAME");
  if(Contains(hostname, "cms") || Contains(hostname, "compute-"))
    bfolder = "/net/cms2"; // In laptops, you can't create a /net folder

  Palette colors("txt/colors.txt", "default");

  string ntupletag = "*.root";
  
  string fdata = bfolder+"/cms2r0/babymaker/babies/2016_11_08/data/merged_database_standard/";



  auto data_highmt = Process::MakeShared<Baby_full>("Data 1l, m_{T} > 140", Process::Type::data, kBlack,
    {fdata+ntupletag},"pass && trig_ra4 && st>500 && mt>140 && nleps==1 && nveto==0 && njets>=6 && nbm_moriond>=1");
  auto data_lowmt = Process::MakeShared<Baby_full>("Data 1l, m_{T} #leq 140", Process::Type::background, kBlack,
    {fdata+ntupletag},"pass && trig_ra4 && st>500 && mt<=140 && nleps==1 && nveto==0 && njets>=6 && nbm_moriond>=1");
  data_lowmt->SetFillColor(kWhite);
  data_lowmt->SetLineColor(kBlue-7);
  data_lowmt->SetLineWidth(2);

  auto data2lveto = Process::MakeShared<Baby_full>("Data 2l or l+trk", Process::Type::data, kBlue+2,
    {fdata+ntupletag},
    "pass && trig_ra4 && st>500 && ((nleps==2 && njets>=5 && nbm_moriond<=2) || (nleps==1 && nveto==1 && njets>=6 && nbm_moriond>=1 && mt>140))");

  auto data2l = Process::MakeShared<Baby_full>("Data 2l", Process::Type::data, kMagenta+3,
    {fdata+ntupletag},
    "pass && trig_ra4 && st>500 && (nleps==2 && njets>=5 && nbm_moriond<=2)");


  auto data = Process::MakeShared<Baby_full>("Data", Process::Type::data, kBlack,
    {fdata+ntupletag},"pass && trig_ra4");


  vector<shared_ptr<Process> > data1l_procs = {data_highmt, data_lowmt};
  vector<shared_ptr<Process> > data2lveto_procs = {data2lveto, data_lowmt};
  vector<shared_ptr<Process> > data2l_procs = {data2l, data_lowmt};

  PlotOpt log_lumi("txt/plot_styles.txt", "CMSPaper");
  log_lumi.Title(TitleType::preliminary)
    .Bottom(BottomType::ratio)
    .YAxis(YAxisType::log)
    .Stack(StackType::data_norm); 
  PlotOpt lin_lumi = log_lumi().YAxis(YAxisType::linear);
  PlotOpt log_shapes = log_lumi().Stack(StackType::shapes)
    .Bottom(BottomType::off)
    .ShowBackgroundError(false);
  PlotOpt lin_shapes = log_shapes().YAxis(YAxisType::linear);
  PlotOpt log_lumi_info = log_lumi().Title(TitleType::info);
  PlotOpt lin_lumi_info = lin_lumi().Title(TitleType::info);
  PlotOpt log_shapes_info = log_shapes().Title(TitleType::info);
  PlotOpt lin_shapes_info = lin_shapes().Title(TitleType::info);
  vector<PlotOpt> log = {log_lumi_info};
  vector<PlotOpt> lin = {lin_lumi_info};


  string baseline = "met>200 && nleps==1 && nveto==0 && st>500 && njets>=6 && nbm_moriond>=1";
  PlotMaker pm;

  //data-to-data
  vector<string> metbins = {"met>150 && met<=500", "met>150 && met<=200", "met>200 && met<=350", "met>350 && met<=500", "met>200 && met<=500","met>500","met>200"};
  for (auto &imet: metbins){
    pm.Push<Hist1D>(Axis(20, 0.,1000., "mj14", "M_{J} [GeV]",{250.,400.}),
		    imet + "&&nbm_moriond==1", data1l_procs, lin).Tag("data1l1b").RatioTitle("Data m_{T} > 140","Data m_{T} #leq 140");

    pm.Push<Hist1D>(Axis(20, 0.,1000., "mj14", "M_{J} [GeV]", {250.,400.}),
		    imet + "&&nbm_moriond>=2", data1l_procs, lin).Tag("data1l2b").RatioTitle("Data m_{T} > 140","Data m_{T} #leq 140");;

    pm.Push<Hist1D>(Axis(20, 0.,1000., "mj14", "M_{J} [GeV]", {250.,400.}),
		    imet,  data2l_procs, lin).Tag("data2l").RatioTitle("Data 2l","Data 1l, m_{T} #leq 140");

    pm.Push<Hist1D>(Axis(20, 0.,1000., "mj14", "M_{J} [GeV]", {250.,400.}),
		    imet, data2lveto_procs, lin).Tag("data2lveto").RatioTitle("Data 2l","Data 1l, m_{T} #leq 140");

  } 


  pm.min_print_ = true;
  pm.MakePlots(lumi);

}
