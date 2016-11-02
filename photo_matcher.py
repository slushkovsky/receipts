import os
import json

import cv2
import numpy as np

from . import config


def match(filepath): 
	assert os.path.exists(filepath)

	img = cv2.imread(filepath)

	assert img is not None

	with open(os.path.join(config.PRESETS_DIR, 'presets.json'), 'r') as f: 
		presets = json.load(f)

	match_results = []

	for img_path in presets:
		preset_img = cv2.imread(os.path.join(config.PRESETS_DIR, img_path)) # TODO: In cache
		
		assert preset_img is not None

		preset_size = (preset_img.shape[1], preset_img.shape[0]) # NOTE: width, height

		matching = cv2.matchTemplate(cv2.resize(img, preset_size), preset_img, cv2.TM_SQDIFF_NORMED)

		assert isinstance(matching, np.ndarray)
		assert matching.shape == (1, 1)

		matching_coeff = matching[0][0]

		match_results.append((img_path, matching_coeff))

	best_match = sorted(match_results, key=lambda m: m[1])[0]

	return presets[best_match[0]]