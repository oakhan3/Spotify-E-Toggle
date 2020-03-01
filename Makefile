.PHONY: format dist

format:
	black --line-length=100 bin spotify_e_toggle tests

dist:
	pyinstaller bin/toggle-explicit.py -F -n spotify-e-toggle
