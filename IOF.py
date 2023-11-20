import cv2
import numpy as np
from params import args
from scipy import signal
from RespirationRateCalculationAlgorithm import RR_Algorithm

def FeaturePointSelectionStrategy(Image, FPN=5, QualityLevel=0.3):
    Image_gray = Image
    feature_params = dict(maxCorners=args.FSS_maxCorners,
                          qualityLevel=QualityLevel,
                          minDistance=args.FSS_minDistance)

    p0 = cv2.goodFeaturesToTrack(Image_gray, mask=args.FSS_mask, **feature_params)

    """ Robust checking """
    while(p0 is None):
        QualityLevel = QualityLevel - args.FSS_QualityLevelRV
        feature_params = dict(maxCorners=args.FSS_maxCorners,
                              qualityLevel=QualityLevel,
                              minDistance=args.FSS_minDistance)
        p0 = cv2.goodFeaturesToTrack(Image_gray, mask=None, **feature_params)

    if len(p0) < FPN:
        FPN = len(p0)

    h = Image_gray.shape[0] / 2
    w = Image_gray.shape[1] / 2

    p1 = p0.copy()
    p1[:, :, 0] -= w
    p1[:, :, 1] -= h
    p1_1 = np.multiply(p1, p1)
    p1_2 = np.sum(p1_1, 2)
    p1_3 = np.sqrt(p1_2)
    p1_4 = p1_3[:, 0]
    p1_5 = np.argsort(p1_4)

    FPMap = np.zeros((FPN, 1, 2), dtype=np.float32)
    for i in range(FPN):
        FPMap[i, :, :] = p0[p1_5[i], :, :]

    return FPMap


def CorrelationGuidedOpticalFlowMethod(FeatureMtx_Amp, RespCurve):
    CGAmp_Mtx = FeatureMtx_Amp.T
    CGAmpAugmented_Mtx = np.zeros((CGAmp_Mtx.shape[0] + 1, CGAmp_Mtx.shape[1]))
    CGAmpAugmented_Mtx[0, :] = RespCurve
    CGAmpAugmented_Mtx[1:, :] = CGAmp_Mtx

    Correlation_Mtx = np.corrcoef(CGAmpAugmented_Mtx)
    CM_mean = np.mean(abs(Correlation_Mtx[0, 1:]))
    Quality_num = (abs(Correlation_Mtx[0, 1:]) >= CM_mean).sum()
    QualityFeaturePoint_arg = (abs(Correlation_Mtx[0, 1:]) >= CM_mean).argsort()[0 - Quality_num:]

    CGOF_Mtx = np.zeros((FeatureMtx_Amp.shape[0], Quality_num))

    for i in range(Quality_num):
        CGOF_Mtx[:, i] = FeatureMtx_Amp[:, QualityFeaturePoint_arg[i]]

    CGOF_Mtx_RespCurve = np.sum(CGOF_Mtx, 1) / Quality_num

    return CGOF_Mtx_RespCurve


def ImproveOptocalFlow(video_path, QualityLevel=0.3, FSS=False, CGOF=False, filter=True, Normalization=False, RR_Evaluation=False):
    video_filename = video_path

    cap = cv2.VideoCapture(video_filename)
    feature_params = dict(maxCorners=args.OFP_maxCorners,
                          qualityLevel=QualityLevel,
                          minDistance=args.OFP_minDistance)

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=args.OFP_mask, **feature_params)

    """ Robust Checking """
    while(p0 is None) :
        QualityLevel = QualityLevel - args.OFP_QualityLevelRV
        feature_params = dict(maxCorners=args.OFP_maxCorners,
                              qualityLevel=QualityLevel,
                              minDistance=args.OFP_minDistance)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    """ FeaturePoint Selection Strategy """
    if FSS:
        p0 = FeaturePointSelectionStrategy(Image=old_gray, FPN=args.FSS_FPN, QualityLevel=args.FSS_qualityLevel)

    else:
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    lk_params = dict(winSize=args.OFP_winSize, maxLevel=args.OFP_maxLevel)
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    FeatureMtx = np.zeros((int(total_frame), p0.shape[0], 2))
    FeatureMtx[0, :, 0] = p0[:, 0, 0].T
    FeatureMtx[0, :, 1] = p0[:, 0, 1].T
    frame_num = 1;

    while (frame_num < total_frame):
        frame_num += 1
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pl, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        old_gray = frame_gray.copy()
        p0 = pl.reshape(-1, 1, 2)
        FeatureMtx[frame_num - 1, :, 0] = p0[:, 0, 0].T
        FeatureMtx[frame_num - 1, :, 1] = p0[:, 0, 1].T

    FeatureMtx_Amp = np.sqrt(FeatureMtx[:, :, 0] ** 2 + FeatureMtx[:, :, 1] ** 2)
    RespCurve = np.sum(FeatureMtx_Amp, 1) / p0.shape[0]

    """ CCorrelation-Guided Optical Flow Method """
    if CGOF:
        RespCurve = CorrelationGuidedOpticalFlowMethod(FeatureMtx_Amp, RespCurve)

    fs = cap.get(5)

    """" Filter """
    if filter:
        original_signal = RespCurve
        #
        filter_order = args.Filter_order
        LowPass = args.Filter_LowPass / 60
        HighPass = args.Filter_HighPass / 60
        b, a = signal.butter(filter_order, [2 * LowPass / fs, 2 * HighPass / fs], args.Filter_type)
        filtedResp = signal.filtfilt(b, a, original_signal)
    else:
        filtedResp = RespCurve

    """ Normalization """
    if Normalization:
        Resp_max = max(filtedResp)
        Resp_min = min(filtedResp)
        Resp_norm = (filtedResp - Resp_min) / (Resp_max - Resp_min) - 0.5
    else:
        Resp_norm = filtedResp

    """ RR Evaluation"""
    RR_method = RR_Algorithm(Resp_norm, fs)
    RR_FFT = RR_method.FFT()
    RR_PC = RR_method.PeakCounting()
    RR_CP = RR_method.CrossingPoint()
    RR_NFCP = RR_method.NegativeFeedbackCrossoverPointMethod()

    if RR_Evaluation:
        return 1 - Resp_norm, round(RR_FFT, 2), round(RR_PC, 2), round(RR_CP, 2), round(RR_NFCP, 2)
    else:
        return 1 - Resp_norm
