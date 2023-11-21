import cv2
import numpy as np
from params import args
import matplotlib.pyplot as plt
from IOF import ImproveOpticalFlow

def main():
    video_path = args.video_path
    cap = cv2.VideoCapture(video_path)
    video_fs = cap.get(5)

    Resp, RR_FFT, RR_PC, RR_CP, RR_NFCP = ImproveOpticalFlow(video_path,
                                                           QualityLevel=args.OFP_qualityLevel,
                                                           FSS=True,
                                                           CGOF=True,
                                                           filter=True,
                                                           Normalization=True,
                                                           RR_Evaluation=True)
    print('RR-FFT: {}(bpm)\nRR-PC: {}(bpm)\nRR-CP: {}(bpm)\nRR-NFCP: {}(bpm)'.format(RR_FFT, RR_PC, RR_CP, RR_NFCP))
    t = np.linspace(1, len(Resp) / video_fs, len(Resp))
    plt.plot(t, Resp)
    plt.xlabel("Time ( s )")
    plt.title('RR-FFT: {}(bpm)      RR-PC: {}(bpm)\nRR-CP: {}(bpm)      RR-NFCP: {}(bpm)'.format(RR_FFT, RR_PC, RR_CP, RR_NFCP))
    plt.show()

if __name__ == '__main__':
    main()
