#!/usr/bin/env python

"""Fit data to first 20%, try to predict last point."""

import vcf_tools as vcf
import matplotlib.pyplot as plt

import numpy as np

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

data = vcf.load_data()
for curve in data:
    xs = np.array([epoch for epoch, _ in curve]).reshape(-1, 1)
    ys = np.array([score for _, score in curve]).reshape(-1, 1)
    percent_traindata = 0.1
    max_train_epoch = int(percent_traindata * len(curve))

    xs_train = xs[:max_train_epoch]
    ys_train = ys[:max_train_epoch]
    xs_test = xs[max_train_epoch:]
    ys_test = ys[max_train_epoch:]

    xs_train = xs_train.reshape(-1, 1)
    ys_train = ys_train.reshape(-1, 1)

    ys_pred_baseline = np.array([ys_train[-1] for x in xs]).reshape(-1, 1)
    # ys_pred_baseline = np.array([1. - (1.0 / (x / 300.) + 0.2) for x in xs]).reshape(-1, 1)

    degree = 1
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(xs_train, ys_train)
    ys_pred = model.predict(xs)

    # Evalualuate
    xs = list(xs.reshape(1, -1)[0])
    ys = list(ys.reshape(1, -1)[0])
    ys_pred = list(ys_pred.reshape(1, -1)[0])
    ys_base = list(ys_pred_baseline.reshape(1, -1)[0])
    ignore = 2

    print(("MSE (total) = {pred:0.2f}\t| base = {base:0.2f}"
           ).format(pred=vcf.mse(ys[ignore:], ys_pred[ignore:]),
                    base=vcf.mse(ys[ignore:], ys_base[ignore:])))
    print(("MSE (train) = {pred:0.2f}\t| base = {base:0.2f}"
           ).format(pred=vcf.mse(ys[ignore:max_train_epoch],
                                 ys_pred[ignore:max_train_epoch]),
                    base=vcf.mse(ys[ignore:max_train_epoch],
                                 ys_base[ignore:max_train_epoch])))
    print(("MSE (test) = {pred:0.2f}\t| base = {base:0.2f}"
           ).format(pred=vcf.mse(ys[max_train_epoch:],
                                 ys_pred[max_train_epoch:]),
                    base=vcf.mse(ys[max_train_epoch:],
                                 ys_base[max_train_epoch:])))
    print(("diff last = {pred:0.2f}\t| base = {base:0.2f}"
           ).format(pred=vcf.last_diff(ys, ys_pred),
                    base=vcf.last_diff(ys, ys_base)))

    # Plot curves
    plt.plot(xs, ys_pred, color='r', label="predicted")
    plt.plot(xs, ys, color='b', label="ground truth")
    plt.plot(xs, ys_base, color='g', label="ground truth")
    plt.plot((xs[max_train_epoch], xs[max_train_epoch]), (0, 1), 'k-')
    plt.ylim(0, 1)  # min and max score
    plt.show()
    print("#" * 80)
