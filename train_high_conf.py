from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

base_model = LinearSVC(C=1.0, class_weight='balanced', max_iter=5000, dual='auto', random_state=42)
model = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)