import cv2
import numpy as np
from skimage.measure import label
from skimage.measure import regionprops

FILTER_DIM = 3


def extract_features(heatmap_prob, t=0.90):
    heatmap_prob[heatmap_prob < int(t * 255)] = 0
    heatmap_prob[heatmap_prob >= int(t * 255)] = 255
    close_kernel = np.ones((FILTER_DIM, FILTER_DIM), dtype=np.uint8)
    image_close = cv2.morphologyEx(np.array(heatmap_prob), cv2.MORPH_CLOSE, close_kernel)
    open_kernel = np.ones((FILTER_DIM, FILTER_DIM), dtype=np.uint8)
    image_open = cv2.morphologyEx(np.array(image_close), cv2.MORPH_OPEN, open_kernel)
    heatmap_prob = image_open[:, :, :1]
    heatmap_prob = np.reshape(heatmap_prob, (heatmap_prob.shape[0], heatmap_prob.shape[1]))

    print(heatmap_prob.ndim)
    labeled_img = label(heatmap_prob)
    region_props = regionprops(labeled_img)
    n_regions = len(region_props)
    print('No of regions: %d' % n_regions)
    for index in range(n_regions):
        print('\n\nDisplaying region: %d' % index)
        region = region_props[index]
        for prop in region:
            print(prop + ': ', region[prop])
            if prop == 'bbox':
                cv2.rectangle(image_open, (region[prop][1], region[prop][0]),
                              (region[prop][3], region[prop][2]), color=(0, 255, 0),
                              thickness=1)
            if prop == 'centroid':
                cv2.ellipse(image_open, (int(region[prop][1]), int(region[prop][0])),
                            (int(region['major_axis_length'] / 2), int(region['minor_axis_length'] / 2)),
                            region['orientation'], 0, 360, color=(0, 0, 255),
                            thickness=2)

    cv2.imshow('bbox', image_open)


old_prob = cv2.imread('tumor_076_prob_old.png')
extract_features(np.array(old_prob))
# new_prob = cv2.imread('tumor_076_prob_new.png')
# old_new_prob = np.array(old_prob)
old_threshold = np.array(old_prob)

# for row in range(old_prob.shape[0]):
#     for col in range(old_prob.shape[1]):
#         if old_prob[row, col, 0] >= 0.70*255 and new_prob[row, col, 0] < 0.50*255:
#             old_new_prob[row, col, :] = new_prob[row, col, :]


# old_new_prob[new_prob < 0.20*255] = 0

old_threshold[old_threshold < int(0.90 * 255)] = 0
old_threshold[old_threshold >= int(0.90 * 255)] = 255
# new_prob[new_prob >= 0.51*255] = 255
# old_prob[old_prob < 0.90*255] = 0
# new_prob[new_prob < 0.51*255] = 0

# cv2.imshow('old_prob', old_prob)
# cv2.imshow('old_new_prob', old_new_prob)


close_kernel = np.ones((FILTER_DIM, FILTER_DIM), dtype=np.uint8)
image_close = cv2.morphologyEx(np.array(old_threshold), cv2.MORPH_CLOSE, close_kernel)
open_kernel = np.ones((FILTER_DIM, FILTER_DIM), dtype=np.uint8)
image_open = cv2.morphologyEx(np.array(image_close), cv2.MORPH_OPEN, open_kernel)
print(image_open.shape)

# cv2.imshow('old_threshold', old_threshold)
# cv2.imshow('image_close', image_close)
cv2.imshow('image_open', image_open)
# cv2.imshow('new_prob', new_prob)
cv2.waitKey(0) & 0xFF
