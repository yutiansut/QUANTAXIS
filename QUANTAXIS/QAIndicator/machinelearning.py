# coding:utf-8
from sklearn import (naive_bayes, neighbors, neural_network, semi_supervised,
                     svm, tree)
from sklearn import linear_model






class linear():
    """
    Ordinary least squares Linear Regression.

    Parameters
    ----------
    fit_intercept : boolean, optional
        whether to calculate the intercept for this model. If set
        to false, no intercept will be used in calculations
        (e.g. data is expected to be already centered).

    normalize : boolean, optional, default False
        If True, the regressors X will be normalized before regression.
        This parameter is ignored when `fit_intercept` is set to False.
        When the regressors are normalized, note that this makes the
        hyperparameters learnt more robust and almost independent of the number
        of samples. The same property is not valid for standardized data.
        However, if you wish to standardize, please use
        `preprocessing.StandardScaler` before calling `fit` on an estimator
        with `normalize=False`.

    copy_X : boolean, optional, default True
        If True, X will be copied; else, it may be overwritten.

    n_jobs : int, optional, default 1
        The number of jobs to use for the computation.
        If -1 all CPUs are used. This will only provide speedup for
        n_targets > 1 and sufficient large problems.

    Attributes
    ----------
    coef_ : array, shape (n_features, ) or (n_targets, n_features)
        Estimated coefficients for the linear regression problem.
        If multiple targets are passed during the fit (y 2D), this
        is a 2D array of shape (n_targets, n_features), while if only
        one target is passed, this is a 1D array of length n_features.

    residues_ : array, shape (n_targets,) or (1,) or empty
        Sum of residuals. Squared Euclidean 2-norm for each target passed
        during the fit. If the linear regression problem is under-determined
        (the number of linearly independent rows of the training matrix is less
        than its number of linearly independent columns), this is an empty
        array. If the target vector passed during the fit is 1-dimensional,
        this is a (1,) shape array.

        .. versionadded:: 0.18

    intercept_ : array
        Independent term in the linear model.

    Notes
    -----
    From the implementation point of view, this is just plain Ordinary
    Least Squares (scipy.linalg.lstsq) wrapped as a predictor object.

    """
    reg = linear_model.LinearRegression()
    reg.fit ([[0, 0], [1, 1], [2, 2]], [0, 1, 2])

    reg.coef_

class SVM:
    pass
class CNN:
    pass


class LSTM:
    pass


class DT:
    
    pass
