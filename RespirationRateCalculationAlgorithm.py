import numpy as np
from params import args
from scipy.fftpack import fft
from scipy.signal import find_peaks

class RR_Algorithm :
    def __init__(self, data, fs) :
        self.data = data
        self.fs = fs
        self.N = len(data)
        self.Time = self.N / fs

    # # Fast Fourier Transform Method
    def FFT(self):
        fft_y = fft(self.data)
        maxFrequency = self.fs
        f = np.linspace(0, maxFrequency, self.N)
        abs_y = np.abs(fft_y)
        normalization_y = abs_y / self.N
        normalization_half_y = normalization_y[range(int(self.N / 2))]
        sorted_indices = np.argsort(normalization_half_y)
        RR = f[sorted_indices[-1]] * 60
        return RR

    # # Peak Counting Method
    def PeakCounting(self, Height=args.RR_Algorithm_PC_Height, Threshold=args.RR_Algorithm_PC_Threshold, MaxRR=args.RR_Algorithm_PC_MaxRR):
        Distance = 60 / MaxRR * self.fs
        peaks, _ = find_peaks(self.data, height=Height, threshold=Threshold, distance=Distance)
        RR = len(peaks) / self.Time * 60
        return RR

    # # Crossover Point Method
    def CrossingPoint(self):
        shfit_distance = int(self.fs / 2)
        data_shift = np.zeros(self.data.shape) - 1
        data_shift[shfit_distance:] = self.data[:-shfit_distance]
        cross_curve = self.data - data_shift

        zero_number = 0
        zero_index = []
        for i in range(len(cross_curve) - 1) :
            if cross_curve[i] == 0 :
                zero_number += 1
                zero_index.append(i)
            else :
                if cross_curve[i] * cross_curve[i + 1] < 0 :
                    zero_number += 1
                    zero_index.append(i)

        cw = zero_number
        N = self.N
        fs = self.fs
        RR1 = ((cw / 2) / (N / fs)) * 60

        return RR1

    def NegativeFeedbackCrossoverPointMethod(self, QualityLevel=args.RR_Algorithm_NFCP_qualityLevel):
        shfit_distance = int(self.fs / 2)
        data_shift = np.zeros(self.data.shape) - 1
        data_shift[shfit_distance:] = self.data[:-shfit_distance]
        cross_curve = self.data - data_shift

        zero_number = 0
        zero_index = []
        for i in range(len(cross_curve) - 1) :
            if cross_curve[i] == 0 :
                zero_number += 1
                zero_index.append(i)
            else :
                if cross_curve[i] * cross_curve[i + 1] < 0 :
                    zero_number += 1
                    zero_index.append(i)

        cw = zero_number
        N = self.N
        fs = self.fs
        RR1 = ((cw / 2) / (N / fs)) * 60

        if (len(zero_index) <= 1 ) :
                RR2 = RR1
        else:
            time_span = 60 / RR1 / 2 * fs * QualityLevel
            zero_span = []
            for i in range(len(zero_index) - 1) :
                zero_span.append(zero_index[i + 1] - zero_index[i])

            while(min(zero_span) < time_span ) :
                doubt_point = np.argmin(zero_span)
                zero_index.pop(doubt_point)
                zero_index.pop(doubt_point)
                if len(zero_index) <= 1:
                    break
                zero_span = []
                for i in range(len(zero_index) - 1):
                    zero_span.append(zero_index[i + 1] - zero_index[i])

            zero_number = len(zero_index)
            cw = zero_number
            N = self.N
            fs = self.fs
            RR2 = ((cw / 2) / (N / fs)) * 60

        return RR2