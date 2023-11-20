import argparse

parser = argparse.ArgumentParser('Lightweight Video-based Respiration Rate Detection Algorithm script', add_help=False)
parser.add_argument('--video-path', default='./test10.mp4', help='Video input path')

# # Optical flow parameters
parser.add_argument('--OFP-maxCorners', default=100, type=int, help='')
parser.add_argument('--OFP-qualityLevel', default=0.1, type=float, help='')
parser.add_argument('--OFP-minDistance', default=7, type=int, help='')
parser.add_argument('--OFP-mask', default=None, help='')
parser.add_argument('--OFP-QualityLevelRV', default=0.05, type=float, help='QualityLeve reduction value')
parser.add_argument('--OFP-winSize', default=(15, 15), help='')
parser.add_argument('--OFP-maxLevel', default=2, type=int, help='')

# # FeaturePoint Selection Strategy parameters
parser.add_argument('--FSS-switch', action='store_true', dest='FSS_switch')
parser.add_argument('--FSS-maxCorners', default=100, type=int, help='')
parser.add_argument('--FSS-qualityLevel', default=0.1, type=float, help='')
parser.add_argument('--FSS-minDistance', default=7, type=int, help='')
parser.add_argument('--FSS-mask', default=None, help='')
parser.add_argument('--FSS-QualityLevelRV', default=0.05, type=float, help='QualityLeve reduction value')
parser.add_argument('--FSS-FPN', default=5, type=int, help='The number of feature points for the feature point selection strategy')

# # CCorrelation-Guided Optical Flow Method parameters
parser.add_argument('--CGOF-switch', action='store_true', dest='CGOF_switch')

# # Filter parameters
parser.add_argument('--Filter-switch', action='store_true', dest='Filter_switch')
parser.add_argument('--Filter-type', default='bandpass', help='')
parser.add_argument('--Filter-order', default=3, type=int, help='')
parser.add_argument('--Filter-LowPass', default=2, type=int, help='')
parser.add_argument('--Filter-HighPass', default=40, type=int, help='')

# # Normalization parameters
parser.add_argument('--Normalization-switch', action='store_true', dest='Normalization_switch')

# # RR Evaluation parameters
parser.add_argument('--RR-switch', action='store_true', dest='RR_switch')

# # RR Algorithm parameters
parser.add_argument('--RR-Algorithm-PC-Height', default=None, help='')
parser.add_argument('--RR-Algorithm-PC-Threshold', default=None, help='')
parser.add_argument('--RR-Algorithm-PC-MaxRR', default=45, type=int, help='')
parser.add_argument('--RR-Algorithm-CP-shfit_distance', default=15, type=int, help='')
parser.add_argument('--RR-Algorithm-NFCP-shfit_distance', default=15, type=int, help='')
parser.add_argument('--RR-Algorithm-NFCP-qualityLevel', default=0.6, type=float, help='')

args = parser.parse_args()
