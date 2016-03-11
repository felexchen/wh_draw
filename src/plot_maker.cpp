#include "plot_maker.hpp"

#include "TCanvas.h"

#include "utilities.hpp"
#include "timer.hpp"
#include "thread_pool.hpp"

using namespace std;

PlotMaker::PlotMaker():
  file_extensions_{"pdf"},
  stacks_(){
}

void PlotMaker::AddPlot(const vector<shared_ptr<Process> > &processes,
                        const HistoDef &histo_def){
  //Adds a plot to the list of plots to be produced. Does NOT fill or draw the histogram.
  stacks_.push_back(HistoStack(processes, histo_def));
}

void PlotMaker::MakePlots(){
  //Processes this list of plots provided with AddPlot and writes the results to disk
  if(file_extensions_.size() == 0){
    DBG("No file extensions provided => no plots produced.");
    return;
  }
  FillHistograms();
  PrintPlots();
}

void PlotMaker::FillHistograms(){
  //Iterates over all processes needed for requested plots and fills the necessary histograms
  set<shared_ptr<Process> > processes = GetProcesses();
  ThreadPool tp;
  vector<future<void> > done_flags;
  for(const auto &proc: processes){
    tp.Push(bind(&PlotMaker::FillHistogram, this, ref(proc)));
  }
  for(auto &done: done_flags){
    done.get();
  }
}

void PlotMaker::FillHistogram(const shared_ptr<Process> &proc){
  cout << "Filling histograms for the " << proc->name_ << " process..." << endl;
  vector<pair<HistoDef, TH1D * const> > histos;
  {
    lock_guard<mutex> lock(Multithreading::root_mutex);
    histos = GetHistos(proc);
  }
  long num_entries = proc->baby_->GetEntries();
  Timer timer(num_entries, 1.);
  timer.Start();
  for(long entry = 0; entry < num_entries; ++entry){
    timer.Iterate();
    proc->baby_->GetEntry(entry);
    for(auto &histo: histos){
      const auto &baby = *(proc->baby_);
      vector<double> values = histo.first.var_(baby);
      vector<double> hist_cuts = histo.first.cut_(baby);
      vector<double> proc_cuts = proc->cut_(baby);
      vector<double> weights = histo.first.weight_(baby);
      bool sc_values = histo.first.var_.IsScalar();
      bool sc_hist_cuts = histo.first.cut_.IsScalar();
      bool sc_proc_cuts = proc->cut_.IsScalar();
      bool sc_weights = histo.first.weight_.IsScalar();
      for(size_t i = 0; (i < 1 || !sc_values || !sc_hist_cuts || !sc_proc_cuts || ! sc_weights)
            && (sc_values || i < values.size())
            && (sc_hist_cuts || i < hist_cuts.size())
            && (sc_proc_cuts || i < proc_cuts.size())
            && (sc_weights || i < weights.size());
            ++i){
        bool hist_cut = sc_hist_cuts ? (hist_cuts.size() ? hist_cuts[0] : false) : hist_cuts.at(i);
        bool proc_cut = sc_proc_cuts ? (proc_cuts.size() ? proc_cuts[0] : false) : proc_cuts.at(i);
        if(!(hist_cut && proc_cut)) continue;
        double x = sc_values ? (values.size() ? values[0] : false) : values.at(i);
        double w = sc_weights ? (weights.size() ? weights[0] : false) : weights.at(i);
        histo.second->Fill(x, w);
      }
    }
  }
}

void PlotMaker::PrintPlots(){
  //Takes already filled histograms and prints to file
  if(file_extensions_.size() == 0){
    DBG("No file extensions provided => no plots produced.");
    return;
  }
  TCanvas c;
  for(auto &stack: stacks_){
    bool drawn = false;
    vector<TH1D> bkgs(stack.backgrounds_.size());
    for(size_t ihist = stack.backgrounds_.size() - 1; ihist < stack.backgrounds_.size(); --ihist){
      bkgs.at(ihist) = stack.backgrounds_.at(ihist).second;
      for(size_t jhist = 0; jhist < ihist; ++jhist){
        bkgs.at(ihist) = bkgs.at(ihist) + stack.backgrounds_.at(jhist).second;
      }
      bkgs.at(ihist).Draw(drawn ? "hist same" : "hist");
      drawn = true;
    }
    for(auto &signal: stack.signals_){
      signal.second.Draw(drawn ? "hist same" : "hist");
      drawn = true;
    }
    for(auto &data: stack.datas_){
      data.second.Draw(drawn ? "hist same" : "hist");
      drawn = true;
    }

    string base_name = stack.definition_.GetName();
    for(const auto &ext: file_extensions_){
      string full_name = base_name+"."+ext;
      c.Print(full_name.c_str());
      cout << "Wrote plot to " << full_name << "." << endl;
    }
  }
}

set<shared_ptr<Process> > PlotMaker::GetProcesses() const{
  //Finds list of all processes needed for requested plots
  set<shared_ptr<Process> > processes;
  for(const auto &stack: stacks_){
    for(const auto &proc: stack.GetProcesses()){
      processes.insert(proc);
    }
  }
  return processes;
}

vector<pair<HistoDef, TH1D * const> > PlotMaker::GetHistos(const shared_ptr<Process> &process){
  //Gets list of plots that include a particular process
  vector<pair<HistoDef, TH1D * const> > histos;
  for(auto &stack: stacks_){
    auto procs = stack.GetProcesses();
    auto loc = procs.find(process);
    if(loc == procs.end()) continue;
    histos.push_back(pair<HistoDef, TH1D * const>(stack.definition_, stack.GetHisto(process)));
  }
  return histos;
}

vector<pair<HistoDef, const TH1D * const> > PlotMaker::GetHistos(const shared_ptr<Process> &process) const{
  //Gets list of plots that include a particular process
  vector<pair<HistoDef, const TH1D * const> > histos;
  for(const auto &stack: stacks_){
    auto procs = stack.GetProcesses();
    auto loc = procs.find(process);
    if(loc == procs.end()) continue;
    histos.push_back(pair<HistoDef, const TH1D * const>(stack.definition_, stack.GetHisto(process)));
  }
  return histos;
}
