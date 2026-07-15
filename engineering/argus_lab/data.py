"""Canonical Chen-Zimmermann data access and event-window construction."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

PORT_COLUMNS={"signalname","port","date","ret","signallag","Nlong","Nshort"}
DOC_COLUMNS={"Acronym","Cat.Signal","Predictability in OP","SampleStartYear","SampleEndYear","Year"}

def normalize_month(values):
    return pd.to_datetime(values).dt.to_period("M").dt.to_timestamp()

def validate_columns(frame,required,label):
    missing=set(required)-set(frame.columns)
    if missing: raise ValueError(f"{label} missing columns: {sorted(missing)}")

def load_signal_doc(raw_dir: Path):
    frame=pd.read_csv(raw_dir/"SignalDoc.csv");validate_columns(frame,DOC_COLUMNS,"SignalDoc");return frame

def load_ports(raw_dir: Path,kind="predictor",panel_end="2024-12-31",long_short_only=True):
    filename={"predictor":"PredictorPortsFull.parquet","placebo":"PlaceboPortsFull.parquet"}[kind]
    frame=pd.read_parquet(raw_dir/filename);validate_columns(frame,PORT_COLUMNS,filename)
    frame=frame.copy();frame["date"]=normalize_month(frame.date);frame=frame[frame.date<=pd.Timestamp(panel_end).to_period("M").to_timestamp()]
    if long_short_only:frame=frame[frame.port=="LS"]
    return frame

def assign_event_windows(frame,date="date",sample_start="SampleStartYear",sample_end="SampleEndYear",publication="Year"):
    year=frame[date].dt.year
    return np.select([year<frame[sample_start],year<=frame[sample_end],year<=frame[publication]],["pre_sample","in_sample","post_sample"],default="post_pub")

def eligible_signals(frame,min_in_sample=12,min_post_pub=12):
    counts=frame.pivot_table(index="signalname",columns="window",values="ret",aggfunc="count").fillna(0)
    return counts.index[(counts.get("in_sample",0)>=min_in_sample)&(counts.get("post_pub",0)>=min_post_pub)]
