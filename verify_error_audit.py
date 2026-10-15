#!/usr/bin/env python3
"""Ensure the public, copyright-safe error-direction counts match the BBC holdout metrics.

This audit is tied to the verified historical BBC run. It deliberately refuses to
treat a different dataset or holdout as the same experiment.
"""
from collections import Counter
from pathlib import Path
import argparse, json
import pandas as pd

ROOT=Path(__file__).resolve().parent

def verify(out=ROOT/'outputs'):
    out=Path(out)
    df=pd.read_csv(out/'error_directions.csv')
    expected={'true_label','predicted_label','error_count'}
    if set(df.columns)!=expected:
        raise AssertionError('Unexpected error-direction CSV columns')
    labs={'business','entertainment','politics','sport','tech'}
    assert len(df)==9, 'Expected nine observed confusion directions'
    assert set(df.true_label).issubset(labs) and set(df.predicted_label).issubset(labs)
    assert df.true_label.ne(df.predicted_label).all(), 'Errors must be off-diagonal'
    assert (df.error_count>0).all() and (df.error_count%1==0).all()
    assert not df.duplicated(['true_label','predicted_label']).any()
    assert int(df.error_count.sum())==11, 'The observed BBC run had 11 holdout mistakes'
    metrics=pd.read_csv(out/'per_class_metrics.csv')
    manifest=json.loads((out/'run_manifest.json').read_text(encoding='utf-8'))
    assert manifest['holdout_rows']==288 and manifest['rows']==1440
    assert abs(manifest['holdout_accuracy']-277/288)<1e-10
    assert manifest['selected_model']=='Linear SVM'
    # Independently recover TP and FN from measured recalls (not from prose).
    tp={}
    for row in metrics.itertuples(index=False):
        count=round(row.recall*row.support)
        assert abs(row.recall-count/row.support)<1e-9
        tp[row.category]=count
        missed=int(df.loc[df.true_label==row.category,'error_count'].sum())
        assert int(row.support)-count==missed, f'FN mismatch for {row.category}'
    for row in metrics.itertuples(index=False):
        incorrect=int(df.loc[df.predicted_label==row.category,'error_count'].sum())
        calculated_precision=tp[row.category]/(tp[row.category]+incorrect)
        assert abs(calculated_precision-row.precision)<1e-9, f'FP mismatch for {row.category}'
    assert sum(tp.values())==277
    print('PASS: all 11 BBC misclassifications independently reconcile to the published precision, recall, and holdout results')
    return True

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--outputs',default='outputs')
    args=p.parse_args()
    verify(ROOT/args.outputs)
