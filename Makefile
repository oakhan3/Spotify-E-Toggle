.PHONY: format

format:
	black --line-length=100 bin spotify_e_toggle tests
