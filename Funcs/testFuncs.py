import numpy as np
import pandas as pd
import warnings
import scipy.stats as stat
from scipy.stats import chi2
from math import sqrt


# test de normalite
def normal(variable):
    return str(stat.normaltest(variable))


# test de normalite
def student(variable1, b):
    return str(stat.ttest_ind(variable1, b))


# test  d'hypotese chi2
def hykhi_deux_gauche(variable):
    return str(stat.kstest(variable, 'chi2', alternative='greater', args=(len(variable) - 1,)))


def hykhi_deux_droite(variable):
    return str(stat.kstest(variable, 'chi2', alternative='less', args=(len(variable) - 1,)))


def hykhi_deux_bila(variable):
    return str(stat.kstest(variable, 'chi2', alternative='two-sided', args=(len(variable) - 1,)))


# test d'hypothese loi normal
def hynorm_gauche(variable):
    return str(stat.kstest(variable, 'norm', alternative='greater', args=(len(variable) - 1,)))


def hynorm_droite(variable):
    return str(stat.kstest(variable, 'norm', alternative='less', args=(len(variable) - 1,)))


def hynorm_bila(variable):
    return str(stat.kstest(variable, 'norm', alternative='two-sided', args=(len(variable) - 1,)))


# test d'hypthese t
def hystudent_gauche(variable):
    return str(stat.kstest(variable, 't', alternative='greater', args=(len(variable) - 1,)))


def hystudent_droite(variable):
    return str(stat.kstest(variable, 't', alternative='less', args=(len(variable) - 1,)))


def hystudent_bila(variable):
    return str(stat.kstest(variable, 't', alternative='two-sided', args=(len(variable) - 1,)))


# intervale de confiance Moyenne
def intervale_moyenne(variable, alpha):
    if alpha == 0.01:
        print(np.mean(variable) - 2.58 * (sqrt(np.var(variable) / len(variable))))
        print(np.mean(variable) + 2.58 * (sqrt(np.var(variable) / len(variable))))

        return "[" + str(np.mean(variable) - 2.58 * (sqrt(np.var(variable) / len(variable))))\
               + ', '+ str(np.mean(variable) + 2.58 * (sqrt(np.var(variable) / len(variable)))) \
               + ']'

    elif alpha == 0.05:
        print(np.mean(variable) - 1.96 * (sqrt(np.var(variable) / len(variable))))
        print(np.mean(variable) + 1.96 * (sqrt(np.var(variable) / len(variable))))

        return "[" + str(np.mean(variable) - 1.96 * (sqrt(np.var(variable) / len(variable)))) \
               + ', ' + str(np.mean(variable) + 1.96 * (sqrt(np.var(variable) / len(variable)))) + ']'

    elif alpha == 0.1:
        print(np.mean(variable) - 1.65 * (sqrt(np.var(variable) / len(variable))))
        print(np.mean(variable) + 1.65 * (sqrt(np.var(variable) / len(variable))))

        return "[" + str(np.mean(variable) - 1.65 * (sqrt(np.var(variable) / len(variable)))) \
               + ', ' + str(np.mean(variable) + 1.65 * (sqrt(np.var(variable) / len(variable)))) + ']'

    else:
        return "veuillez entrer un alphat valable!"


def intervale_variance(variable, alpha):
    n = len(variable)
    alpha_g = 1 - (alpha / 2)
    alpha_d = alpha / 2
    if len(variable) < 30:
        print(((n - 1) * np.var(variable)) / tablekhi2(alpha_g, n - 1))
        print(((n - 1) * np.var(variable)) / tablekhi2(alpha_d, n - 1))

        return "[" + str(((n - 1) * np.var(variable)) / tablekhi2(alpha_g, n - 1)) \
               + ", " + str(((n - 1) * np.var(variable)) / tablekhi2(alpha_d, n - 1)) + "]"
    else:
        return intervale_moyenne(variable, alpha)


def tablekhi2(a, b):
    p = np.array([0.995, 0.99, 0.975, 0.95, 0.90, 0.10, 0.05, 0.025, 0.01, 0.005])
    df = np.array(list(range(1, 30)) + list(range(30, 101, 10))).reshape(-1, 1)
    table = stat.chi2.isf(p, df)
    if a == 0.995:
        d = 0
    if a == 0.005:
        d = 9
    if a == 0.975:
        d = 2
    if a == 0.025:
        d = 7

    return table[d, b]

