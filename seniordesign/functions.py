import numpy as np
import matplotlib.pyplot as plt


def mixsolver(f, e, e1, e2=None):

    if len(f) == 2:
        f = f[0]
        a = -2
        # print(
        #     f"{(0-((e*(3*f-1)+e1*(2-3*f)))+((((e*(3*f-1)+e1*(2-3*f))**2)+8*e1*e)**0.5))/(-4)}, = {np.roots([-2, (e*(3*f-1)+e1*(2-3*f)), e1*e])[root]}")
        # return (0-((e*(3*f-1)+e1*(2-3*f)))+((((e*(3*f-1)+e1*(2-3*f))**2)+8*e1*e)**0.5))/(-4)
        # np.roots([-2, (e*(3*f-1)+e1*(2-3*f)), e1*e])[root]
        out = np.empty(len(e), dtype=np.cdouble)
        sign = "-"
        for i in range(len(e)):
            b = (e[i]*(3*f-1)+e1[i]*(2-3*f))
            c = e1[i]*e[i]
            delta = 0-(4*a*c)+b**2
            if sign == "-":
                if i == 0 or i == 1:
                    out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f)))-((((e[i]*(3*f-1)+e1[i]
                                                                   * (2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)  # (-b-(delta**0.5))/2*a
                else:
                    out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) -
                              ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                    if np.abs(out[i]-out[i-1])-(out[i-1]-out[i-2]) > 1:
                        print("change - to + sign")
                        sign = "+"
                        out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                                  ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
            else:
                if i == 0 or i == 1:
                    out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                              ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                else:
                    out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                              ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                    if np.abs((out[i]-out[i-1])-(out[i-1]-out[i-2])) > 1:
                        print("change + to - sign")

                        sign = "-"
                        out[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) -
                                  ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)

        out1 = np.empty(len(e), dtype=np.cdouble)
        sign = "+"
        for i in range(len(e)):
            b = (e[i]*(3*f-1)+e1[i]*(2-3*f))
            c = e1[i]*e[i]
            delta = 0-(4*a*c)+b**2
            if sign == "-":
                if i == 0 or i == 1:
                    out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f)))-((((e[i]*(3*f-1)+e1[i]
                                                                    * (2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)  # (-b-(delta**0.5))/2*a
                else:
                    out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) -
                               ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                    if np.abs(out1[i]-out1[i-1])-(out1[i-1]-out1[i-2]) > 1:
                        print("change - to + sign")
                        sign = "+"
                        out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                                   ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
            else:
                if i == 0 or i == 1:
                    out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                               ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                else:
                    out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) +
                               ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
                    if np.abs((out1[i]-out1[i-1])-(out1[i-1]-out1[i-2])) > 1:
                        print("change + to - sign")

                        sign = "-"
                        out1[i] = (0-((e[i]*(3*f-1)+e1[i]*(2-3*f))) -
                                   ((((e[i]*(3*f-1)+e1[i]*(2-3*f))**2)+8*e1[i]*e[i])**0.5))/(-4)
        scoreforout = 0
        scoreforout1 = 0

        for i in range(len(e)):
            if np.real(e[i]-e1[i]) > 0:
                if np.real((e[i]-e1[i])-(e[i]-out[i])) > 0:
                    scoreforout += 1
                if np.real((e[i]-e1[i])-(e[i]-out1[i])) > 0:
                    scoreforout1 += 1
            else:
                if(np.real(e1[i]-e[i])-(e1[i]-out[i])) > 0:
                    scoreforout += 1
                if(np.real(e1[i]-e[i])-(e1[i]-out1[i])) > 0:
                    scoreforout1 += 1
            if np.imag(e[i]-e1[i]) > 0:
                if np.imag((e[i]-e1[i])-(e[i]-out[i])) > 0:
                    scoreforout += 1
                if np.imag((e[i]-e1[i])-(e[i]-out1[i])) > 0:
                    scoreforout1 += 1
            else:
                if(np.imag(e1[i]-e[i])-(e1[i]-out[i])) > 0:
                    scoreforout += 1
                if(np.imag(e1[i]-e[i])-(e1[i]-out1[i])) > 0:
                    scoreforout1 += 1
        print(scoreforout, scoreforout1)
        if scoreforout > scoreforout1:
            return out
        else:
            return out1
    else:
        ffirst = (f[0])/(f[0]+f[1])
        ffsec = (f[1])/(f[0]+f[1])
        e_for_e_and_e1 = mixsolver([ffirst, ffsec], e, e1)
        return mixsolver([f[0]+f[1], f[2]], e_for_e_and_e1, e2)


def calcdrude(frequency, frequencyn, gamma, sigma):
    return -frequencyn*frequencyn / (frequency*(frequency + 1j*gamma)) * sigma


def calclorentizan(frequency, frequencyn, gamma, sigma):
    return frequencyn*frequencyn / (frequencyn*frequencyn - frequency*frequency - 1j*gamma*frequency) * sigma


def preprocess(input, max, min, max_imag, min_imag):
    real = input.real - min.real
    real = real / (max.real - min.real)

    imag = input.imag - min_imag
    imag = imag / (max_imag - min_imag)

    return np.stack((real, imag), axis=-1)


def predict_single(input):
    import pickle
    import tensorflow as tf

    variables = pickle.load(open("variables.p", "rb"))
    in_processed = preprocess(
        input, variables['max'], variables['min'], variables['max_imag'], variables['min_imag'])
    model = tf.keras.models.load_model('my_model.h5')
    in_processed = np.expand_dims(in_processed, axis=0)
    result = model.predict(in_processed)[0]
    return result * variables['scale']
