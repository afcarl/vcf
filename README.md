# Validation Curve Fitting

Validation curves are scores of neural networks which are evaluated for many
epochs. Hence the x-axis is the epoch, the y axis is the score.

Each csv file has a header. The seperator is `,`. The first colum is the
epoch, the second is the score.


## Evaluation

The task is to predict the last score. So given a CSV file in `vcf-data`, you
may take the first 20% of it. Fit your model only to those 20%. Then take the
epoch of the last line and try to predict its score.

If you want to report how well you did, report the absolute difference of the
true score of the last line and your predicted score.

Do the same, but only with 10% of the data for training.


## Baselines

| File                                          | Take last (20%-err)  | Take last (10%-err)  |
| --------------------------------------------- | -------------------- | -------------------- |
| cnn32-32-64-64-1024-1024-relu-30000-train.csv | 0.06                 | 0.14                 |
| cnn-32-32-64-64-1024-1024-relu-30000-test.csv | 0.14                 | 0.22                 |
|                                               |                      |                      |
